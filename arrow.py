from PyQt5.QtCore import *
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem


class QArrow(QGraphicsItem):
    def __init__(self, parent):
        super(QArrow, self).__init__()
        self.m_chart = parent
        self.dest = QPointF(1, 1)

    def boundingRect(self) -> QRectF:
        rect = QRectF()
        rect.setLeft(0)
        rect.setRight(500)
        rect.setTop(0)
        rect.setBottom(500)
        return rect

    def updateGeometry(self):
        self.prepareGeometryChange()

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        # setPen
        pen = QPen(Qt.green)
        pen.setWidth(3)
        pen.setJoinStyle(Qt.MiterJoin)
        QPainter.setPen(pen)
        # setBrush
        brush = QBrush()
        brush.setColor(Qt.green)
        brush.setStyle(Qt.SolidPattern)
        QPainter.setBrush(brush)
        source = QPointF(self.mapFromParent(self.m_chart.mapToPosition(QPoint(0, 0))))

        dest = self.mapFromParent(self.m_chart.mapToPosition(self.dest))
        # print(self.dest)
        line = QLineF(source, dest)
        line.setLength(line.length() - 3)

        v = line.unitVector()
        v.setLength(2)
        v.translate(QPointF(line.dx(), line.dy()))

        n = v.normalVector()
        n.setLength(n.length() * 0.5)
        n2 = n.normalVector().normalVector()

        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()

        QPainter.drawLine(line)
        QPainter.drawPolygon(p1, p2, p3)
