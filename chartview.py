# coding:utf-8

from PyQt5.QtChart import QChartView, QAbstractSeries, QChart
from PyQt5.QtCore import QPointF, QRectF, QSizeF, QEvent, Qt, QPoint
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QResizeEvent, QPen, QColor, QPainter, QKeyEvent
from PyQt5.QtWidgets import QHBoxLayout

# from main import MainUi

from callout import Callout
from markerline import MarkerLine


class ChartView(QChartView):
    def __init__(self, *__args, chart: QChart, data: list):
        super().__init__(*__args)
        self.polar_chartview = None
        self.chartview = None
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

    def setChartview(self, chartview: QChartView):
        self.chartview = chartview

    def setPolarChartview(self, chartview: QChartView):
        self.polar_chartview = chartview

    def mouseMoveEvent(self, event: QMouseEvent):
        self.right_clicked = False

        if self.is_clicking:
            if self.x_old == 0 and self.y_old == 0:
                pass
            else:
                x = event.x() - self.x_old
                y = event.y() - self.y_old
                self.chart().scroll(-x, y)
                # self.chartview.chart().scroll(-x, y)
            self.x_old = event.x()
            self.y_old = event.y()
        time_min = self.chart().axisX().min()
        time_max = self.chart().axisX().max()
        self.chartview.chart().axisX().setRange(time_min, time_max)
        self.chartview.update()
        self.update()
        # print('move')
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            x = round(self.chart().mapToValue(event.pos()).x())
            marker = MarkerLine(self.chart())
            marker.m_anchor = QPoint(x, 0)
            marker.setZValue(0)
            marker.setText("%d" % marker.m_anchor.x())
            marker.show()
            self.scene().addItem(marker)
            self.marker_lines.append(marker)
            if self.chart().series()[0]:
                start = self.chart().series()[0].pointsVector()[0].x()
                if len(self.chart().series()[0].pointsVector()) > x - start:
                    y = self.chart().series()[0].at(x - start).y()
                    yb = self.chartview.chart().series()[0].at(x - start).y()
                    if self.objectName() == 'chart1':
                        self.polar_chartview.updateArrow(y, yb)
                    if self.objectName() == 'chart2':
                        self.polar_chartview.updateArrow(yb, y)
        self.update()
        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
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
        self.update()
        super().mouseReleaseEvent(event)
        if self.right_clicked:
            for item in self.marker_lines:
                self.scene().removeItem(item)
            self.marker_lines.clear()
        time_min = self.chart().axisX().min()
        time_max = self.chart().axisX().max()
        self.chartview.chart().axisX().setRange(time_min, time_max)
        self.chartview.update()

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() < 0:
            self.chart().zoom(0.8)
        else:
            self.chart().zoom(1.1)
        super().wheelEvent(event)

    def keep_callout(self):
        self.m_callouts.append(self.m_tooltip)
        self.m_tooltip = Callout(self.chart())
        self.scene().addItem(self.m_tooltip)

    def tooltip(self, point: QPointF, state: bool):
        if not self.m_tooltip:
            self.m_tooltip = Callout(self.chart())
        if state:
            x = round(point.x())
            start = self.chart().series()[0].pointsVector()[0].x()
            y = self.chart().series()[0].at(x - start).y()
            # y2 = self.chart().series()[0].at(x - start + 2).y()
            y1 = self.chart().series()[0].at(x - start + 1).y()

            self.m_tooltip.setText("X: %d \nY: %f" % (x, y))
            self.m_tooltip.m_anchor = point
            self.m_tooltip.setZValue(2)
            if y1 > y:
                self.m_tooltip.adjust = QPointF(10, 70)
            else:
                self.m_tooltip.adjust = QPointF(10, -50)
            self.m_tooltip.update()
            self.m_tooltip.show()
            yb = self.chartview.chart().series()[0].at(x - start).y()
            if self.objectName() == 'chart1':
                self.polar_chartview.updateArrow(y, yb)
            if self.objectName() == 'chart2':
                self.polar_chartview.updateArrow(yb, y)
        else:
            self.m_tooltip.hide()
        self.update()

    def resizeEvent(self, event: QResizeEvent):
        if self.scene():
            self.scene().setSceneRect(QRectF(QPointF(0, 0), QSizeF(event.size())))
            self.chart().resize(QSizeF(event.size()))
            self.update()
        super().resizeEvent(event)

    def addSeries(self, abstractSeries: QAbstractSeries):
        self.chart().addSeries(abstractSeries)
        # abstractSeries.clicked.connect(self.keep_callout)
        abstractSeries.hovered.connect(self.tooltip)
        abstractSeries.setUseOpenGL(True)
