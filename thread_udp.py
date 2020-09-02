from socket import *

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
        if not self.s:
            print("new socket")
            self.s = socket(AF_INET, SOCK_DGRAM)
            self.s.bind(('127.0.0.1', 5555))

        try:
            print('send')
            self.s.sendto(b'FS', server_addr)
        except timeout:
            print('error')
        except Exception:
            print('exception')


    def run(self) -> None:
        print("start thread")

        if not self.s:

            self.s = socket(AF_INET, SOCK_DGRAM)
            self.s.bind(('127.0.0.1', 5555))

        while self.receive:
            data, addr = self.s.recvfrom(1024)
            print(data)
        # self.s.close()

# include <QThread>
# include <QtCore>
# include <QObject>
# include <QMutex>
# include <iostream>
# include <QtNetwork>
