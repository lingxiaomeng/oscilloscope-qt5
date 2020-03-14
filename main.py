# coding:utf-8
import random
import sys

from PyQt5 import QtWidgets
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPainter, QIcon, QPen, QColor, QBrush
from PyQt5.QtWidgets import QLabel, QCheckBox, QPushButton, QLineEdit, QAction, QFileDialog, QGridLayout

from PolarChartView import PolarChartView
from chartview import ChartView
from configurations import Configurations
from settingwindow import SettingWindow


class MainUi(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setObjectName('main')

        self.configurations = Configurations()
        self.count = 0
        self.original_data_1 = list()
        self.original_data_2 = list()
        self.original_data_3 = list()
        self.is_stop = True
        # self.setMinimumSize(1000, 740)

        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.control_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.main_layout.setSpacing(10)  # 去除缝隙
        self.main_layout.addLayout(self.control_layout, 1, 1)
        self.main_layout.setColumnStretch(0, 2)
        self.main_layout.setColumnStretch(1, 1)
        self.main_layout.setRowStretch(0, 1)
        self.main_layout.setRowStretch(1, 1)


        self.chart1 = QChart()
        self.chart2 = QChart()
        self.chart_view1 = ChartView(chart=self.chart1, data=self.original_data_1)
        self.chart_view2 = ChartView(chart=self.chart2, data=self.original_data_2)
        self.constellation_chart = QPolarChart()
        self.constellation_chart_view = PolarChartView(chart=self.constellation_chart)



        self.series_1 = QLineSeries()
        self.series_2 = QLineSeries()

        self.timer = QTimer()

        self.start_btn = QPushButton("Start")
        self.start_btn.setIcon(QIcon("start.png"))
        self.control_layout.addWidget(self.start_btn, 0, 0, Qt.AlignTop | Qt.AlignLeft)
        self.control_layout.setContentsMargins(10, 10, 10, 10)

        self.init_chart()
        self.init_menu()
        self.init_constellation_diagram()
        self.timer.timeout.connect(self.timer_slot)
        # self.timer.start(50)

        self.start_btn.clicked.connect(self.stop_slot)
        self.start_btn.setObjectName("start_btu")

        file = open('stylesheet.css')
        self.stylesheet = file.read()
        self.setStyleSheet(self.stylesheet)
        self.setMouseTracking(True)

    def init_menu(self):
        file_menu = self.menuBar().addMenu('File')
        save_action = QAction("Save", self)
        load_action = QAction("Load", self)
        reset_action = QAction("Reset", self)

        save_action.triggered.connect(self.save_data)
        load_action.triggered.connect(self.load_data)
        reset_action.triggered.connect(self.data_reset)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)

        action_menu = self.menuBar().addMenu('Action')
        self.start_action = QAction("Start", self)
        # option_menu = self.menuBar().addMenu('Options')
        setting_action = QAction("Settings", self)
        file_menu.addAction(setting_action)
        action_menu.addAction(self.start_action)
        action_menu.addAction(reset_action)

        self.start_action.triggered.connect(self.stop_slot)
        setting_action.triggered.connect(self.configuration_setting)

    def init_chart_background(self, qchart: QChart, series: QAbstractSeries):
        pen = QPen(QColor('yellow'))
        background_brush = QBrush(Qt.black)
        qchart.setBackgroundBrush(background_brush)
        pen.setWidthF(2)

        series.setPen(pen)
        qchart.axisX().setLinePen(QPen(QColor(0xffffff)))
        qchart.axisY().setLinePen(QPen(QColor(0xffffff)))
        qchart.axisX().setLabelsBrush(QBrush(QColor(0xffffff)))
        qchart.axisY().setLabelsBrush(QBrush(QColor(0xffffff)))
        qchart.axisX().setTitleBrush(QBrush(QColor(0xffffff)))
        qchart.axisY().setTitleBrush(QBrush(QColor(0xffffff)))

    def init_chart(self):
        self.chart_view1.setObjectName("chart1")
        self.chart_view2.setObjectName("chart2")

        self.chart_view1.addSeries(self.series_1)
        self.chart_view2.addSeries(self.series_2)
        self.series_1.setName("Data 1")
        self.series_2.setName("Data 2")
        self.chart1.createDefaultAxes()
        self.chart1.axisX().setRange(self.configurations.time_min, self.configurations.time_max)
        self.chart1.axisY().setRange(self.configurations.mag_min, self.configurations.mag_max)
        self.chart1.legend().hide()
        self.chart1.axisX().setTitleFont(QFont("Microsoft YaHei", 10, QFont.Normal, True))
        self.chart1.axisY().setTitleFont(QFont("Microsoft YaHei", 10, QFont.Normal, True))
        self.chart1.axisX().setTitleText("Time/sec")
        self.chart1.axisY().setTitleText("Magnitude")
        self.chart1.axisX().setGridLineVisible(False)
        self.chart1.axisY().setGridLineVisible(False)

        self.chart2.createDefaultAxes()
        self.chart2.axisX().setRange(self.configurations.time_min, self.configurations.time_max)
        self.chart2.axisY().setRange(self.configurations.phase_min, self.configurations.phase_max)
        self.chart2.legend().hide()
        self.chart2.axisX().setTitleFont(QFont("Microsoft YaHei", 10, QFont.Normal, True))
        self.chart2.axisY().setTitleFont(QFont("Microsoft YaHei", 10, QFont.Normal, True))
        self.chart2.axisX().setTitleText("Time/sec")
        self.chart2.axisY().setTitleText("Phase")
        self.chart2.axisX().setGridLineVisible(False)
        self.chart2.axisY().setGridLineVisible(False)

        self.chart_view1.setRenderHint(QPainter.Antialiasing)
        self.chart_view2.setRenderHint(QPainter.Antialiasing)

        self.main_layout.addWidget(self.chart_view1, 0, 0)
        self.main_layout.addWidget(self.chart_view2, 1, 0)

        self.chart1.legend().setAlignment(Qt.AlignBottom)
        self.chart2.legend().setAlignment(Qt.AlignBottom)

        self.series_1.setPointLabelsClipping(True)
        # self.chart1.setAcceptHoverEvents(True)
        self.series_1.setPointsVisible(True)
        self.series_2.setPointsVisible(True)
        self.init_chart_background(self.chart1, self.series_1)
        self.init_chart_background(self.chart2, self.series_2)

    def init_constellation_diagram(self):

        self.constellation_chart_view.setObjectName("chart3")
        self.constellation_chart_view.setChart(self.constellation_chart)
        self.constellation_chart.setTitle(' ')
        self.main_layout.addWidget(self.constellation_chart_view, 0, 1)

        radial_axis = QValueAxis()
        radial_axis.setRange(self.configurations.mag_min, self.configurations.mag_max)

        angular_axis = QValueAxis()
        angular_axis.setTickCount(5)
        angular_axis.setRange(self.configurations.phase_min, self.configurations.phase_max)

        self.constellation_chart.legend().setVisible(False)
        self.constellation_chart.addAxis(angular_axis, QPolarChart.PolarOrientationAngular)
        self.constellation_chart.addAxis(radial_axis, QPolarChart.PolarOrientationRadial)

        series_point = QScatterSeries()
        self.constellation_chart.addSeries(series_point)
        series_point.attachAxis(radial_axis)
        series_point.attachAxis(angular_axis)

        series = QSplineSeries()
        self.constellation_chart.addSeries(series)
        series.attachAxis(radial_axis)
        series.attachAxis(angular_axis)

        self.constellation_chart.setTitleBrush(Qt.white)
        self.constellation_chart.setBackgroundBrush(Qt.black)

        angular_axis.setLinePen(Qt.white)
        angular_axis.setGridLinePen(Qt.white)
        angular_axis.setLabelsBrush(Qt.white)
        radial_axis.setLinePen(Qt.white)
        radial_axis.setGridLinePen(Qt.white)
        radial_axis.setLabelsBrush(Qt.white)
        self.constellation_chart_view.setRenderHint(QPainter.Antialiasing)

    def configuration_reset(self):
        self.chart1.axisX().setRange(self.configurations.time_min, self.configurations.time_max)
        self.chart1.axisY().setRange(self.configurations.mag_min, self.configurations.mag_max)
        self.chart2.axisX().setRange(self.configurations.time_min, self.configurations.time_max)
        self.chart2.axisY().setRange(self.configurations.phase_min, self.configurations.phase_max)

        data1 = list()
        data2 = list()
        data1 += (self.original_data_1[self.configurations.time_min:self.configurations.time_max])
        data2 += (self.original_data_2[self.configurations.time_min:self.configurations.time_max])
        self.series_1.replace(data1)
        self.series_2.replace(data2)

    def configuration_setting(self):
        setting_window = SettingWindow(self, self.configurations)
        setting_window.show()
        # print("end")

    def save_data(self):
        filename = QFileDialog.getSaveFileName(self, 'save file', "", "Qt Wave Files (*.qtwave)")
        if filename[0] != '':
            f = open(filename[0], 'w')
            # f.write("data1\n")
            for data in self.original_data_1:
                f.write(str(data.y()) + ",")
            f.write("\n")
            # f.write("data2\n")
            for data in self.original_data_2:
                f.write(str(data.y()) + ",")
            f.write("\n")
            f.close()

    def load_data(self):
        filename = QFileDialog.getOpenFileName(self, 'read file', "", "Qt Wave Files (*.qtwave)")
        if filename[0] != '':
            print(filename)
            f = open(filename[0], 'r')

            data = f.read().split('\n')
            print(data)
            data1 = data[0].split(',')
            data2 = data[1].split(',')
            print(data1)
            print(data2)
            self.original_data_1 = list()
            self.original_data_2 = list()
            length = len(data1) - 1
            for i in range(len(data1) - 1):
                self.original_data_1.append(QPointF(i, float(data1[i])))
                self.original_data_2.append(QPointF(i, float(data2[i])))
            self.series_1.replace(self.original_data_1)
            self.series_2.replace(self.original_data_2)
            self.configurations.update(0, length, length, 0, 360, 0, 10)
            self.configuration_reset()
            self.count = length
            f.close()

    def data_reset(self):
        self.configurations.update(0, 100, 100, 0, 360, 0, 10)
        self.original_data_1 = list()
        self.original_data_2 = list()
        self.series_1.replace(self.original_data_1)
        self.series_2.replace(self.original_data_2)
        self.configuration_reset()
        self.count = 0
        self.constellation_chart_view.arrow.hide()

    def timer_slot(self):
        mag = random.random() * 3 + 5
        phase = random.random() * 360

        if not self.is_stop:
            self.constellation_chart.setTitle("Magnitude:%.4f  Phase:%8f" % (mag, phase))
            self.constellation_chart_view.updateArrow(mag, phase)
            self.update_data(mag, phase)
            # self.chart_view1.updateGeometry()
            # self.chart_view2.updateGeometry()
            # self.updateGeometry()

    def stop_slot(self):
        if self.is_stop:
            self.timer.start(50)
            self.start_action.setText('Stop')
            self.start_btn.setText('Stop')
            self.start_btn.setIcon(QIcon("stop.png"))
            self.configurations.time_max = self.count if self.count > self.configurations.time_max_range else self.configurations.time_max_range
            self.configurations.time_min = self.configurations.time_max - self.configurations.time_max_range
            self.is_stop = False
            data1 = self.original_data_1[self.configurations.time_min:self.configurations.time_max]
            data2 = self.original_data_2[self.configurations.time_min:self.configurations.time_max]
            self.series_1.replace(data1)
            self.series_2.replace(data2)
        else:
            self.timer.stop()
            self.start_btn.setIcon(QIcon("start.png"))
            self.start_btn.setText('Start')
            self.start_action.setText('Start')
            self.is_stop = True

    def update_data(self, mag, phase):
        old_data_1 = self.series_1.pointsVector()
        old_data_2 = self.series_2.pointsVector()
        data3 = list()
        data3.append(QPoint(phase, mag))
        data3.append(QPoint(0, 0))
        data_length = len(old_data_1)
        data_1 = old_data_1
        data_2 = old_data_2

        if not self.is_stop and data_length > 200:
            data_1 = data_1[-200:-1]
            data_2 = data_2[-200:-1]

        for i in range(1):
            point_1 = QPointF(self.count, mag)
            point_2 = QPointF(self.count, phase)
            data_1.append(point_1)
            data_2.append(point_2)
            self.original_data_1.append(point_1)
            self.original_data_2.append(point_2)
        if not self.is_stop:
            self.series_1.replace(data_1)
            self.series_2.replace(data_2)
        self.count += 1
        if data_length > self.configurations.time_max_range and not self.is_stop:
            self.configurations.time_min += 1
            self.configurations.time_max += 1
            self.chart1.axisX().setRange(self.configurations.time_min, self.configurations.time_max)
            self.chart2.axisX().setRange(self.configurations.time_min, self.configurations.time_max)




def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    icon = QIcon("start.png")
    # icon.addPixmap(QPixmap("my.ico"),QIcon.Normal, QIcon.Off)
    gui.setWindowIcon(icon)
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
