# coding:utf-8

from PyQt5.Qt import Qt
from PyQt5.QtChart import QChartView, QAbstractSeries, QChart
from PyQt5.QtCore import QPointF, QRectF, QSizeF, QEvent
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QResizeEvent, QPen, QColor, QPainter
from PyQt5.QtWidgets import QHBoxLayout

# from main import MainUi

from callout import Callout
from markerline import MarkerLine


class ChartView(QChartView):
    def __init__(self, *__args, chart: QChart, data: list):
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
        self.data = data
        self.setRubberBand(QChartView.RectangleRubberBand)
        self.right_clicked = False
        self.setRenderHint(QPainter.Antialiasing)
        self.marker_lines = list()

    def updateGeometry(self) -> None:
        for callout in self.m_callouts:
            callout.updateGeometry()
        for marker in self.marker_lines:
            marker.updateGeometry()
        self.chart().updateGeometry()
        # self.scene().update()

        # QAbstractSeries.setUseOpenGL()
        super().updateGeometry()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.right_clicked = False

        if self.is_clicking:
            if self.x_old == 0 and self.y_old == 0:
                pass
            else:
                x = event.x() - self.x_old
                y = event.y() - self.y_old
                self.chart().scroll(-x, y)
            self.x_old = event.x()
            self.y_old = event.y()
        self.updateGeometry()
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            marker = MarkerLine(self.chart())
            marker.m_anchor = self.chart().mapToValue(event.pos())
            marker.setZValue(11)
            marker.setText(str(marker.m_anchor.x()))
            marker.updateGeometry()
            marker.show()
            self.scene().addItem(marker)
            self.marker_lines.append(marker)
        else:
            for item in self.marker_lines:
                self.scene().removeItem(item)
            self.marker_lines.clear()
            self.updateGeometry()
        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        # print(self.mapFromParent(event.pos()))
        if event.button() and event.button() == Qt.LeftButton:
            self.is_clicking = True
            event = QMouseEvent(QEvent.MouseButtonPress, event.pos(), Qt.RightButton, Qt.RightButton, Qt.NoModifier)
        elif event.button() and event.button() == Qt.RightButton:
            event = QMouseEvent(QEvent.MouseButtonPress, event.pos(), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
            self.right_clicked = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.is_clicking:
            self.x_old, self.y_old = 0, 0
            self.is_clicking = False
            # event = QMouseEvent(QEvent.MouseButtonPress, event.pos(), Qt.RightButton, Qt.RightButton, Qt.NoModifier)
        else:
            event = QMouseEvent(QEvent.MouseButtonPress, event.pos(), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        if self.right_clicked:
            self.chart().zoomReset()
        # self.callout.setText("")
        self.updateGeometry()
        super().mouseReleaseEvent(event)

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
        if state:
            x = round(point.x())
            # y = self.data[x].y()
            start = self.chart().series()[0].pointsVector()[0].x()
            y = self.chart().series()[0].at(x - start).y()
            self.m_tooltip.setText("X: %d \nY: %f" % (x, y))
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

            self.updateGeometry()
        super().resizeEvent(event)

    def addSeries(self, abstractSeries: QAbstractSeries):
        self.chart().addSeries(abstractSeries)
        # abstractSeries.clicked.connect(self.keep_callout)
        abstractSeries.hovered.connect(self.tooltip)
        abstractSeries.setUseOpenGL(True)
