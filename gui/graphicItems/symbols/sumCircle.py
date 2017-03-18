# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class SumCircle(QtGui.QGraphicsItem):
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)
        self.width = 30
        self.height = 30

        self.painterPath = QtGui.QPainterPath()
        self.painterPath.addEllipse(QtCore.QPointF(0, 0), self.width/2, self.height/2)

        self.pen = QtGui.QPen()
        self.pen.setWidth(2)
        self.pen.setCosmetic(True)


    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.setPen(self.pen)
        QPainter.drawPath(self.painterPath)

    def boundingRect(self):
        return QtCore.QRectF(-self.width/2, -self.height/2, self.width, self.height)

    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height

    @property
    def northCoordinates(self):
        return self.mapToScene(QtCore.QPoint(0, -self.height/2))

    @property
    def westCoordinates(self):
        return self.mapToScene(QtCore.QPoint(-self.width/2, 0))

    @property
    def southCoordinates(self):
        return self.mapToScene(QtCore.QPoint(0, self.height/2))

    @property
    def eastCoordinates(self):
        return self.mapToScene(QtCore.QPoint(self.width/2, 0))


