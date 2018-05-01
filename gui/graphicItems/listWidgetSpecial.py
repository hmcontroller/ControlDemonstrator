# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class ListWidgetSpecial(QtGui.QListWidget):

    valueSelected = QtCore.pyqtSignal(float)
    closeMe = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ListWidgetSpecial, self).__init__(parent)
        self.itemClicked.connect(self.theItemClicked)

    def theItemClicked(self, item):
        self.valueSelected.emit(float(item.text()))

    def keyPressEvent(self, QKeyEvent):

        if QKeyEvent.key() == QtCore.Qt.Key_Up and self.currentRow() == 0:
            self.closeMe.emit()

        if QKeyEvent.key() == QtCore.Qt.Key_Enter or QKeyEvent.key() == QtCore.Qt.Key_Return:
            self.valueSelected.emit(float(self.currentItem().text()))

        super(ListWidgetSpecial, self).keyPressEvent(QKeyEvent)

    def focusOutEvent(self, *args, **kwargs):
        self.hide()