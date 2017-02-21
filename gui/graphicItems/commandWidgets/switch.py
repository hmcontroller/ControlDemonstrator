# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore

from baseCommand import BaseCommand
from gui.constants import *

class Switch(BaseCommand):
    """
    This class uses some variables of the super class, therefore they are not instantiated here.
    The checks whether the microcontroller receives a given command or not are all done in the super class.
    In this class, concerning the mentioned checks, only the relevant visualisation is implemented.
    """

    valueChanged = QtCore.pyqtSignal(float)

    def __init__(self, command):
        super(Switch, self).__init__(command)

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

    @property
    def inCoordinates(self):
        return self.mapToScene(QtCore.QPointF(-10, 0))

    @property
    def outCoordinates(self):
        return self.mapToScene(QtCore.QPointF(40, 0))

    # overwrites method of super class
    def negativeConfirmation(self):
        super(Switch, self).negativeConfirmation()
        self.value = self.command.value

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)

        if self.showHoverIndication is True:
            QPainter.setPen(self.dottedPen)
            QPainter.drawPath(self.boundingRectPath)
            QPainter.fillPath(self.boundingRectPath, self.hoverBrush)

        # wrong user input warning is not possible with the switch

        # draw confirmation timeout warning
        if self.showConfirmationTimeoutWarning is True:
            QPainter.fillPath(self.boundingRectPath, self.unconfirmedWarningBrush)

        # draw negative confirmation warning in front of all other colors
        if self.showNegativeConfirmationWarning is True:
            QPainter.fillPath(self.boundingRectPath, self.negativeConfirmedWarningBrush)

        # draw dots
        QPainter.fillPath(self.dotsPath, self.brush)

        QPainter.setPen(self.normalPen)
        QPainter.drawPath(self.fixedLines)

        if self.value < 0.5:
            QPainter.drawPath(self.switchOpenedPath)
        else:
            QPainter.drawPath(self.switchClosedPath)

    def boundingRect(self):
        return QtCore.QRectF(self.bounds[0], self.bounds[1], self.bounds[2] - self.bounds[0], self.bounds[3] - self.bounds[1])

    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height

    # # using method of base command here
    # def setValue(self, value):
    #     self.value = value
    #     self.valueChanged.emit(self.value)

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        if self.value > 0.5:
            self.setValue(0.0)
        else:
            self.setValue(1.0)
        QtGui.QGraphicsItem.mousePressEvent(self, QGraphicsSceneMouseEvent)


