from math import inf

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout, QLabel, QSpinBox, QPushButton

from configurations import Configurations


class SettingWindow(QtWidgets.QDialog):
    def __init__(self, parent, configurations: Configurations):
        super().__init__(parent=parent)
        self.parent = parent
        self.configurations = configurations
        self.setWindowTitle("configurations.py")
        main_layout = QGridLayout()
        self.setLayout(main_layout)
        self.time_min = QSpinBox()
        self.time_min.setRange(0, 2147483647)
        self.time_min.setValue(0)

        self.time_max = QSpinBox()
        self.time_max.setRange(0, 2147483647)
        self.time_max.setValue(100)

        self.mag_min = QSpinBox()
        # self.mag_min.setRange(0, 1000)
        self.mag_min.setValue(0)

        self.mag_max = QSpinBox()
        # self.mag_max.setRange(0, 1000)
        self.mag_max.setValue(10)

        self.phase_min = QSpinBox()
        self.phase_min.setRange(0, 360)
        self.phase_min.setValue(0)

        self.phase_max = QSpinBox()
        self.phase_max.setRange(0, 360)
        self.phase_max.setValue(360)

        self.btn = QPushButton("OK")

        self.btn.clicked.connect(self.change_configurations)

        main_layout.addWidget(QLabel("Min"), 0, 1)
        main_layout.addWidget(QLabel("Max"), 0, 2)
        main_layout.addWidget(QLabel("Time range"), 1, 0)
        main_layout.addWidget(QLabel("Magnitude range"), 2, 0)
        main_layout.addWidget(QLabel("Phase range"), 3, 0)
        main_layout.addWidget(self.time_min, 1, 1)
        main_layout.addWidget(self.time_max, 1, 2)
        main_layout.addWidget(self.mag_min, 2, 1)
        main_layout.addWidget(self.mag_max, 2, 2)
        main_layout.addWidget(self.phase_min, 3, 1)
        main_layout.addWidget(self.phase_max, 3, 2)

        main_layout.addWidget(self.btn, 4, 2)

    def change_configurations(self):
        if self.time_min.value() > 0:
            self.configurations.time_min = self.time_min.value()
        if self.time_max.value() - self.time_min.value() > 0:
            self.configurations.time_max = self.time_max.value()
        else:
            self.configurations.time_max = self.configurations.time_min + 100
        if self.phase_min.value() > 0:
            self.configurations.phase_min = self.phase_min.value()
        if self.phase_max.value() > 0 - self.phase_min.value():
            self.configurations.phase_max = self.phase_max.value()
        else:
            self.configurations.phase_max = self.configurations.phase_min + 100
        if self.mag_min.value() > 0:
            self.configurations.mag_min = self.mag_min.value()
        if self.mag_max.value() - self.mag_min.value() > 0:
            self.configurations.mag_max = self.mag_max.value()
        else:
            self.configurations.mag_max = self.configurations.mag_min + 100
        if self.configurations.time_max - self.configurations.time_min > 0:
            self.configurations.time_max_range = self.configurations.time_max - self.configurations.time_min
        self.parent.configuration_reset()
        self.close()
