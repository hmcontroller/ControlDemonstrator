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

        self.command = command

        self.command.lowerLimit = 0
        self.command.upperLimit = 3


        if len(gauges) == 0:
            raise ValueError("Need at least one gauge in the list")

        self.gauges = gauges

        for gauge in self.gauges:
            gauge.setParentItem(self)
            gauge.setPos(10, 25)
            gauge.hide()

        self.currentNumber = int(command.value)
        self.gauges[0].show()
        # self.command.setValue(0.0)

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

    def valueChangedFromController(self):
        self.currentNumber = int(round(self.command.value))
        self.actualize()

    def oneToTheLeft(self):
        self.currentNumber -= 1
        self.fitNumberInRange()
        self.command.setValue(self.currentNumber)
        self.actualize()

    def oneToTheRight(self):
        self.currentNumber += 1
        self.fitNumberInRange()
        self.command.setValue(self.currentNumber)
        self.actualize()

    def actualize(self):
        for gauge in self.gauges:
            gauge.hide()
        self.gauges[self.currentNumber].show()
        self.update()

    def fitNumberInRange(self):
        if self.currentNumber < self.command.lowerLimit:
            self.currentNumber = self.command.lowerLimit
        if self.currentNumber > self.command.upperLimit:
            self.currentNumber = self.command.upperLimit

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