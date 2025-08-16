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

from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtNetwork import QTcpSocket, QHostAddress, QAbstractSocket
from PyQt5.QtWidgets import QApplication

class TcpClient(QObject):
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    receivedData = pyqtSignal(bytes)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tcpSocket = QTcpSocket(self)
        self.heartBeatTimer = QTimer(self)
        self.heartBeatTimer.setInterval(180000)  # 设置定时时间为3分钟

        self.tcpSocket.connected.connect(self.socketConnected)
        self.tcpSocket.disconnected.connect(self.socketDisconnected)
        self.tcpSocket.readyRead.connect(self.readData)
        self.tcpSocket.errorOccurred.connect(self.handleError)
        self.heartBeatTimer.timeout.connect(self.sendHeartbeat)

    def connectToServer(self, ip, port):
        self.tcpSocket.connectToHost(QHostAddress(ip), port)
        if not self.tcpSocket.waitForConnected(3000):
            print("连接失败：", self.tcpSocket.errorString())
            return

        self.heartBeatTimer.start()

    def socketConnected(self):
        self.connected.emit()

    def socketDisconnected(self):
        self.disconnected.emit()
        self.heartBeatTimer.stop()

    def readData(self):
        if self.tcpSocket.bytesAvailable() > 0:
            data = self.tcpSocket.readAll().data()
            print("收到数据：", data)
            if data == b"heartbeat_response":
                return
            self.receivedData.emit(data)

    def handleError(self, socketError):
        print("错误：", socketError, "-", self.tcpSocket.errorString())

    def sendHeartbeat(self):
        heartbeatData = b"heartbeat"
        if self.tcpSocket.state() == QAbstractSocket.ConnectedState:
            bytesWritten = self.tcpSocket.write(heartbeatData)
            if bytesWritten == -1:
                print("发送心跳包失败：", self.tcpSocket.errorString())
            else:
                print("发送心跳包成功")
        else:
            print("无法发送心跳包，连接已断开。")

    def sendData(self, data):
        if self.tcpSocket.state() == QAbstractSocket.ConnectedState:
            if self.tcpSocket.write(data) == -1:
                print("发送数据失败：", self.tcpSocket.errorString())
        else:
            print("无法发送数据，连接已断开。")
