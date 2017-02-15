# -*- encoding: utf-8 -*-
from PyQt4 import QtGui


class LineEditDoubleClickSpecial(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(LineEditDoubleClickSpecial, self).__init__(parent)

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.selectAll()