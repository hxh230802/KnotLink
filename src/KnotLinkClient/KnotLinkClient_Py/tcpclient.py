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
# along with this program.  If not, see <https://www.gnu.org/licenses/ >.

import socket
import threading
import time

class TcpClient:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.heart_beat_interval = 180  # 设置心跳包发送间隔为180秒（3分钟）
        self.heart_beat_timer = None
        self.connected = False
        self.received_data_callback = None

    def connect_to_server(self, ip, port):
        try:
            self.tcp_socket.connect((ip, port))
            self.connected = True
            print("连接成功")
            self.start_heart_beat()
            threading.Thread(target=self.receive_data, daemon=True).start()
        except socket.error as e:
            print("连接失败：", e)

    def start_heart_beat(self):
        self.heart_beat_timer = threading.Timer(self.heart_beat_interval, self.send_heart_beat)
        self.heart_beat_timer.start()

    def send_heart_beat(self):
        if self.connected:
            try:
                self.tcp_socket.sendall(b"heartbeat")
                print("发送心跳包成功")
            except socket.error as e:
                print("发送心跳包失败：", e)
                self.connected = False
        else:
            print("无法发送心跳包，连接已断开。")
        self.start_heart_beat()

    def receive_data(self):
        while self.connected:
            try:
                data = self.tcp_socket.recv(1024)
                if not data:
                    print("连接已断开")
                    self.connected = False
                    break
                print("收到数据：", data)
                if data != b"heartbeat_response":
                    self.handle_received_data(data)
            except socket.error as e:
                print("接收数据失败：", e)
                self.connected = False
                break

    def handle_received_data(self, data):
        # 在这里处理接收到的数据
        print("处理数据：", data)
        if self.received_data_callback:
            self.received_data_callback(data)

    def send_data(self, data):
        if self.connected:
            try:
                self.tcp_socket.sendall(data)
            except socket.error as e:
                print("发送数据失败：", e)
                self.connected = False
        else:
            print("无法发送数据，连接已断开。")

    def disconnect(self):
        self.connected = False
        self.tcp_socket.close()
        if self.heart_beat_timer:
            self.heart_beat_timer.cancel()
        print("已断开连接")

# 示例用法
if __name__ == "__main__":
    client = TcpClient()
    client.connect_to_server("127.0.0.1", 6370)  # 替换为服务器的 IP 和端口
    time.sleep(10)  # 等待一段时间
    client.send_data(b"Hello, Server!")
    time.sleep(60)  # 继续等待一段时间
    client.disconnect()