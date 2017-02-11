# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class Switch(QtGui.QGraphicsObject):

    valueChanged = QtCore.pyqtSignal(float)

    def __init__(self):
        QtGui.QGraphicsObject.__init__(self)

        self.setAcceptHoverEvents(True)
        self.showBoundingRect = False

        # TODO use Qt standard coordinates
        self.bounds = [-20, -20, 50, 20]
        self.height = 30
        self.value = 1.0
        self.brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))

        self.normalPen = QtGui.QPen()
        self.normalPen.setColor(QtGui.QColor(0, 0, 0))
        self.normalPen.setCosmetic(True)
        self.normalPen.setWidth(2)

        self.dottedPen = QtGui.QPen()
        self.dottedPen.setStyle(QtCore.Qt.DashLine)
        self.dottedPen.setCosmetic(True)
        self.dottedPen.setWidth(1)

        self.dotsPath = QtGui.QPainterPath()
        self.dotsPath.addEllipse(QtCore.QPointF(0, 0), 3, 3)
        self.dotsPath.addEllipse(QtCore.QPointF(30, 0), 3, 3)
        self.dotsPath.setFillRule(QtCore.Qt.WindingFill)

        self.fixedLines = QtGui.QPainterPath()
        self.fixedLines.moveTo(-10, 0)
        self.fixedLines.lineTo(0, 0)
        self.fixedLines.moveTo(30, 0)
        self.fixedLines.lineTo(40, 0)

        self.switchClosedPath = QtGui.QPainterPath()
        self.switchClosedPath.moveTo(0, 0)
        self.switchClosedPath.lineTo(30, 0)

        self.switchOpenedPath = QtGui.QPainterPath()
        self.switchOpenedPath.moveTo(0, 0)
        self.switchOpenedPath.lineTo(23, -15)

        self.boundingRectPath = QtGui.QPainterPath()
        self.boundingRectPath.moveTo(self.bounds[0], self.bounds[1])
        self.boundingRectPath.lineTo(self.bounds[2], self.bounds[1])
        self.boundingRectPath.lineTo(self.bounds[2], self.bounds[3])
        self.boundingRectPath.lineTo(self.bounds[0], self.bounds[3])
        self.boundingRectPath.closeSubpath()

        self.boundingRectBrush = QtGui.QBrush(QtGui.QColor(200, 200, 200))

    def getSwitchInCoordinates(self):
        return self.mapToScene(QtCore.QPointF(-10, 0))

    def getSwitchOutCoordinates(self):
        return self.mapToScene(QtCore.QPointF(40, 0))

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)

        if self.showBoundingRect is True:
            QPainter.setPen(self.dottedPen)
            QPainter.drawPath(self.boundingRectPath)
            QPainter.fillPath(self.boundingRectPath, self.boundingRectBrush)

        QPainter.fillPath(self.dotsPath, self.brush)

        QPainter.setPen(self.normalPen)
        QPainter.drawPath(self.fixedLines)

        if self.value <0.5:
            QPainter.drawPath(self.switchOpenedPath)
        else:
            QPainter.drawPath(self.switchClosedPath)


    def boundingRect(self):
        return QtCore.QRectF(self.bounds[0], self.bounds[1], self.bounds[2] - self.bounds[0], self.bounds[3] - self.bounds[1])

    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height

    def setOn(self, value):
        self.value = value
        self.valueChanged.emit(self.value)

    @QtCore.pyqtSlot()
    def confirmationTimeOut(self):
        print "hello switch timeOut"

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        if self.value > 0.5:
            self.setOn(0.0)
        else:
            self.setOn(1.0)
        QtGui.QGraphicsItem.mousePressEvent(self, QGraphicsSceneMouseEvent)

    def hoverEnterEvent(self, QGraphicsSceneMouseEvent):
        self.showBoundingRect = True
        QtGui.QGraphicsItem.hoverEnterEvent(self, QGraphicsSceneMouseEvent)

    def hoverLeaveEvent(self, QGraphicsSceneMouseEvent):
        self.showBoundingRect = False
        QtGui.QGraphicsItem.hoverLeaveEvent(self, QGraphicsSceneMouseEvent)

