# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class Corner(QtGui.QGraphicsItem):
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        pass

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 1, 1)

    @property
    def coordinates(self):
        return self.mapToScene(QtCore.QPoint(0, 0))


