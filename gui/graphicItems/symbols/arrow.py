# -*- encoding: utf-8 -*-

import math

from PyQt4 import QtGui, QtCore


class Arrow(QtGui.QGraphicsItem):
    def __init__(self, absStart, absEnd):
        QtGui.QGraphicsItem.__init__(self)

        # self.end = end

        angle = 0
        if absStart.x() == absEnd.x():
            if absStart.y() < absEnd.y():
                angle = 90
            elif absStart.y() > absEnd.y():
                angle = 270
        elif absStart.y() == absEnd.y():
            if absStart.x() < absEnd.x():
                angle = 0
            elif absStart.x() > absEnd.x():
                angle = 180
        else:
            angle = math.atan(  (absEnd.y() - absStart.y()) / (absEnd.x() - absStart.x()) ) * 180 / math.pi
            if absStart.x() > absEnd.x():
                angle = angle + 180


        self.relativeEndPoint = QtCore.QPointF(absEnd.x() - absStart.x() , absEnd.y() - absStart.y())

        self.lineStartPoint = QtCore.QPointF(0, 0)

        intermediateEndX = self.relativeEndPoint.x() - 15 * math.cos(angle * math.pi / 180)
        intermediateEndY = self.relativeEndPoint.y() - 15 * math.sin(angle * math.pi / 180)

        self.lineEndPoint = QtCore.QPointF(intermediateEndX, intermediateEndY)

        self.linePath = QtGui.QPainterPath()
        self.linePath.moveTo(0, 0)
        self.linePath.lineTo(self.lineEndPoint)

        self.arrowHead = ArrowHead(self)
        self.arrowHead.setPos(self.lineEndPoint)
        self.arrowHead.rotate(angle)

        self.pen = QtGui.QPen()
        self.pen.setWidth(2)
        self.pen.setCosmetic(True)


    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.setPen(self.pen)
        QPainter.drawPath(self.linePath)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 10)

    def setFillColor(self, color):
        self.arrowHead.setFillColor(color)

    @property
    def inCoordinates(self):
        return self.mapToScene(QtCore.QPoint(0, 0))

    @property
    def outCoordinates(self):
        return self.mapToScene(self.relativeEndPoint)



class ArrowHead(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self.painterPath = QtGui.QPainterPath()


        self.painterPath.moveTo(0, -3)
        self.painterPath.lineTo(15, 0)
        self.painterPath.lineTo(0, 3)
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

    @property
    def inCoordinates(self):
        return self.mapToScene(QtCore.QPoint(0, 0))

    @property
    def outCoordinates(self):
        return self.mapToScene(QtCore.QPoint(20, 0))
