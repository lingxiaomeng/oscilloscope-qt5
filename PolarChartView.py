# coding:utf-8

from PyQt5.QtChart import QChartView, QAbstractSeries, QChart
from PyQt5.QtCore import QPointF, QRectF, QSizeF
from PyQt5.QtGui import QResizeEvent, QPainter

# from main import MainUi
from arrow import QArrow


class PolarChartView(QChartView):
    def __init__(self, *__args, chart: QChart):
        super().__init__(*__args)
        self.m_callouts = list()
        self.setChart(chart)
        self.setMouseTracking(True)
        self.right_clicked = False
        self.setRenderHint(QPainter.Antialiasing)
        self.arrow = QArrow(chart)
        self.scene().addItem(self.arrow)
        self.x = 0
        self.y = 0

    def update(self) -> None:
        self.arrow.update()
        super().update()

    def updateArrow(self, mag, phase):
        self.chart().setTitle("Magnitude:%.4f  Phase:%8f" % (mag, phase))

        self.x = phase
        self.y = mag
        self.arrow.dest = QPointF(self.x, self.y)
        self.update()

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
