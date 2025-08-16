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

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from .tcpclient import TcpClient  # 确保 tcpclient.py 在同一目录下

class SignalSubscriber(QObject):
    received_data = pyqtSignal(str)
    received_data_a = pyqtSignal(bytes)

    def __init__(self, APPID, SignalID, parent=None):
        super().__init__(parent)
        self.appID = APPID
        self.signalID = SignalID
        self.init()

    def init(self):
        self.KLsubscriber = TcpClient(self)
        self.KLsubscriber.connectToServer("127.0.0.1", 6372)
        print("OKK")
        self.KLsubscriber.receivedData.connect(self.dataRecv)
        s_key = f"{self.appID}-{self.signalID}"
        s_key_bytes = s_key.encode('utf-8')
        self.KLsubscriber.sendData(s_key_bytes)

    def subscribe(self, APPID, SignalID):
        self.appID = APPID
        self.signalID = SignalID
        s_key = f"{self.appID}-{self.signalID}"
        s_key_bytes = s_key.encode('utf-8')
        self.KLsubscriber.sendData(s_key_bytes)

    @pyqtSlot(bytes)
    def dataRecv(self, data):
        self.received_data_a.emit(data)
        received_text = data.decode('utf-8')
        self.received_data.emit(received_text)