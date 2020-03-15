from PyQt5.QtWidgets import QTableWidgetItem


class QTableWidgetNumItem(QTableWidgetItem):
    def __init__(self, value):
        super().__init__(str(value))
        self.value = value

    def __lt__(self, other):
        if isinstance(other, QTableWidgetNumItem):
            return self.value < other.value
        return super(QTableWidgetItem, self).__lt__(other)
