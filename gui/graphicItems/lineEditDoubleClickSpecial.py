# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class LineEditDoubleClickSpecial(QtGui.QLineEdit):

    lostFocus = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(LineEditDoubleClickSpecial, self).__init__(parent)
        self.oldValueText = None

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.selectAll()

    # def focusInEvent(self, QFocusEvent):
    #     print "focus in in LineEditClass"
    #     self.oldValueText = self.text()
    #     super(LineEditDoubleClickSpecial, self).focusInEvent(QFocusEvent)
    #
    # def focusOutEvent(self, QFocusEvent):
    #     print "focus out in LineEditClass"
    #     super(LineEditDoubleClickSpecial, self).focusOutEvent(QFocusEvent)
    #     self.lostFocus.emit()