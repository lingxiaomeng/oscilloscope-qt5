from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtNetwork import QTcpSocket


class TcpClient(QThread):
    # Define the signal, define the parameter as str type
    breakSignal = pyqtSignal(str)

    def __init__(self, parent=None, socket: QTcpSocket = None):
        super().__init__(parent)
        self.socket = socket
        # The following initialization methods are all possible, some python versions do not support
        # super(Mythread, self).__init__()

    def run(self):
        # The behavior to be defined, such as starting an activity or something
        recv_data = self.tcpSocket.readAll()
        self.breakSignal.emit(recv_data)
