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

from PyQt5.QtCore import QObject
from .tcpclient import TcpClient  # 确保 tcpclient.py 在同一目录下

class SignalSender(QObject):
    def __init__(self, APPID=None, SignalID=None, parent=None):
        super().__init__(parent)
        self.appID = APPID
        self.signalID = SignalID
        self.KLsender = TcpClient(self)
        self.KLsender.connectToServer("127.0.0.1", 6370)

    def setConfig(self, APPID, SignalID):
        self.appID = APPID
        self.signalID = SignalID

    def emitt(self, data):
        self._emitt(self.appID, self.signalID, data)

    def _emitt(self, APPID, SignalID, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.__emitt(APPID, SignalID, data)

    def __emitt(self, APPID, SignalID, data):
        s_key = f"{APPID}-{SignalID}&*&"
        s_key_bytes = s_key.encode('utf-8')
        s_data = s_key_bytes + data
        self.KLsender.sendData(s_data)