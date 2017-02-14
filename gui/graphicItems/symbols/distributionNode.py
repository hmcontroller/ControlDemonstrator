# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class DistributionNode(QtGui.QGraphicsItem):
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)
        self.width = 8
        self.height = 8

        self.painterPath = QtGui.QPainterPath()
        self.painterPath.addEllipse(QtCore.QPointF(0, 0), self.width/2, self.height/2)

        self.brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.fillPath(self.painterPath, self.brush)

    def boundingRect(self):
        return QtCore.QRectF(-self.width/2, -self.height/2, self.width/2, self.height/2)

    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height

    @property
    def coordinates(self):
        return self.mapToScene(QtCore.QPoint(0, 0))

