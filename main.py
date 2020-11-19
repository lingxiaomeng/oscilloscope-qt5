# coding:utf-8
import os
import struct
import sys
import time

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPainter, QIcon, QPen, QColor, QBrush, QKeyEvent, QFontMetrics
from PyQt5.QtNetwork import QHostAddress, QTcpSocket, QAbstractSocket
from PyQt5.QtWidgets import QPushButton, QAction, QFileDialog, QGridLayout, QToolBar, QTableWidget, QHeaderView, QFrame, \
    QLineEdit, QMessageBox, QTabWidget, QWidget, QLabel

from PolarChartView import PolarChartView
from QTableWidgetNumItem import QTableWidgetNumItem
from chartview import ChartView
from configurations import Configurations
from settingwindow import SettingWindow
from utility import ip_auto_detect


class MainUi(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.start_time = 0

        self.server_ip = '192.168.137.10'
        self.port = 5551

        self.mag_min = 4096000
        self.mag_max = -4096000
        self.phase_min = 4096000
        self.phase_max = -4096000

        self.zoom_fit_arg = 0.1

        self.stop_action = QAction("Stop", self)
        self.start_action = QAction("Start", self)
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
        self.controlTab = QTabWidget()
        self.main_layout.addWidget(self.controlTab, 1, 1)
        self.main_layout.setColumnStretch(0, 2)
        self.main_layout.setColumnStretch(1, 1)
        self.main_layout.setRowStretch(0, 1)
        self.main_layout.setRowStretch(1, 1)

        self.chart1 = QChart()
        self.chart2 = QChart()
        self.chart_view1 = ChartView(chart=self.chart1, parent=self)
        self.chart_view2 = ChartView(chart=self.chart2, parent=self)
        self.constellation_chart = QPolarChart()
        self.constellation_chart_view = PolarChartView(chart=self.constellation_chart)

        self.chart_view1.setChartview(self.chart_view2)
        self.chart_view2.setChartview(self.chart_view1)
        self.chart_view1.setPolarChartview(self.constellation_chart_view)
        self.chart_view2.setPolarChartview(self.constellation_chart_view)

        self.series_1 = QLineSeries()
        self.series_2 = QLineSeries()

        self.timer = QTimer()

        self.start_btn = QPushButton("Start")
        self.start_btn.setIcon(QIcon("image/start.png"))
        # self.control_layout.addWidget(self.start_btn, 0, 0, Qt.AlignTop | Qt.AlignLeft)

        self.file_path = QLineEdit()
        self.file_path.setReadOnly(False)
        self.browse_btn = QPushButton('Browse')
        self.save_btn = QPushButton('Save')
        self.load_btn = QPushButton('Load')

        self.browse_btn.clicked.connect(self.choose_path)
        self.save_btn.clicked.connect(self.save_action)
        self.load_btn.clicked.connect(self.load_action)

        self.initControlTab()
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

        self.tcpSocket = QTcpSocket(self)
        # self.tcpSocket.bind('192.168.137.1', 7755)
        self.tcpSocket.readyRead.connect(self.ReadData)
        self.tcpSocket.error.connect(self.ReadError)

        # self.data_to_show = queue.Queue()

        # self.udpSocket.readyRead.connect(self.readPendingDatagrams)
        # self.grabKeyboard()

    def update_range(self, data1, data2):
        if data1 < self.mag_min:
            self.mag_min = data1
        if data1 > self.mag_max:
            self.mag_max = data1
        if data2 < self.phase_min:
            self.phase_min = data2
        if data2 > self.phase_max:
            self.phase_max = data2

    def ReadData(self):  # todo network read data
        recv_data = self.tcpSocket.readAll()
        self.update_data(recv_data)

    def ReadError(self, error: QAbstractSocket.SocketError):
        print('error')
        print(self.tcpSocket.errorString())
        pass

    def initControlTab(self):

        control_widget = QWidget()
        control_widget.setObjectName("c1")

        self.controlTab.addTab(control_widget, 'Main')
        self.controlTab.setObjectName("c0")

        control_widget.setLayout(self.control_layout)
        self.control_layout.addWidget(self.file_path, 0, 0)
        self.control_layout.addWidget(self.browse_btn, 0, 1, Qt.AlignTop | Qt.AlignLeft)
        self.control_layout.addWidget(self.save_btn, 1, 1, Qt.AlignTop | Qt.AlignLeft)
        self.control_layout.addWidget(self.load_btn, 2, 1, Qt.AlignTop | Qt.AlignLeft)
        self.control_layout.setColumnStretch(0, 4)
        self.control_layout.setColumnStretch(1, 1)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.setHorizontalHeaderLabels(['t', 'magnitude', 'phase'])
        # self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().hide()
        self.table.hide()
        # self.table.setMinimumWidth(350)
        self.control_layout.addWidget(self.table, 1, 0, 14, 1, Qt.AlignTop)
        self.control_layout.setContentsMargins(0, 5, 0, 0)

        self.initSpiTab()

    # TODO spi tab
    def initSpiTab(self):
        spi_control_widget = QWidget()
        spi_control_widget.setObjectName("c2")
        self.controlTab.addTab(spi_control_widget, 'SPI')
        spi_layout = QGridLayout()
        spi_control_widget.setLayout(spi_layout)
        spi_control_widget.setContentsMargins(0, 5, 0, 0)

        self.rst_sft = QLineEdit()
        self.rst_cancel = QLineEdit()
        self.baseband = QLineEdit()
        self.reader_tx_en = QLineEdit()
        self.cmd_type = QLineEdit()
        self.cmd_excu = QLineEdit()
        self.main_state = QLineEdit()
        self.carcel_state = QLineEdit()
        self.tx1_amp = QLineEdit()
        self.tx2_amp = QLineEdit()
        self.rx_mean_i = QLineEdit()
        self.rx_mean_q = QLineEdit()
        self.Read_Cmd = QLineEdit()
        self.Write_Cmd = QLineEdit()
        self.Query_Cmd = QLineEdit()
        self.Lock_Cmd = QLineEdit()
        self.FIFO_Count = QLineEdit()
        self.FIFO_Data = QLineEdit()

        spi_layout.addWidget(QLabel("rst_sft"), 0, 0, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("rst_cancel"), 1, 0, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("baseband"), 2, 0, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("reader_tx_en"), 3, 0, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("cmd_type"), 4, 0, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("cmd_excu"), 5, 0, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("main_state"), 6, 0, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("carcel_state"), 7, 0, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("tx1_amp"), 8, 0, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("tx2_amp"), 0, 2, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("rx_mean_i"), 1, 2, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("rx_mean_q"), 2, 2, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("Read_Cmd"), 3, 2, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("Write_Cmd"), 4, 2, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("Query_Cmd"), 5, 2, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("Lock_Cmd"), 6, 2, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("FIFO_Count"), 7, 2, Qt.AlignCenter)
        spi_layout.addWidget(QLabel("FIFO_Data"), 8, 2, Qt.AlignCenter)

        spi_layout.addWidget(self.rst_sft, 0, 1, Qt.AlignCenter)
        spi_layout.addWidget(self.rst_cancel, 1, 1, Qt.AlignCenter)
        spi_layout.addWidget(self.baseband, 2, 1, Qt.AlignCenter)
        spi_layout.addWidget(self.reader_tx_en, 3, 1, Qt.AlignCenter)
        spi_layout.addWidget(self.cmd_type, 4, 1, Qt.AlignCenter)
        spi_layout.addWidget(self.cmd_excu, 5, 1, Qt.AlignCenter)
        spi_layout.addWidget(self.main_state, 6, 1, Qt.AlignCenter)
        spi_layout.addWidget(self.carcel_state, 7, 1, Qt.AlignCenter)
        spi_layout.addWidget(self.tx1_amp, 8, 1, Qt.AlignCenter)
        spi_layout.addWidget(self.tx2_amp, 0, 3, Qt.AlignCenter)
        spi_layout.addWidget(self.rx_mean_i, 1, 3, Qt.AlignCenter)
        spi_layout.addWidget(self.rx_mean_q, 2, 3, Qt.AlignCenter)
        spi_layout.addWidget(self.Read_Cmd, 3, 3, Qt.AlignCenter)
        spi_layout.addWidget(self.Write_Cmd, 4, 3, Qt.AlignCenter)
        spi_layout.addWidget(self.Query_Cmd, 5, 3, Qt.AlignCenter)
        spi_layout.addWidget(self.Lock_Cmd, 6, 3, Qt.AlignCenter)
        spi_layout.addWidget(self.FIFO_Count, 7, 3, Qt.AlignCenter)
        spi_layout.addWidget(self.FIFO_Data, 8, 3, Qt.AlignCenter)

        self.btn_rst_sft = QPushButton('发送')
        self.btn_rst_cancel = QPushButton('rst_cancel')
        self.btn_base_band = QPushButton('rst_baseband')

        spi_layout.addWidget(self.btn_rst_sft, 9, 0)

    def spi_rst_sft(self):
        # TODO spi rst sft
        pass

    def spi_rst_cancel(self):
        # TODO spi
        pass

    def spi_rst_baseband(self):
        # TODO spi
        pass

    def spi_reader_tx_en(self):
        # TODO SPI
        pass

    def spi_cmd_type(self):
        # todo spi
        pass

    def spi_read_cmd(self):
        # todo spi
        pass

    def spi_write_cmd(self):
        # todo spi
        pass

    def spi_query_cmd(self):
        # todo spi
        pass

    def spi_lock_cmd(self):
        # todo spi
        pass

    def init_menu(self):

        file_menu = self.menuBar().addMenu('File')
        action_menu = self.menuBar().addMenu('Action')

        save_action = QAction("Save", self)
        load_action = QAction("Load", self)
        reset_action = QAction("Reset", self)
        setting_action = QAction("Settings", self)
        remove_line_action = QAction("Remove", self)
        tcp_connect_action = QAction("Connect", self)
        zoom_fit_action = QAction("Zoom Fit", self)

        save_action.triggered.connect(self.save_data)
        load_action.triggered.connect(self.load_data)
        reset_action.triggered.connect(self.data_reset)
        self.start_action.triggered.connect(self.stop_slot)
        self.stop_action.triggered.connect(self.stop_slot)
        setting_action.triggered.connect(self.configuration_setting)
        remove_line_action.triggered.connect(self.remove_marker_lines)
        tcp_connect_action.triggered.connect(self.tcp_connect_clicked)
        zoom_fit_action.triggered.connect(self.zoom_fit_action)

        setting_action.setIcon(QIcon('image/setting.png'))
        self.start_action.setIcon(QIcon('image/start.png'))
        self.stop_action.setIcon(QIcon('image/stop.png'))
        remove_line_action.setIcon(QIcon('image/return.png'))
        reset_action.setIcon(QIcon('image/refresh.png'))
        tcp_connect_action.setIcon((QIcon('image/connect.png')))
        zoom_fit_action.setIcon(QIcon('image/autoscale.png'))

        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
        file_menu.addAction(setting_action)
        action_menu.addAction(self.start_action)
        action_menu.addAction(self.stop_action)
        action_menu.addAction(reset_action)
        action_menu.addAction(tcp_connect_action)
        action_menu.addAction(zoom_fit_action)

        toolbar = QToolBar()
        toolbar.setMaximumHeight(30)
        toolbar.addAction(self.start_action)
        toolbar.addAction(self.stop_action)
        toolbar.addAction(setting_action)
        toolbar.addAction(remove_line_action)
        toolbar.addAction(reset_action)
        toolbar.addAction(zoom_fit_action)
        toolbar.addAction(tcp_connect_action)
        toolbar.setMovable(False)
        toolbar.setObjectName('toolbar')
        self.addToolBar(toolbar)

    def init_chart_background(self, qchart: QChart, series: QAbstractSeries):

        # pen = QPen(QColor(0x567EBB))
        pen = QPen(QColor(0xCAFF42))
        background_brush = QBrush(0x1F1F20)
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

        self.radial_axis = QValueAxis()
        self.radial_axis.setRange(self.configurations.mag_min, self.configurations.mag_max)

        angular_axis = QValueAxis()
        angular_axis.setTickCount(5)
        angular_axis.setRange(self.configurations.phase_min, self.configurations.phase_max)

        self.constellation_chart.legend().setVisible(False)
        self.constellation_chart.addAxis(angular_axis, QPolarChart.PolarOrientationAngular)
        self.constellation_chart.addAxis(self.radial_axis, QPolarChart.PolarOrientationRadial)

        series_point = QScatterSeries()
        self.constellation_chart.addSeries(series_point)
        series_point.attachAxis(self.radial_axis)
        series_point.attachAxis(angular_axis)

        series = QSplineSeries()
        self.constellation_chart.addSeries(series)
        series.attachAxis(self.radial_axis)
        series.attachAxis(angular_axis)

        self.constellation_chart.setTitleBrush(Qt.white)
        self.constellation_chart.setBackgroundBrush(QBrush(0x1F1F20))

        angular_axis.setLinePen(Qt.white)
        angular_axis.setGridLinePen(Qt.white)
        angular_axis.setLabelsBrush(Qt.white)
        self.radial_axis.setLinePen(Qt.white)
        self.radial_axis.setGridLinePen(Qt.white)
        self.radial_axis.setLabelsBrush(Qt.white)
        self.constellation_chart_view.setRenderHint(QPainter.Antialiasing)

    def zoom_fit_action(self):
        if len(self.series_1.pointsVector()) > 0:
            chart1_x_min = self.series_1.pointsVector()[0].x()
            chart1_x_max = self.series_1.pointsVector()[-1].x()
            chart1_y_max = self.mag_max
            chart1_y_min = self.mag_min

            chart2_x_min = self.series_2.pointsVector()[0].x()
            chart2_x_max = self.series_2.pointsVector()[-1].x()
            chart2_y_max = self.phase_max
            chart2_y_min = self.phase_min

            self.update_axis_range(chart1_y_min, chart1_y_max, chart2_y_min, chart2_y_max, chart1_x_min, chart1_x_max)

            print(f'{chart1_x_min} {chart1_x_max} {chart1_y_min} {chart1_y_max}')
            print(f'{chart2_x_min} {chart2_x_max} {chart2_y_min} {chart2_y_max}')

            self.mag_min = 4096
            self.mag_max = -4096
            self.phase_min = 4096
            self.phase_max = -4096

            self.chart_view1.update()
            self.chart_view2.update()

    def table_add_row(self, x, mag, phase):
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)
        self.table.setItem(row, 0, QTableWidgetNumItem(x))
        self.table.setItem(row, 1, QTableWidgetNumItem(mag))
        self.table.setItem(row, 2, QTableWidgetNumItem(phase))
        count = self.table.verticalHeader().count()
        self.table.sortItems(0, Qt.AscendingOrder)
        self.table.show()
        scrollBarHeight = self.table.horizontalScrollBar().height()
        horizontalHeaderHeight = self.table.horizontalHeader().height()
        rowTotalHeight = 0
        for i in range(count):
            rowTotalHeight = rowTotalHeight + self.table.rowHeight(i)
        self.table.setMaximumHeight(horizontalHeaderHeight + rowTotalHeight + scrollBarHeight)

    def get_row_width(self, text: str, old_w: int):
        font = QFont()
        fm = QFontMetrics(font)
        w = fm.width(text) + 20
        return w if w > old_w else old_w

    def configuration_reset(self):

        self.update_axis_range(self.configurations.mag_min, self.configurations.mag_max, self.configurations.phase_min,
                               self.configurations.phase_max, self.configurations.time_min,
                               self.configurations.time_min + self.configurations.time_max_range)

        data1 = list()
        data2 = list()
        data1 += (self.original_data_1[self.configurations.time_min:])
        data2 += (self.original_data_2[self.configurations.time_min:])
        self.series_1.replace(data1)
        self.series_2.replace(data2)

    def configuration_setting(self):
        setting_window = SettingWindow(self, self.configurations)
        setting_window.show()
        # print("end")

    def choose_path(self):
        filename = QFileDialog.getOpenFileName(self, 'read file', "", "Qt Wave Files (*.qtwave)")
        if filename[0] != '':
            self.file_path.setText(filename[0])

    def save_action(self):
        try:
            f = open(self.file_path.text(), 'w')
            for data in self.original_data_1:
                f.write(str(data.y()) + ",")
            f.write("\n")
            for data in self.original_data_2:
                f.write(str(data.y()) + ",")
            f.write("\n")
            f.close()
            QMessageBox.information(self, "save succeed", "save succeed", QMessageBox.Ok)
        except:
            QMessageBox.warning(self, "save failed", "save failed", QMessageBox.Ok)

    def load_action(self):
        name, ext = os.path.splitext(self.file_path.text())
        if ext == '.qtwave':
            f = open(self.file_path.text(), 'r')
            data = f.read().split('\n')
            data1 = data[0].split(',')
            data2 = data[1].split(',')
            self.original_data_1 = list()
            self.original_data_2 = list()
            length = len(data1) - 1
            for i in range(len(data1) - 1):
                self.original_data_1.append(QPointF(i, float(data1[i])))
                self.original_data_2.append(QPointF(i, float(data2[i])))
            self.configurations.update(0, length, self.configurations.time_max_range, 0, 360, 0, 10)
            self.configuration_reset()
            self.count = length
            f.close()
            # QMessageBox.information(self, "load succeed", "load succeed", QMessageBox.Ok)
            self.chart_view1.update()
            self.chart_view2.update()
        else:
            QMessageBox.warning(self, "filetype error", "filetype error", QMessageBox.Ok)

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
            f = open(filename[0], 'r')
            data = f.read().split('\n')
            data1 = data[0].split(',')
            data2 = data[1].split(',')
            self.original_data_1 = list()
            self.original_data_2 = list()
            length = len(data1) - 1
            for i in range(len(data1) - 1):
                self.original_data_1.append(QPointF(i, float(data1[i])))
                self.original_data_2.append(QPointF(i, float(data2[i])))
            self.series_1.replace(self.original_data_1)
            self.series_2.replace(self.original_data_2)
            self.configurations.update(0, length, self.configurations.time_max_range, 0, 360, 0, 10)
            self.configuration_reset()
            self.count = length
            f.close()

    def data_reset(self):
        f = open('./tmp.qtwave', 'w')
        for data in self.original_data_1:
            f.write(str(data.y()) + ",")
        f.write("\n")
        for data in self.original_data_2:
            f.write(str(data.y()) + ",")
        f.write("\n")
        f.close()
        # self.configurations.update(0, 100, 100, 0, 360, 0, 10)
        self.original_data_1 = list()
        self.original_data_2 = list()
        self.series_1.replace(self.original_data_1)
        self.series_2.replace(self.original_data_2)
        self.configuration_reset()
        self.count = 0
        self.constellation_chart_view.updateArrow(0, 0)
        self.remove_marker_lines()
        self.tcpSocket.close()
        self.chart_view1.m_tooltip.hide()
        self.chart_view2.m_tooltip.hide()

        self.chart_view1.update()
        self.chart_view2.update()
        self.constellation_chart_view.update()

    def timer_slot(self):

        if not self.is_stop:
            # self.update_data()
            self.chart_view1.update()
            self.chart_view2.update()
            # self.updateGeometry()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            if self.chart1.isZoomed():
                self.chart1.zoomReset()
                time_min = self.chart1.axisX().min()
                time_max = self.chart1.axisX().max()
                self.chart2.axisX().setRange(time_min, time_max)
            if self.chart2.isZoomed():
                self.chart2.zoomReset()
                time_min = self.chart2.axisX().min()
                time_max = self.chart2.axisX().max()
                self.chart1.axisX().setRange(time_min, time_max)
            self.chart_view1.update()
            self.chart_view2.update()
        super().keyPressEvent(event)

    def remove_marker_lines(self):
        for item in self.chart_view1.marker_lines:
            self.chart_view1.scene().items().remove(item)
        for item in self.chart_view2.marker_lines:
            self.chart_view2.scene().items().remove(item)
        self.chart_view1.marker_lines = list()
        self.chart_view2.marker_lines = list()
        self.chart_view1.update()
        self.chart_view2.update()
        self.table.clearContents()
        self.table.model().removeRows(0, self.table.rowCount())
        self.table.hide()

    # TODO START BUTTON

    def stop_slot(self):
        if self.is_stop:
            # self.udpThread.start()

            if self.tcpSocket.state() == QTcpSocket.ConnectedState:
                print('send start')
                self.tcpSocket.write(b'START')
                self.start_time = time.time()
            # self.timer.start(1)
            self.start_action.setEnabled(False)
            self.stop_action.setEnabled(True)
            # self.start_action.setText('Stop')
            self.start_btn.setText('Stop')
            self.start_btn.setIcon(QIcon("image/stop.png"))
            self.configurations.time_max = self.count if self.count > self.configurations.time_max_range else self.configurations.time_max_range
            self.configurations.time_min = self.configurations.time_max - self.configurations.time_max_range
            self.is_stop = False
            # data1 = self.original_data_1[self.configurations.time_min:self.configurations.time_max]
            # data2 = self.original_data_2[self.configurations.time_min:self.configurations.time_max]
            # self.series_1.replace(data1)
            # self.series_2.replace(data2)
        else:
            # self.udpThread.stopImmediately()
            if self.tcpSocket.state() == QTcpSocket.ConnectedState:
                print('send stop')
                self.tcpSocket.write(b'STOP')
            self.start_action.setEnabled(True)
            self.stop_action.setEnabled(False)
            # self.timer.stop()
            self.start_btn.setIcon(QIcon("image/start.png"))
            self.start_btn.setText('Start')
            # self.start_action.setText('Start')
            self.is_stop = True

    def update_data(self, recv_data):
        self.mag_min = 4096000
        self.mag_max = -4096000
        self.phase_min = 4096000
        self.phase_max = -4096000
        # print(recv_data)
        data_len = len(recv_data)
        data_length = len(self.series_1)
        # print(f"read data {data_len}")
        points_1 = []
        points_2 = []
        self.count = 0
        for i in range(data_len // 4):
            res = struct.unpack('!hh', recv_data[i * 4:i * 4 + 4])
            data_abs = res[0]
            data_phase = res[1]

            # data_abs = data_abs / 4096
            # data_phase = data_phase / 2048

            self.update_range(data_abs, data_phase)
            # self.data_to_show.put((data_abs, data_phase))
            point_1 = QPointF(self.count, data_abs)
            point_2 = QPointF(self.count, data_phase)
            points_1.append(point_1)
            points_2.append(point_2)
            # self.series_1.append(point_1)
            # self.series_2.append(point_2)
            # self.original_data_1.append(point_1)
            # self.original_data_2.append(point_2)
            self.count += 1
        # print(1)
        self.series_1.replace(points_1)
        self.series_2.replace(points_2)
        self.constellation_chart_view.updateArrow(
            self.mag_max if self.mag_max < self.radial_axis.max() else self.radial_axis.max(), self.phase_max)

        # if data_length > self.configurations.time_max_range and not self.is_stop:
        #     self.configurations.time_min += data_len // 4
        #     self.configurations.time_max += data_len // 4
        #     self.chart1.axisX().setRange(self.configurations.time_min, self.configurations.time_max)
        #     self.chart2.axisX().setRange(self.configurations.time_min, self.configurations.time_max)
        # if mag:
        #     self.constellation_chart_view.updateArrow(mag, phase)
        # self.chart_view1.update()
        # self.chart_view2.update()
        # self.zoom_fit_action()
        # print(time.time() - self.start_time)

    def tcp_connect_clicked(self):
        # self.server_ip = ip_auto_detect()
        # self.server_ip = '192.168.137.10'
        print(self.server_ip)
        self.tcpSocket.connectToHost(QHostAddress(self.server_ip), self.port)
        if self.tcpSocket.waitForConnected(1000):
            print('connected')
        else:
            print('Not connected')
        pass

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.tcpSocket.close()
        super().closeEvent(a0)

    def update_axis_range(self, mag_min, mag_max, phase_min, phase_max, time_min, time_max):
        self.chart1.axisX().setRange(time_min, time_max)
        self.chart1.axisY().setRange(mag_min, mag_max)
        self.chart2.axisX().setRange(time_min, time_max)
        self.chart2.axisY().setRange(phase_min, phase_max)
        self.radial_axis.setRange(mag_min, mag_max)


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    icon = QIcon("image/start.png")
    # icon.addPixmap(QPixmap("my.ico"),QIcon.Normal, QIcon.Off)
    gui.setWindowIcon(icon)
    gui.setWindowTitle('Oscilloscope')
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
