# coding:utf-8

from PyQt5.Qt import Qt
from PyQt5.QtChart import QChartView, QAbstractSeries, QChart
from PyQt5.QtCore import QPointF, QRectF, QSizeF
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QResizeEvent
from PyQt5.QtWidgets import QHBoxLayout

# from main import MainUi
from callout import Callout


class ChartView(QChartView):
    def __init__(self, *__args,chart:QChart):
        super().__init__(*__args)
        self.m_callouts = list()
        self.setChart(chart)
        self.is_clicking = False
        self.x_old, self.y_old = 0, 0
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.callout = Callout(self.chart())
        self.m_tooltip = Callout(self.chart())
        self.m_tooltip.hide()
        self.scene().addItem(self.m_tooltip)
        self.setMouseTracking(True)

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
        super().mouseMoveEvent(event)


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

    def keep_callout(self):
        self.m_callouts.append(self.m_tooltip)
        self.m_tooltip = Callout(self.chart())
        self.scene().addItem(self.m_tooltip)

    def tooltip(self, point: QPointF, state: bool):
        if not self.m_tooltip:
            self.m_tooltip = Callout(self.chart())
        print("hovered")
        if state:
            self.m_tooltip.setText("X: %d \nY: %d" % (point.x(), point.y()))
            self.m_tooltip.m_anchor = point
            self.m_tooltip.setZValue(11)
            self.m_tooltip.updateGeometry()
            self.m_tooltip.show()

        else:
            self.m_tooltip.hide()

    def resizeEvent(self, event: QResizeEvent):
        if self.scene():
            self.scene().setSceneRect(QRectF(QPointF(0, 0), QSizeF(event.size())))
            self.chart().resize(QSizeF(event.size()))

            for callout in self.m_callouts:
                callout.updateGeometry()

        super().resizeEvent(event)

    def addSeries(self, qAbstractSeries: QAbstractSeries):
        self.chart().addSeries(qAbstractSeries)
        qAbstractSeries.clicked.connect(self.keep_callout)
        qAbstractSeries.hovered.connect(self.tooltip)
