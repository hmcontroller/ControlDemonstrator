# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore

from gui.constants import *

class Switch(QtGui.QGraphicsObject):

    valueChanged = QtCore.pyqtSignal(float)

    def __init__(self, command):
        QtGui.QGraphicsObject.__init__(self)

        self.command = command

        self.setAcceptHoverEvents(True)
        self.showBoundingRect = False

        self.showConfirmationFailure = True
        self.warningBrush = QtGui.QBrush(CONFIRMATION_WARNING_COLOR)

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

        self.boundingRectBrush = QtGui.QBrush(HOVER_COLOR)

        self.confirmationWarningTimer = QtCore.QTimer()
        self.confirmationWarningTimer.setSingleShot(False)
        self.confirmationWarningTimer.timeout.connect(self.toggleConfirmationFailureIndication)
        self.confirmationWarningBlinkInterval = 200
        self.confirmationWarningTimer.start(self.confirmationWarningBlinkInterval)

        self.setValue(self.command.value)
        self.valueChanged.connect(self.command.setValue)
        self.command.confirmationTimeOut.connect(self.confirmationTimeOut)
        self.command.confirmation.connect(self.confirmation)


    @property
    def inCoordinates(self):
        return self.mapToScene(QtCore.QPointF(-10, 0))

    @property
    def outCoordinates(self):
        return self.mapToScene(QtCore.QPointF(40, 0))

    def confirmationTimeOut(self):
        self.isCommandConfirmed = False
        self.confirmationWarningTimer.start(self.confirmationWarningBlinkInterval)

    def confirmation(self):
        self.confirmationWarningTimer.stop()
        self.isCommandConfirmed = True
        self.showConfirmationFailure = False

    def toggleConfirmationFailureIndication(self):
        self.showConfirmationFailure = not self.showConfirmationFailure

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)

        if self.showBoundingRect is True:
            QPainter.setPen(self.dottedPen)
            QPainter.drawPath(self.boundingRectPath)
            QPainter.fillPath(self.boundingRectPath, self.boundingRectBrush)

        if self.showConfirmationFailure is True:
            QPainter.fillPath(self.boundingRectPath, self.warningBrush)

        # draw dots
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

    def setValue(self, value):
        self.value = value
        self.valueChanged.emit(self.value)

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        if self.value > 0.5:
            self.setValue(0.0)
        else:
            self.setValue(1.0)
        QtGui.QGraphicsItem.mousePressEvent(self, QGraphicsSceneMouseEvent)

    def hoverEnterEvent(self, QGraphicsSceneMouseEvent):
        self.showBoundingRect = True
        QtGui.QGraphicsItem.hoverEnterEvent(self, QGraphicsSceneMouseEvent)

    def hoverLeaveEvent(self, QGraphicsSceneMouseEvent):
        self.showBoundingRect = False
        QtGui.QGraphicsItem.hoverLeaveEvent(self, QGraphicsSceneMouseEvent)

