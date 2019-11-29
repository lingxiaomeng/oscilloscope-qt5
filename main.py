# coding:utf-8
import math
import sys
from math import sin, cos

from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *

from chartview import ChartView


class MainUi(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.start_range = 0
        self.end_range = 100
        self.count = 0
        self.original_data_1 = list()
        self.original_data_2 = list()
        self.is_stop = False

        self.setFixedSize(1200, 720)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(5)  # 去除缝隙
        self.chart = QChart()
        self.chart_view = ChartView(ui=self)
        self.series_1 = QLineSeries()
        self.series_2 = QLineSeries()
        self.stop_button = QPushButton("stop")
        self.timer = QTimer()
        self.start_range_input = QLineEdit()
        self.end_range_input = QLineEdit()
        self.label_1 = QLabel("Start index")
        self.label_2 = QLabel("End index")
        self.rang_btn = QPushButton("Enter")
        self.check_data1 = QCheckBox("Data 1")
        self.check_data2 = QCheckBox("Data 2")

        self.main_layout.addWidget(self.stop_button, 5, 1, 1, 1)
        self.main_layout.addWidget(self.start_range_input, 2, 1, 1, 1)
        self.main_layout.addWidget(self.end_range_input, 2, 2, 1, 1)
        self.main_layout.addWidget(self.label_1, 1, 1, 1, 1)
        self.main_layout.addWidget(self.label_2, 1, 2, 1, 1)
        self.main_layout.addWidget(self.rang_btn, 2, 3, 1, 1)
        self.main_layout.addWidget(self.check_data1, 3, 1, 1, 1)
        self.main_layout.addWidget(self.check_data2, 4, 1, 1, 1)

        self.init_chart()
        self.timer.timeout.connect(self.timer_slot)
        self.timer.start(20)
        self.chart_view.setFixedSize(900, 700)
        self.stop_button.clicked.connect(self.stop_slot)
        self.rang_btn.clicked.connect(self.change_range)
        self.check_data1.stateChanged.connect(self.change_data)
        self.check_data2.stateChanged.connect(self.change_data)

    def init_chart(self):
        self.chart.addSeries(self.series_1)
        self.chart.addSeries(self.series_2)
        self.series_1.setName("Data 1")
        self.series_2.setName("Data 2")
        self.chart.createDefaultAxes()
        self.chart.axisX().setRange(self.start_range, self.end_range)
        self.chart.axisY().setRange(-15, 15)
        self.chart.legend().hide()
        self.chart.axisX().setTitleFont(QFont("Microsoft YaHei", 10, QFont.Normal, True))
        self.chart.axisY().setTitleFont(QFont("Microsoft YaHei", 10, QFont.Normal, True))
        self.chart.axisX().setTitleText("Time/sec")
        self.chart.axisY().setTitleText("Speed/m")
        self.chart.axisX().setGridLineVisible(False)
        self.chart.axisY().setGridLineVisible(False)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setChart(self.chart)
        self.main_layout.addWidget(self.chart_view, 0, 0, 35, 1)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

    def change_data(self):
        if not self.check_data1.isChecked():
            self.series_1.setVisible(False)
        else:
            self.series_1.setVisible(True)
        if not self.check_data2.isChecked():
            self.series_2.setVisible(False)
        else:
            self.series_2.setVisible(True)

    def change_range(self):
        start = self.start_range_input.text()
        end = self.end_range_input.text()
        try:
            start = int(start)
            end = int(end)
            start = 0 if start < 0 else start
            end = len(self.original_data_1) - 1 if end >= len(self.original_data_1) else end
            data1 = self.original_data_1[start:end]
            data2 = self.original_data_2[start:end]
            self.series_1.replace(data1)
            self.series_2.replace(data2)
            self.chart.axisX().setRange(start, end)
        except ValueError:
            print("value Error")

    def timer_slot(self):
        self.update_data()

    def stop_slot(self):
        if self.is_stop:
            self.end_range = self.count
            self.start_range = self.end_range - 100
            self.is_stop = False
            data1 = self.original_data_1[self.start_range:self.end_range]
            data2 = self.original_data_2[self.start_range:self.end_range]

            self.series_1.replace(data1)
            self.series_2.replace(data2)
        else:
            self.is_stop = True

    def update_data(self):
        old_data_1 = self.series_1.pointsVector()
        old_data_2 = self.series_2.pointsVector()
        data_length = len(old_data_1)
        data_1 = old_data_1
        data_2 = old_data_2
        if not self.is_stop and data_length > 200:
            data_1 = data_1[-200:-1]
            data_2 = data_2[-200:-1]

        for i in range(1):
            point_1 = QPointF(self.count, 5 * sin(math.pi * self.count / 45))
            point_2 = QPointF(self.count, 5 * cos(math.pi * self.count / 45))
            data_1.append(point_1)
            data_2.append(point_2)
            self.original_data_1.append(point_1)
            self.original_data_2.append(point_2)
        self.series_1.replace(data_1)
        self.series_2.replace(data_2)
        self.count += 1
        if data_length > 100 and not self.is_stop:
            self.start_range += 1
            self.end_range += 1
            self.chart.axisX().setRange(self.start_range, self.end_range)
            # self.chart.scroll(2, 0)

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() < 0:
            self.chart.zoom(0.8)
        else:
            self.chart.zoom(1.1)


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
