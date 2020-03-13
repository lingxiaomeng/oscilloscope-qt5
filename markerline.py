import typing

from PyQt5.Qt import Qt
from PyQt5.QtChart import QChart, QAbstractAxis, QValueAxis
from PyQt5.QtCore import QRectF, QPointF, QRect
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QColor, QFontMetrics
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem
import math


class MarkerLine(QGraphicsItem):

    def __init__(self, parent: QChart):
        super().__init__()
        self.m_chart = parent
        self.m_text = ''
        self.m_anchor = QPointF()
        self.m_font = QFont()
        self.m_textRect = QRectF()
        self.m_rect = QRectF()

    def setText(self, text: str):
        self.m_text = text
        metrics = QFontMetrics(self.m_font)
        self.m_textRect = QRectF(metrics.boundingRect(QRect(0, 0, 150, 150), Qt.AlignLeft, self.m_text))
        self.m_textRect.translate(5, 5)
        self.prepareGeometryChange()
        self.m_rect = QRectF(self.m_textRect.adjusted(-5, -5, 5, 5))
        self.updateGeometry()

    def updateGeometry(self):
        self.prepareGeometryChange()
        self.setPos(self.m_chart.mapToPosition(self.m_anchor) + QPointF(10, -50))

    def boundingRect(self) -> QRectF:
        xmin = self.m_chart.axisX().min()
        xmax = self.m_chart.axisX().max()
        ymin = self.m_chart.axisY().min()
        ymax = self.m_chart.axisY().max()

        original_point = QPointF(self.mapFromParent(self.m_chart.mapToPosition(QPointF(xmin, ymin))))
        far_point = QPointF(self.mapFromParent(self.m_chart.mapToPosition(QPointF(xmax, ymax))))
        start_point = QPointF(self.mapFromParent(self.m_chart.mapToPosition(QPointF(self.m_anchor.x(), ymax))))
        end_point = QPointF(self.mapFromParent(self.m_chart.mapToPosition(QPointF(self.m_anchor.x(), ymin))))

        from_parent = self.mapFromParent(self.m_chart.mapToPosition(self.m_anchor))
        anchor = QPointF(from_parent)
        rect = QRectF()
        rect.setLeft(max(min(self.m_rect.left(), anchor.x()), original_point.x()))
        rect.setRight(min(max(self.m_rect.right(), anchor.x()), far_point.x()))
        rect.setTop(start_point.y() - 20)
        rect.setBottom(end_point.y())
        return rect

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
        start_point = QPointF(self.mapFromParent(self.m_chart.mapToPosition(QPointF(self.m_anchor.x(), self.m_chart.axisY().max()))))
        end_point = QPointF(self.mapFromParent(self.m_chart.mapToPosition(QPointF(self.m_anchor.x(), self.m_chart.axisY().min()))))

        path = QPainterPath()
        mr = self.m_rect
        path.addRoundedRect(mr, 5, 5)
        anchor = QPointF(self.mapFromParent(self.m_chart.mapToPosition(self.m_anchor)))
        painter.setPen(QColor('green'))
        painter.setBrush(QColor('green'))
        # painter.drawPath(path)
        # painter.drawText(self.m_textRect, self.m_text)
        painter.drawLine(start_point, end_point)
        painter.drawText(start_point.x(), start_point.y() - 10, '%.4f' % (self.m_anchor.x()))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        event.setAccepted(True)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if event.buttons() & Qt.LeftButton:
            self.setPos(self.mapToParent(event.pos() - event.buttonDownPos(Qt.LeftButton)))
            event.setAccepted(True)
        else:
            event.setAccepted(False)
