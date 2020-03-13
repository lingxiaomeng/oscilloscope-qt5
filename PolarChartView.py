# coding:utf-8

from PyQt5.Qt import Qt
from PyQt5.QtChart import QChartView, QAbstractSeries, QChart, QPolarChart
from PyQt5.QtCore import QPointF, QRectF, QSizeF, QEvent, QPoint
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QResizeEvent, QPen, QColor, QPainter
from PyQt5.QtWidgets import QHBoxLayout

# from main import MainUi
from arrow import QArrow
from callout import Callout
from markerline import MarkerLine


class PolarChartView(QChartView):
    def __init__(self, *__args, chart: QChart):
        super().__init__(*__args)
        self.m_callouts = list()
        self.setChart(chart)
        self.setMouseTracking(True)
        self.right_clicked = False
        self.setRenderHint(QPainter.Antialiasing)
        self.arrow = None
        # self.arrow = QArrow(chart)
        # self.scene().addItem(self.arrow)
        self.x = 0
        self.y = 0

    def updateGeometry(self) -> None:
        if self.arrow:
            self.arrow.updateGeometry()
        super().updateGeometry()

    def updateArrow(self, mag, phase):
        # phase_max = self.chart().axisX().max()
        # mag_max = self.chart().axisY().max()

        self.x = phase
        self.y = mag
        if self.arrow:
            self.arrow.dest = QPointF(self.x, self.y)
            self.updateGeometry()
        else:
            self.arrow = QArrow(self.chart())
            self.arrow.dest = QPointF(self.x, self.y)
            self.scene().addItem(self.arrow)
            self.arrow.show()

    def resizeEvent(self, event: QResizeEvent):
        if self.scene():
            self.scene().setSceneRect(QRectF(QPointF(0, 0), QSizeF(event.size())))
            self.chart().resize(QSizeF(event.size()))
            self.updateGeometry()
        super().resizeEvent(event)

    def addSeries(self, abstractSeries: QAbstractSeries):
        self.chart().addSeries(abstractSeries)
        # abstractSeries.clicked.connect(self.keep_callout)
        abstractSeries.setUseOpenGL(True)
