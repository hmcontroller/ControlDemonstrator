# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class Arrow(QtGui.QGraphicsItem):
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)
        self.painterPath = QtGui.QPainterPath()
        self.painterPath.moveTo(-5, -5)
        self.painterPath.lineTo(20, 0)
        self.painterPath.lineTo(-5, 5)
        self.painterPath.lineTo(0, 0)
        self.painterPath.closeSubpath()
        self.painterPath.setFillRule(QtCore.Qt.WindingFill)
        self.brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.fillPath(self.painterPath, self.brush)
        #QPainter.drawPath(self.painterPath)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 10)

    def setFillColor(self, color):
        self.brush.setColor(color)
        self.update()

