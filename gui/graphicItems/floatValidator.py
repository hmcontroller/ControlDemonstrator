# -*- encoding: utf-8 -*-
import re

from PyQt4 import QtGui, QtCore


class FloatValidator(QtGui.QDoubleValidator):

    valueAboveLimit = QtCore.pyqtSignal(float)
    valueBelowLimit = QtCore.pyqtSignal(float)

    def __init__(self):
        super(FloatValidator, self).__init__()
        expression = ur"\A[-]{0,1}\d{0,}[\.,]{0,1}\d{0,}\Z"
        self.expression = re.compile(expression)

    def validate(self, qString, p_int):
        text = unicode(qString)



        if text == u"":
            return QtGui.QValidator.Acceptable, p_int

        if self.expression.search(text):
            return QtGui.QValidator.Acceptable, p_int
        else:
            return QtGui.QValidator.Invalid, p_int

