# coding:utf-8
from PyQt5.Qt import Qt
from PyQt5.QtChart import QChartView
from PyQt5.QtGui import QMouseEvent, QFont, QWheelEvent
from PyQt5.QtWidgets import QLabel, QLayout, QGridLayout, QHBoxLayout


# from main import MainUi


class ChartView1(QChartView):
    def __init__(self, *__args, ui):
        super().__init__(*__args)
        self.ui = ui
        self.is_clicking = False
        self.x_old, self.y_old = 0, 0
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.callout = QLabel("")

        self.callout.setFont(QFont("Microsoft YaHei", 10, QFont.Bold, True))
        self.callout.setGeometry(0, 0, 0, 0)

        self.layout.addChildWidget(self.callout)


    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_clicking:
            if self.x_old == 0 and self.y_old == 0:
                pass
            else:
                x = event.x() - self.x_old
                y = event.y() - self.y_old
                self.chart().scroll(-x, y)
            self.x_old = event.x()
            self.y_old = event.y()
        else:
            x = event.x()
            y = event.y()
            x_max = (self.chart().axisX().max())
            x_min = (self.chart().axisX().min())

            y_max = (self.chart().axisY().max())
            y_min = (self.chart().axisY().min())
            print(y)
            index = int((x - 90) / (765 / (x_max - x_min)) + x_min)
            y = (y - 35) / (200 / (y_max - y_min))
            y = y_max - y
            if index < len(self.ui.original_data_1):
                y1 = self.ui.original_data_1[index].y()
                if abs(y1 - y) < 2 and 85 < x < 856:
                    self.callout.setText("    x:%d, y:%.4f" % (int(index), y1))
                    self.callout.setGeometry(event.x(), event.y(), 220, 20)
                else:
                    self.callout.setText("")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() and event.button() == Qt.LeftButton:
            self.is_clicking = True
        elif event.button() and event.button() == Qt.RightButton:
            self.chart().zoomReset()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.is_clicking:
            self.x_old, self.y_old = 0, 0
            self.is_clicking = False
        self.callout.setText("")

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() < 0:
            self.chart().zoom(0.8)
        else:
            self.chart().zoom(1.1)


class ChartView2(QChartView):
    def __init__(self, *__args, ui):
        super().__init__(*__args)
        self.ui = ui
        self.is_clicking = False
        self.x_old, self.y_old = 0, 0
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.xy_label = QLabel("")
        self.callout = QLabel("")

        self.callout.setFont(QFont("Microsoft YaHei", 10, QFont.Bold, True))
        self.callout.setGeometry(0, 0, 0, 0)
        self.xy_label.setFont(QFont("Microsoft YaHei", 10, QFont.Bold, True))
        self.xy_label.setGeometry(330, 310, 300, 20)

        self.layout.addChildWidget(self.callout)
        self.layout.addChildWidget(self.xy_label)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_clicking:
            if self.x_old == 0 and self.y_old == 0:
                pass
            else:
                x = event.x() - self.x_old
                y = event.y() - self.y_old
                self.chart().scroll(-x, y)
            self.x_old = event.x()
            self.y_old = event.y()
        else:
            x = event.x()
            y = event.y()
            x_max = (self.chart().axisX().max())
            x_min = (self.chart().axisX().min())

            y_max = (self.chart().axisY().max())
            y_min = (self.chart().axisY().min())
            print(y)
            index = int((x - 90) / (765 / (x_max - x_min)) + x_min)
            y = (y - 35) / (200 / (y_max - y_min))
            y = y_max - y
            if index < len(self.ui.original_data_1):
                y1 = self.ui.original_data_2[index].y()
                y2 = self.ui.original_data_2[index].y()
                if abs(y2 - y) < 2 and 85 < x < 856:
                    self.callout.setText("    x:%d, y:%.4f" % (int(index), y2))
                    self.xy_label.setText("x:%d, Data1:%.8f, Data2:%.8f" % (int(index), y1, y2))
                    self.callout.setGeometry(event.x(), event.y(), 220, 20)
                else:
                    self.callout.setText("")
                    self.xy_label.setText("")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() and event.button() == Qt.LeftButton:
            self.is_clicking = True
        elif event.button() and event.button() == Qt.RightButton:
            self.chart().zoomReset()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.is_clicking:
            self.x_old, self.y_old = 0, 0
            self.is_clicking = False
        self.callout.setText("")

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() < 0:
            self.chart().zoom(0.8)
        else:
            self.chart().zoom(1.1)
