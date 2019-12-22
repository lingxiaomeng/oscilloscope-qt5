# coding:utf-8
import math
import random
import sys
from math import sin, cos

from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *

from chartview import ChartView1


class MainUi(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # self.statusBar().showMessage("Ready")
        self.start_range = 0
        self.end_range = 100
        self.count = 0
        self.original_data_1 = list()
        self.original_data_2 = list()
        self.original_data_3 = list()

        self.is_stop = True

        self.setFixedSize(1000, 740)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)  # 去除缝隙
        self.chart1 = QChart()
        self.chart2 = QChart()
        self.chart_view1 = ChartView1(ui=self)
        self.chart_view2 = ChartView1(ui=self)
        self.chart_view1.setObjectName("chart1")
        self.chart_view2.setObjectName("chart2")

        self.series_1 = QLineSeries()
        self.series_2 = QLineSeries()
        self.series_3 = QScatterSeries()
        self.series_3.setName("series")
        self.stop_button = QPushButton("STOP")
        self.timer = QTimer()
        self.start_range_input = QLineEdit()
        self.end_range_input = QLineEdit()
        self.label_1 = QLabel("Start index")
        self.label_2 = QLabel("End index")
        self.rang_btn = QPushButton("Enter")
        self.check_data1 = QCheckBox("Data 1")
        self.check_data2 = QCheckBox("Data 2")
        self.xy_label = QLabel("")
        self.xy_label.setFont(QFont("Microsoft YaHei", 10, QFont.Bold, True))

        self.main_layout.addChildWidget(self.xy_label)
        self.xy_label.setGeometry(615, 365, 350, 20)
        # self.save_btn = QPushButton("Save")

        # self.main_layout.addWidget(self.stop_button, 18, 40, 1, 1)
        # self.main_layout.addWidget(self.save_btn, 5, 2, 1, 1)
        # self.main_layout.addWidget(self.start_range_input, 2, 40, 1, 1)
        # self.main_layout.addWidget(self.end_range_input, 2, 41, 1, 1)
        # self.main_layout.addWidget(self.label_1, 1, 40, 1, 1)
        # self.main_layout.addWidget(self.label_2, 1, 41, 1, 1)
        # self.main_layout.addWidget(self.rang_btn, 2, 42, 1, 1)
        # self.main_layout.addWidget(self.check_data1, 3, 40, 1, 1)
        # self.main_layout.addWidget(self.check_data2, 4, 40, 1, 1)

        self.init_chart()
        self.init_menu()
        self.init_constellation_diagram()
        self.timer.timeout.connect(self.timer_slot)
        self.timer.start(20)
        self.chart_view1.setFixedSize(600, 350)
        self.chart_view2.setFixedSize(600, 350)

        self.check_data1.setChecked(True)
        self.check_data2.setChecked(True)
        self.stop_button.clicked.connect(self.stop_slot)
        self.stop_button.setObjectName("stop_btu")
        self.rang_btn.clicked.connect(self.change_range)
        self.check_data1.stateChanged.connect(self.change_data)
        self.check_data2.stateChanged.connect(self.change_data)
        # self.save_btn.clicked.connect(self.save_data)
        file = open('stylesheet.qss')
        self.stylesheet = file.read()
        # print(self.stylesheet)
        self.setStyleSheet(self.stylesheet)

    def init_menu(self):
        file_menu = self.menuBar().addMenu('File')
        save_action = QAction("Save", self)
        load_action = QAction("Load", self)
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
        self.start_action = QAction("Start", self)
        option_menu = self.menuBar().addMenu('Options')
        range_action = QAction("Range", self)
        option_menu.addAction(range_action)
        self.menuBar().addAction(self.start_action)
        self.start_action.triggered.connect(self.stop_slot)

    def init_chart(self):
        self.chart1.addSeries(self.series_1)
        self.chart2.addSeries(self.series_2)
        self.series_1.setName("Data 1")
        self.series_2.setName("Data 2")
        self.chart1.createDefaultAxes()
        self.chart1.axisX().setRange(self.start_range, self.end_range)
        self.chart1.axisY().setRange(0, 15)
        self.chart1.legend().hide()
        self.chart1.axisX().setTitleFont(QFont("Microsoft YaHei", 10, QFont.Normal, True))
        self.chart1.axisY().setTitleFont(QFont("Microsoft YaHei", 10, QFont.Normal, True))
        self.chart1.axisX().setTitleText("Time/sec")
        self.chart1.axisY().setTitleText("Magnitude")
        self.chart1.axisX().setGridLineVisible(False)
        self.chart1.axisY().setGridLineVisible(False)

        self.chart2.createDefaultAxes()
        self.chart2.axisX().setRange(self.start_range, self.end_range)
        self.chart2.axisY().setRange(0, 360)
        self.chart2.legend().hide()
        self.chart2.axisX().setTitleFont(QFont("Microsoft YaHei", 10, QFont.Normal, True))
        self.chart2.axisY().setTitleFont(QFont("Microsoft YaHei", 10, QFont.Normal, True))
        self.chart2.axisX().setTitleText("Time/sec")
        self.chart2.axisY().setTitleText("Phase")
        self.chart2.axisX().setGridLineVisible(False)
        self.chart2.axisY().setGridLineVisible(False)

        self.chart_view1.setRenderHint(QPainter.Antialiasing)
        self.chart_view1.setChart(self.chart1)

        self.chart_view2.setRenderHint(QPainter.Antialiasing)
        self.chart_view2.setChart(self.chart2)

        self.main_layout.addChildWidget(self.chart_view1)
        self.main_layout.addChildWidget(self.chart_view2)
        self.chart_view1.setGeometry(10, 10, 600, 350)
        self.chart_view2.setGeometry(10, 365, 600, 350)

        # self.chart1.legend().setVisible(True)
        self.chart1.legend().setAlignment(Qt.AlignBottom)
        # self.chart2.legend().setVisible(True)
        self.chart2.legend().setAlignment(Qt.AlignBottom)

    def init_constellation_diagram(self):
        self.constellation_chart = QPolarChart()
        self.constellation_chart_view = QChartView()
        self.constellation_chart_view.setObjectName("chart3")
        self.constellation_chart_view.setChart(self.constellation_chart)
        self.constellation_chart_view.setFixedSize(350, 350)
        self.main_layout.addChildWidget(self.constellation_chart_view)
        self.constellation_chart_view.setGeometry(615, 10, 350, 350)
        self.radialAxis = QValueAxis()
        self.radialAxis.setRange(0, 10)

        self.angularAxis = QValueAxis()
        self.angularAxis.setTickCount(9)
        self.angularAxis.setRange(0, 360)
        self.constellation_chart.legend().setVisible(False)
        self.series_3.setMarkerSize(6.0)
        self.constellation_chart.addSeries(self.series_3)
        self.constellation_chart.addAxis(self.angularAxis, QPolarChart.PolarOrientationAngular)
        self.constellation_chart.addAxis(self.radialAxis, QPolarChart.PolarOrientationRadial)
        self.series_3.attachAxis(self.radialAxis)
        self.series_3.attachAxis(self.angularAxis)
        self.constellation_chart_view.setRenderHint(QPainter.Antialiasing)

    def save_data(self):
        filename = QFileDialog.getSaveFileName(self, 'save file', "", "Text Files (*.txt)")
        if filename[0] != '':
            f = open(filename[0], 'w')
            f.write("data1\n")
            for data in self.original_data_1:
                f.write(str(data.y()) + ",")
            f.write("\n")
            f.write("data2\n")
            for data in self.original_data_2:
                f.write(str(data.y()) + ",")
            f.write("\n")
            f.close()

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
            self.chart1.axisX().setRange(start, end)
            self.chart2.axisX().setRange(start, end)

        except ValueError:
            print("value Error")

    def timer_slot(self):
        mag = 3 * sin(math.pi * self.count / 45) + 5
        mag = random.random() * 3 + 5
        rand = random.random()
        phase = random.random() * 360
        if not self.is_stop:
            self.xy_label.setText("Magnitude:%.8f  Phase:%.8f" % (mag, phase))

        # if rand < 0.25:
        #     phase = 90
        # elif rand < 0.5:
        #     phase = 180
        # elif rand < 0.75:
        #     phase = 270
        # else:
        #     pass

        self.update_data(mag, phase)

    def stop_slot(self):
        if self.is_stop:
            self.start_action.setText('Stop')

            self.end_range = self.count
            self.start_range = self.end_range - 100
            self.is_stop = False
            data1 = self.original_data_1[self.start_range:self.end_range]
            data2 = self.original_data_2[self.start_range:self.end_range]
            data3 = self.original_data_3[self.start_range:self.end_range]

            self.series_1.replace(data1)
            self.series_2.replace(data2)
            self.series_3.replace(data3)

        else:
            self.start_action.setText('Start')
            self.is_stop = True

    def update_data(self, mag, phase):
        old_data_1 = self.series_1.pointsVector()
        old_data_2 = self.series_2.pointsVector()
        old_data_3 = self.series_3.pointsVector()
        data_length = len(old_data_1)
        data_1 = old_data_1
        data_2 = old_data_2
        data_3 = old_data_3
        if not self.is_stop and data_length > 200:
            data_1 = data_1[-200:-1]
            data_2 = data_2[-200:-1]

        for i in range(1):
            point_1 = QPointF(self.count, mag)
            point_2 = QPointF(self.count, phase)
            point_3 = QPointF(phase, mag)
            data_1.append(point_1)
            data_2.append(point_2)
            data_3.append(point_3)
            self.original_data_1.append(point_1)
            self.original_data_2.append(point_2)
            self.original_data_3.append(point_3)
        if not self.is_stop:
            self.series_3.replace(data_3)
            self.series_1.replace(data_1)
            self.series_2.replace(data_2)
        self.count += 1
        if data_length > 100 and not self.is_stop:
            self.start_range += 1
            self.end_range += 1
            self.chart1.axisX().setRange(self.start_range, self.end_range)
            self.chart2.axisX().setRange(self.start_range, self.end_range)
            # self.series_3.replace(data_3)

            # self.chart.scroll(2, 0)


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
