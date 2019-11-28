from PyQt5.QtChart import QChart
from PyQt5.QtCore import QRectF, QPoint, QPointF, Qt, QRect, qAbs
from PyQt5.QtGui import QFont, QPainter, QFontMetrics, QPainterPath, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem


class Callout(QGraphicsItem):
    def __init__(self, chart: QChart):
        super().__init__(chart)
        self.chart = chart
        self.rect = QRectF()
        self.point = QPoint()
        self.font = QFont()
        self.textRect = QRectF()
        self.anchor = QPointF
        self.text = ""

    def set_text(self, text):
        self.text = text
        metrics = QFontMetrics(text)
        self.textRect = metrics.boundingRect(QRect(0, 0, 150, 150), Qt.AlignLeft, self.text)
        self.textRect.translate(5, 5)
        self.prepareGeometryChange()
        self.rect = self.textRect.adjusted(-5, -5, 5, 5)

    def setAnchor(self, point: QPoint):
        self.anchor = point

    def updateGeometry(self):
        self.prepareGeometryChange()
        self.setPos(self.chart.mapToPosition(self.anchor) + QPoint(10, -50))

    def boundingRect(self):
        anchor = self.mapFromParent(self.chart.mapToPosition(self.anchor))
        rect = QRectF()
        rect.setLeft(min(self.rect.left(), anchor.x()))
        rect.setRight(max(self.rect.right(), anchor.x()))
        rect.setTop(min(self.rect.top(), anchor.y()))
        rect.setBottom(max(self.rect.bottom(), anchor.y()))
        return rect

    def paint(self, painter: QPainter, item: QStyleOptionGraphicsItem, widget=None):
        # Q_UNUSED(option)
        # Q_UNUSED(widget)
        path =QPainterPath()
        path.addRoundedRect(self.rect, 5, 5)
        anchor = self.mapFromParent(self.chart.mapToPosition(self.anchor))
        if not self.rect.contains(anchor):
            point1, point2 = QPoint(), QPoint
            above = anchor.y() <= self.rect.top()
            aboveCenter = self.rect.top() < anchor.y() <= self.rect.center().y()
            belowCenter = self.rect.center().y() < anchor.y() <= self.rect.bottom()
            below = anchor.y() > self.rect.bottom()

            onLeft = anchor.x() <= self.rect.left()
            leftOfCenter = self.rect.left() < anchor.x() <= self.rect.center().x()
            rightOfCenter = self.rect.center().x() < anchor.x() <= self.rect.right()
            onRight = anchor.x() > self.rect.right()

            x = (onRight + rightOfCenter) * self.rect.width()
            y = (below + belowCenter) * self.rect.height()
            cornerCase = (above and onLeft) or (above and onRight) or (below and onLeft) or (below and onRight)
            vertical = qAbs(anchor.x() - x) > qAbs(anchor.y() - y)

            x1 = x + leftOfCenter * 10 - rightOfCenter * 20 + cornerCase * (not vertical) * (onLeft * 10 - onRight * 20)
            y1 = y + aboveCenter * 10 - belowCenter * 20 + cornerCase * vertical * (above * 10 - below * 20)
            point1.setX(x1)
            point1.setY(y1)

            x2 = x + leftOfCenter * 20 - rightOfCenter * 10 + cornerCase * (not vertical) * (onLeft * 20 - onRight * 10)
            y2 = y + aboveCenter * 20 - belowCenter * 10 + cornerCase * vertical * (above * 20 - below * 10)
            point2.setX(x2)
            point2.setY(y2)

            path.moveTo(point1)
            path.lineTo(anchor)
            path.lineTo(point2)
            path = path.simplified()

        painter.setBrush(QColor(255, 255, 255))
        painter.drawPath(path)
        painter.drawText(self.textRect, self.text)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        event.setAccepted(True)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() and event.button() == Qt.LeftButton:
            self.setPos(self.mapToParent(event.pos() - event.buttonDownPos(Qt.LeftButton)))
            event.setAccepted(False)
        else:
            event.setAccepted(True)
