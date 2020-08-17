import socket

from PyQt5.QtCore import QThread, QMutexLocker, QMutex
from PyQt5.QtNetwork import QUdpSocket, QHostAddress

server_addr = ('127.0.0.1', 5556)


class UdpThread(QThread):
    def __init__(self, data1, data2, data3):
        super().__init__()
        self.data3 = data3
        self.data2 = data2
        self.data1 = data1
        self.receive = True
        self.s = None
        # self.m_lock = QMutex()

        # QMutexLocker().mutex()

    def stopImmediately(self):
        self.receive = False

    def run(self) -> None:
        print("start thread")
        # socket = QUdpSocket()
        # result = socket.bind(QHostAddress("127.0.0.1"), 5555)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('127.0.0.1', 5555))

        while self.receive:
            data, addr = self.s.recvfrom(1024)
            print(data)
        self.s.close()
        del self.s

# include <QThread>
# include <QtCore>
# include <QObject>
# include <QMutex>
# include <iostream>
# include <QtNetwork>
