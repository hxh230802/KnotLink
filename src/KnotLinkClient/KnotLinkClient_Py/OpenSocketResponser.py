# OpenSocketResponser.py
# Copyright (C) 2025 HXH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/

from .tcpclient import TcpClient  # 确保 tcpclient.py 在同一目录下
from queue import Queue
import threading

class OpenSocketResponser:
    def __init__(self, APPID: str, OpenSocketID: str):
        self.appID = APPID
        self.openSocketID = OpenSocketID
        self.recv_func = None  # 回调函数（str 类型）
        self.data_queue = Queue()  # 线程安全队列
        self.init()

    def init(self):
        self.KLresponser = TcpClient()
        self.KLresponser.connect_to_server("127.0.0.1", 6378)
        self.KLresponser.received_data_callback = self._internal_data_recv

        s_key = f"{self.appID}-{self.openSocketID}"
        s_key_bytes = s_key.encode("utf-8")  # 转换为 UTF-8 编码的 QByteArray
        self.KLresponser.send_data(s_key_bytes)

        # 启动一个线程处理队列中的数据
        threading.Thread(target=self._process_queue, daemon=True).start()

    def sendBack(self, data: str, key: str):
        """向客户端发送响应数据"""
        s_key = f"{key}&*&"
        s_key_bytes = s_key.encode("utf-8")
        s_data = s_key_bytes + data.encode("utf-8")
        self.KLresponser.send_data(s_data)

    def _internal_data_recv(self, data: bytes):
        """内部数据接收处理"""
        try:
            key_end = data.index(b"&*&")
            key = data[:key_end].decode("utf-8")
            payload = data[key_end + 3:]  # 跳过 "&*&"
        except (ValueError, UnicodeDecodeError) as e:
            print(f"解析数据失败：{e}")
            return

        if payload:
            self.data_queue.put((payload.decode("utf-8", errors="ignore"), key))

    def _process_queue(self):
        """处理队列中的数据"""
        while True:
            if not self.data_queue.empty():
                payload, key = self.data_queue.get()
                if self.recv_func:
                    response = self.recv_func(payload)
                    if response is not None:
                        self.sendBack(response, key)
                self.data_queue.task_done()

    def set_RecvFunc(self, recv_func):
        """
        设置接收到字符串数据后的处理函数。
        :param recv_func: 处理函数，接收一个参数：str 类型的数据。
                          处理函数返回一个 str 类型的响应。
        """
        self.recv_func = recv_func

# 示例用法
if __name__ == "__main__":
    import time
    def on_received_data(data: str) -> str:
        print(f"接收到字符串数据：{data}")
        time.sleep(5)
        return f"Hello, Client! Your message has been received."

    responser = OpenSocketResponser("0x00000001", "0x00000002")
    responser.set_RecvFunc(on_received_data)

    # 模拟运行一段时间
    
    time.sleep(60)
    responser.KLresponser.disconnect()