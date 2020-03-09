# coding:utf-8
import random
import sys

from PyQt5 import QtWidgets
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPainter, QIcon, QPen, QColor, QBrush
from PyQt5.QtWidgets import QLabel, QCheckBox, QPushButton, QLineEdit, QAction, QFileDialog, QGridLayout

from chartview import ChartView
from configurations import Configurations
from settingwindow import SettingWindow


class MainUi(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setObjectName('main')
        self.configurations = Configurations()
        self.m_tooltip = None
        self.m_callouts = list()

        # self.statusBar().showMessage("Ready")
        # self.start_range = 0
        # self.end_range = self.configurations.time_max_range
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
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(10)  # 去除缝隙
        self.chart1 = QChart()
        self.chart2 = QChart()
        self.chart_view1 = ChartView(chart=self.chart1, data=self.original_data_1)
        self.chart_view2 = ChartView(chart=self.chart2, data=self.original_data_2)

        self.chart_view1.setObjectName("chart1")
        self.chart_view2.setObjectName("chart2")

        self.series_1 = QLineSeries()
        self.series_2 = QLineSeries()
        self.series_3 = QSplineSeries()
        self.series_3_point = QScatterSeries()
        self.series_3.setName("series")
        self.timer = QTimer()
        self.start_range_input = QLineEdit()
        self.end_range_input = QLineEdit()
        self.label_1 = QLabel("Start index")
        self.label_2 = QLabel("End index")
        self.rang_btn = QPushButton("Enter")
        self.check_data1 = QCheckBox("Data 1")
        self.check_data2 = QCheckBox("Data 2")

        self.start_btn = QPushButton("Start")
        self.start_btn.setIcon(QIcon("start.png"))
        # self.start_btn.setFixedSize(70, 40)

        self.main_layout.addLayout(self.control_layout, 1, 1)
        self.main_layout.setColumnStretch(0, 2)
        self.main_layout.setColumnStretch(1, 1)
        self.main_layout.setRowStretch(0, 1)
        self.main_layout.setRowStretch(1, 1)
        self.control_layout.addWidget(self.start_btn, 0, 0, Qt.AlignTop | Qt.AlignLeft)
        self.control_layout.setContentsMargins(10, 10, 10, 10)
        # self.control_layout.setOriginCorner(Qt.TopLeftCorner)
        self.init_chart()
        self.init_menu()
        self.init_constellation_diagram()
        self.timer.timeout.connect(self.timer_slot)
        self.timer.start(50)
        # self.chart_view1.setMinimumSize(600, 350)
        # self.chart_view2.setMinimumSize(600, 350)

        self.check_data1.setChecked(True)
        self.check_data2.setChecked(True)
        self.start_btn.clicked.connect(self.stop_slot)
        self.start_btn.setObjectName("start_btu")
        self.rang_btn.clicked.connect(self.change_range)
        self.check_data1.stateChanged.connect(self.change_data)
        self.check_data2.stateChanged.connect(self.change_data)
        # self.save_btn.clicked.connect(self.save_data)
        file = open('stylesheet.css')
        self.stylesheet = file.read()
        # print(self.stylesheet)
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
        pen = QPen(QColor('green'))
        background_brush = QBrush(QColor(0x555555))
        qchart.setBackgroundBrush(background_brush)
        pen.setWidth(1.5)
        series.setPen(pen)
        qchart.axisX().setLinePen(QPen(QColor(0xffffff)))
        qchart.axisY().setLinePen(QPen(QColor(0xffffff)))
        qchart.axisX().setLabelsBrush(QBrush(QColor(0xffffff)))
        qchart.axisY().setLabelsBrush(QBrush(QColor(0xffffff)))
        qchart.axisX().setTitleBrush(QBrush(QColor(0xffffff)))
        qchart.axisY().setTitleBrush(QBrush(QColor(0xffffff)))

    def init_chart(self):
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
        # self.chart_view1.setGeometry(10, 10, 600, 350)
        # self.chart_view2.setGeometry(10, 365, 600, 350)

        # self.chart1.legend().setVisible(True)
        self.chart1.legend().setAlignment(Qt.AlignBottom)
        # self.chart2.legend().setVisible(True)
        self.chart2.legend().setAlignment(Qt.AlignBottom)

        # self.series_1.setPointLabelsClipping(True)
        # self.chart1.setAcceptHoverEvents(True)
        self.series_1.setPointsVisible(True)
        self.series_2.setPointsVisible(True)
        self.init_chart_background(self.chart1, self.series_1)
        self.init_chart_background(self.chart2, self.series_2)

    def init_constellation_diagram(self):
        self.constellation_chart = QPolarChart()
        self.constellation_chart_view = QChartView()
        self.constellation_chart_view.setObjectName("chart3")
        self.constellation_chart_view.setChart(self.constellation_chart)
        # self.constellation_chart_view.setMinimumSize(350, 350)
        self.main_layout.addWidget(self.constellation_chart_view, 0, 1)
        # self.constellation_chart_view.setGeometry(615, 10, 350, 350)
        self.radialAxis = QValueAxis()
        self.radialAxis.setRange(self.configurations.mag_min, self.configurations.mag_max)

        self.angularAxis = QValueAxis()
        self.angularAxis.setTickCount(9)
        self.angularAxis.setRange(self.configurations.phase_min, self.configurations.phase_max)
        self.constellation_chart.legend().setVisible(False)
        # self.series_3.setMarkerSize(6.0)
        self.constellation_chart.addSeries(self.series_3)
        self.constellation_chart.addSeries(self.series_3_point)
        self.constellation_chart.addAxis(self.angularAxis, QPolarChart.PolarOrientationAngular)
        self.constellation_chart.addAxis(self.radialAxis, QPolarChart.PolarOrientationRadial)
        self.series_3.attachAxis(self.radialAxis)
        self.series_3.attachAxis(self.angularAxis)
        self.series_3_point.attachAxis(self.radialAxis)
        self.series_3_point.attachAxis(self.angularAxis)
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
        data3 = list()
        self.series_3.replace(data3)
        self.series_3_point.replace(data3[0:1])
        self.count = 0

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
        # mag = 3 * sin(math.pi * self.count / 45) + 5
        mag = random.random() * 3 + 5
        # rand = random.random()
        phase = random.random() * 360
        if not self.is_stop:
            # self.xy_label.setText("Magnitude:%.8f  Phase:%.8f" % (mag, phase))
            self.constellation_chart.setTitle("Magnitude:%.4f  Phase:%.4f" % (mag, phase))
            self.update_data(mag, phase)
            self.chart_view1.updateGeometry()
            self.chart_view2.updateGeometry()

    def stop_slot(self):
        if self.is_stop:
            self.start_action.setText('Stop')
            self.start_btn.setText('Stop')
            self.start_btn.setIcon(QIcon("stop.png"))

            self.configurations.time_max = self.count if self.count > self.configurations.time_max_range else self.configurations.time_max_range
            self.configurations.time_min = self.configurations.time_max - self.configurations.time_max_range
            self.is_stop = False
            data1 = self.original_data_1[self.configurations.time_min:self.configurations.time_max]
            data2 = self.original_data_2[self.configurations.time_min:self.configurations.time_max]
            # data3 = self.original_data_3[self.start_range:self.end_range].append(QPointF(0, 0))

            self.series_1.replace(data1)
            self.series_2.replace(data2)
            # self.series_3.replace(data3[-1])

        else:
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
            # point_3 = QPointF(phase, mag)
            data_1.append(point_1)
            data_2.append(point_2)
            # data_3.append(point_3)
            self.original_data_1.append(point_1)
            self.original_data_2.append(point_2)
            # self.original_data_3.append(point_3)
        if not self.is_stop:
            self.series_1.replace(data_1)
            self.series_2.replace(data_2)
            self.series_3.replace(data3)
            self.series_3_point.replace(data3[0:1])
        self.count += 1
        if data_length > self.configurations.time_max_range and not self.is_stop:
            self.configurations.time_min += 1
            self.configurations.time_max += 1
            self.chart1.axisX().setRange(self.configurations.time_min, self.configurations.time_max)
            self.chart2.axisX().setRange(self.configurations.time_min, self.configurations.time_max)
            # self.series_3.replace(data_3)

            # self.chart.scroll(2, 0)


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
