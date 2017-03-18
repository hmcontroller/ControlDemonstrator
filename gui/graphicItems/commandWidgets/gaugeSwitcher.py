# -*- encoding: utf-8 -*-
from PyQt4 import QtCore

from baseCommand import BaseCommand
from gui.constants import *
from gui.graphicItems.button import SymbolButton

class GaugeSwitcher(BaseCommand):
    """
    This class uses some variables of the super class, therefore they are not instantiated here.
    The checks whether the microcontroller receives a given command or not are all done in the super class.
    In this class, concerning the mentioned checks, only the relevant visualisation should be implemented.
    """

    valueChanged = QtCore.pyqtSignal(float)

    def __init__(self, command, gauges):
        super(GaugeSwitcher, self).__init__(command)

        if len(gauges) == 0:
            raise ValueError("Need at least one gauge in the list")

        self.command = command

        self.command.setLowerLimit(0, self)
        self.command.setUpperLimit(len(gauges) - 1, self)



        self.gauges = gauges

        for gauge in self.gauges:
            gauge.setParentItem(self)
            gauge.setPos(10, 25)
            gauge.hide()

        self.currentNumber = int(command.getValue())
        self.gauges[0].show()

        self.width = 80
        self.height = self.gauges[0].boundingRect().height() + 25

        self.leftButton = SymbolButton(SymbolButton.LEFT, parent=self)
        self.leftButton.setPos(0, 0)
        self.leftButton.clicked.connect(self.oneToTheLeft)

        self.rightButton = SymbolButton(SymbolButton.RIGHT, parent=self)
        buttonWidth = self.rightButton.boundingRect().width()
        self.rightButton.setPos(self.width - buttonWidth, 0)
        self.rightButton.clicked.connect(self.oneToTheRight)

        self.borderPath = QtGui.QPainterPath()
        self.borderPath.addRect(0, 0, self.width, self.height)
        self.borderPen = CABLE_PEN
        self.backgroundBrush = QtGui.QBrush(QtCore.Qt.lightGray)

    def valueChangedPerWidget(self, widgetInstance):
        if widgetInstance is self:
            pass
        else:
            self.currentNumber = int(round(self.command.getValue()))
            self.actualize()

    # overwrites method of super class
    def differentValueReceived(self):
        # this call is needed to start the blink timer
        super(GaugeSwitcher, self).differentValueReceived()

        self.currentNumber = int(round(self.command.getValue()))
        self.actualize()

    def oneToTheLeft(self):
        self.currentNumber -= 1
        self.fitNumberInRange()
        self.command.setValue(self.currentNumber, self)
        self.actualize()

    def oneToTheRight(self):
        self.currentNumber += 1
        self.fitNumberInRange()
        self.command.setValue(self.currentNumber, self)
        self.actualize()

    def actualize(self):
        for gauge in self.gauges:
            gauge.hide()
        self.gauges[self.currentNumber].show()
        self.update()

    def fitNumberInRange(self):
        if self.currentNumber < self.command.getLowerLimit():
            self.currentNumber = self.command.getLowerLimit()
        if self.currentNumber > self.command.getUpperLimit():
            self.currentNumber = self.command.getUpperLimit()

    @property
    def northCoordinates(self):
        return self.mapToScene(QtCore.QPoint(self.width / 2, 0))

    @property
    def westCoordinates(self):
        return self.mapToScene(QtCore.QPoint(0, self.height / 2))

    @property
    def southCoordinates(self):
        return self.mapToScene(QtCore.QPoint(self.width / 2, self.height))

    @property
    def eastCoordinates(self):
        return self.mapToScene(QtCore.QPoint(self.width, self.height / 2))


    def paint(self, qPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        qPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        qPainter.setPen(self.borderPen)
        # qPainter.fillPath(self.borderPath, self.backgroundBrush)
        qPainter.drawPath(self.borderPath)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.width, self.height)