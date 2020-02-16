# import sys
# from typing import List
#
# from PyQt5.QtChart import QSplineSeries, QLineSeries, QChart
# from PyQt5.QtCore import QPointF, QRectF, QSizeF, Qt
# from PyQt5.QtGui import QResizeEvent, QMouseEvent, QPainter
# from PyQt5.QtWidgets import QApplication, QGraphicsSimpleTextItem, QGraphicsScene, QGraphicsView
#
# from callout import Callout
#
#
# class View(QGraphicsView):
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.m_callouts = List[Callout]
#         self.setDragMode(QGraphicsView.NoDrag)
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#
#         # chart
#         self.m_chart = QChart(parent)
#         self.m_chart.setMinimumSize(640, 480)
#         self.m_chart.setTitle("Hover the line to show callout. Click the line to make it stay")
#         self.m_chart.legend().hide()
#         series = QLineSeries()
#         series.append(1, 3)
#         series.append(4, 5)
#         series.append(5, 4.5)
#         series.append(7, 1)
#         series.append(11, 2)
#         self.m_chart.addSeries(series)
#
#
#         series2 = QSplineSeries()
#         series2.append(1.6, 1.4)
#         series2.append(2.4, 3.5)
#         series2.append(3.7, 2.5)
#         series2.append(7, 4)
#         series2.append(10, 2)
#         self.m_chart.addSeries(series2)
#
#         self.m_chart.createDefaultAxes()
#         self.m_chart.setAcceptHoverEvents(True)
#
#         self.setRenderHint(QPainter.Antialiasing)
#
#         self.setScene(QGraphicsScene())
#         self.scene().addItem(self.m_chart)
#
#         self.m_coordX = QGraphicsSimpleTextItem(self.m_chart)
#         self.m_coordX.setPos(self.m_chart.size().width() / 2 - 50, self.m_chart.size().height() - 20)
#         self.m_coordX.setText("X: ")
#         self.m_coordY = QGraphicsSimpleTextItem(self.m_chart)
#         self.m_coordY.setPos(self.m_chart.size().width() / 2 + 50, self.m_chart.size().height() - 20)
#         self.m_coordY.setText("Y: ")
#
#         self.m_tooltip = Callout(self.m_chart)
#         self.scene().addItem(self.m_tooltip)
#
#         series.clicked.connect(self.keep_callout)
#         series.hovered.connect(self.tooltip)
#         series2.clicked.connect(self.keep_callout)
#         series2.hovered.connect(self.tooltip)
#
#         self.setMouseTracking(True)
#
#     def resizeEvent(self, event: QResizeEvent):
#         if self.scene():
#             self.scene().setSceneRect(QRectF(QPointF(0, 0), QSizeF(event.size())))
#             self.m_chart.resize(QSizeF(event.size()))
#             self.m_coordX.setPos(self.m_chart.size().width() / 2 - 50, self.m_chart.size().height() - 20)
#             self.m_coordY.setPos(self.m_chart.size().width() / 2 + 50, self.m_chart.size().height() - 20)
#
#             for callout in self.m_callouts:
#                 callout.updateGeometry()
#
#         super().resizeEvent(event)
#
#     def mouseMoveEvent(self, event: QMouseEvent):
#         from_chart = self.m_chart.mapToValue(event.pos())
#         self.m_coordX.setText("X: "+str(from_chart.x()))
#         self.m_coordX.setText("Y: "+str(from_chart.y()))
#         super().mouseMoveEvent(event)
#
#     def keep_callout(self):
#         self.m_callouts.append(self.m_tooltip)
#         self.m_tooltip = Callout(self.m_chart)
#         self.scene().addItem(self.m_tooltip)
#
#     def tooltip(self, point: QPointF, state: bool):
#         if not self.m_tooltip:
#             self.m_tooltip = Callout(self.m_chart)
#         # print("hovered")
#         if state:
#
#             self.m_tooltip.setText("X: %d \nY: %d" % (point.x(), point.y()))
#             self.m_tooltip.m_anchor = point
#             self.m_tooltip.setZValue(11)
#             self.m_tooltip.updateGeometry()
#             self.m_tooltip.show()
#             # print("state")
#         else:
#             self.m_tooltip.hide()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = View()
#     window.resize(640, 480)
#     window.show()
#     sys.exit(app.exec_())
