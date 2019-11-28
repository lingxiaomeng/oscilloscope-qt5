from PyQt5.QtChart import QChartView
from PyQt5.Qt import Qt
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMouseEvent

from callout import Callout


class ChartView(QChartView):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.is_clicking = False
        self.x_old, self.y_old = 0, 0
        self.callout = None

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
            return
        else:
            self.tooltip(event.pos(), True)

    #
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() and event.button() == Qt.LeftButton:
            print('{} {}'.format(event.x(), event.y()))
            self.is_clicking = True
        elif event.button() and event.button() == Qt.RightButton:
            self.chart().zoomReset()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.is_clicking:
            self.x_old, self.y_old = 0, 0
            self.is_clicking = False

    def tooltip(self, point: QPoint, state: bool):
        print("hover")
        if not self.callout:
            self.callout = Callout(self.chart())

        if state:
            self.callout.set_text("X:{} Y:{}".format(point.x(), point.y()))
            self.callout.show()
        else:
            self.callout.hide()
