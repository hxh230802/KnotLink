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

from PyQt5.QtCore import QObject, pyqtSignal, QEventLoop
from .tcpclient import TcpClient  # 假设 TcpClient 类已经定义在 tcpclient.py 文件中

class OpenSocketQuerier(QObject):
    dataBack = pyqtSignal(str)
    dataBack_a = pyqtSignal(bytes)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init()

    def __init__(self, APPID: str, OpenSocketID: str, parent=None):
        super().__init__(parent)
        self.appID = APPID
        self.openSocketID = OpenSocketID
        self.init()

    def init(self):
        self.KLquerier = TcpClient(self)
        self.KLquerier.connectToServer("127.0.0.1", 6376)
        self.KLquerier.receivedData.connect(self.dataRecv)
        self.lock = False

    def setConfig(self, APPID: str, OpenSocketID: str):
        self.appID = APPID
        self.openSocketID = OpenSocketID

    def query_l(self, data: str) -> str:
        result = ""
        loop = QEventLoop()  # 创建局部事件循环

        def on_data_received(received_data: bytes):
            nonlocal result
            result = received_data.decode("utf-8")  # 保存信号值
            self.lock = False
            loop.quit()  # 退出事件循环

        self.KLquerier.receivedData.connect(on_data_received)
        self.query(data)
        self.lock = True
        loop.exec_()  # 启动事件循环，阻塞直到退出
        self.KLquerier.receivedData.disconnect(on_data_received)
        return result

    def query(self, data: str):
        self._query_a(self.appID, self.openSocketID, data.encode("utf-8"))

    def query_a(self, data: bytes):
        self._query_a(self.appID, self.openSocketID, data)

    def _query(self, APPID: str, OpenSocketID: str, data: str):
        self._query_a(APPID, OpenSocketID, data.encode("utf-8"))

    def _query_a(self, APPID: str, OpenSocketID: str, data: bytes):
        s_key = f"{APPID}-{OpenSocketID}&*&"
        s_key_bytes = s_key.encode("utf-8")  # 转换为 UTF-8 编码的 QByteArray
        s_data = s_key_bytes + data  # 将 s_key 和 data 合并
        self.KLquerier.sendData(s_data)

    def dataRecv(self, data: bytes):
        if self.lock:
            return
        self.dataBack_a.emit(data)
        received_text = data.decode("utf-8")
        self.dataBack.emit(received_text)
