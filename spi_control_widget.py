from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5 import QtWidgets


class SpiControlWidget(QtWidgets.QWidget):
    def __int__(self, parent):
        super().__init__(parent=parent)
        self.spi_id1 = QLineEdit()
        self.spi_id2 = QLineEdit()
        self.spi_ok = QPushButton("Send")

        spi_layout = QGridLayout()
        self.setLayout(spi_layout)
        self.setContentsMargins(0, 5, 0, 0)

        spi_layout.addWidget(QLabel("ID 1"), 0, 0, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("ID 2"), 1, 0, Qt.AlignCenter)
        spi_layout.addWidget(self.spi_id1, 0, 1, Qt.AlignCenter)
        spi_layout.addWidget(self.spi_id2, 1, 1, Qt.AlignCenter)
        spi_layout.addWidget(self.spi_ok, 1, 2, Qt.AlignCenter)
