# -*- encoding: utf-8 -*-
import math

from PyQt4 import QtCore

from core.signalGeneratorCommandGroup import SignalGeneratorCommandGroup
from gui.constants import *
from gui.graphicItems.commandWidgets.baseCommand import BaseCommand
from gui.graphicItems.button import SymbolButton
from gui.genericCommandEditorWindow import GenericCommandEditorWindow


class SignalGenerator(BaseCommand):
    def __init__(self, signalGeneratorCommandGroup):
        if not isinstance(signalGeneratorCommandGroup, SignalGeneratorCommandGroup):
            raise TypeError("must be initialized with a core.signalGeneratorCommandGroup.SignalGeneratorCommandGroup instance")

        self.commands = signalGeneratorCommandGroup
        self.functionNumberCommand = self.commands.functionNumberCommand

        # there exist 6 functions that can be used for signal generation at the time of writing this (2017-02-23).
        self.functionNumberCommand.setLowerLimit(0, self)
        self.functionNumberCommand.setUpperLimit(4, self)
        self.signalSymbols = list()

        # the command to set the function number of the generator is used as main command here
        # TODO refactor comment one line above
        super(SignalGenerator, self).__init__(self.commands.functionNumberCommand)


        # set up some groups of commands, each suitable for a function number
        # the editing of the parameters takes place in a popup window
        self.groupedCommandLists = list()

        # these are commands for the dirac function
        cmds = list()
        cmds.append(self.commands.diracLowCommand)
        cmds[-1].displayName = u"unterer Wert"
        cmds.append(self.commands.diracHighCommand)
        cmds[-1].displayName = u"oberer Wert"
        cmds.append(self.commands.diracDurationCommand)
        cmds[-1].displayName = u"Dauer in Sekunden"
        self.groupedCommandLists.append(cmds)

        # these are commands for the heavyside function
        cmds = list()
        cmds.append(self.commands.stepLowCommand)
        cmds[-1].displayName = u"unterer Wert"
        cmds.append(self.commands.stepHighCommand)
        cmds[-1].displayName = u"oberer Wert"
        self.groupedCommandLists.append(cmds)

        # these are commands for the ramp function
        cmds = list()
        cmds.append(self.commands.rampState)
        cmds[-1].displayName = u"Rampe Richtung"
        cmds.append(self.commands.rampGradient)
        cmds[-1].displayName = u"Rampe Steigung"
        cmds.append(self.commands.rampLow)
        cmds[-1].displayName = u"Rampe unten"
        cmds.append(self.commands.rampHigh)
        cmds[-1].displayName = u"Rampe oben"



        self.groupedCommandLists.append(cmds)

        # these are commands for the sin function
        cmds = list()
        cmds.append(self.commands.sinAmplitudeCommand)
        cmds[-1].displayName = u"Amplitude"
        cmds.append(self.commands.sinOmegaCommand)
        cmds[-1].displayName = u"Omega"
        cmds.append(self.commands.sinOffsetCommand)
        cmds[-1].displayName = u"Y-Offset"
        self.groupedCommandLists.append(cmds)

        # these are commands for the square wave function
        cmds = list()
        cmds.append(self.commands.squareLowCommand)
        cmds[-1].displayName = u"Square unterer Wert"
        cmds.append(self.commands.squareHighCommand)
        cmds[-1].displayName = u"Square oberer Wert"
        cmds.append(self.commands.squareFrequencyCommand)
        cmds[-1].displayName = u"Square Frequenz in Hz"

        self.groupedCommandLists.append(cmds)


        # a list with functions that get executed on the trigger button
        self.triggerCommands = list()
        self.triggerCommands.append(self.startDirac)
        self.triggerCommands.append(self.toggleHeavySide)
        self.triggerCommands.append(self.toggleRamp)
        self.triggerCommands.append(None)
        self.triggerCommands.append(None)




        self.warningPath = QtGui.QPainterPath()
        self.warningPath.addRect(70, 5, 20, 20)

        self.upButton = SymbolButton(SymbolButton.UP, parent=self)
        self.upButton.setPos(125, 0)
        self.upButton.clicked.connect(self.oneSignalUp)

        self.okButton = SymbolButton(SymbolButton.OK, parent=self)
        self.okButton.setPos(125, 25)
        # the slot connected to this button changes programmatically

        self.settingsButton = SymbolButton(SymbolButton.SETTINGS, parent=self)
        self.settingsButton.setPos(125, 50)
        self.settingsButton.clicked.connect(self.settingsButtonClicked)

        self.downButton = SymbolButton(SymbolButton.DOWN, parent=self)
        self.downButton.setPos(125, 75)
        self.downButton.clicked.connect(self.oneSignalDown)


        dirac = DiracSignal(self)
        dirac.setPos(20, 0)
        self.signalSymbols.append(dirac)

        heavySide = HeaviSideSignal(self)
        heavySide.setPos(20, 0)
        self.signalSymbols.append(heavySide)

        ramp = RampSignal(self)
        ramp.setPos(20, 0)
        self.signalSymbols.append(ramp)

        sinus = SinusSignal(self)
        sinus.setPos(25, 50)
        sinus.setScale(0.2)
        self.signalSymbols.append(sinus)

        square = SquareSignal(self)
        square.setPos(20, 0)
        self.signalSymbols.append(square)

        self.currentSignalNumber = int(self.command.getValue())
        self.drawCurrentSignal()

        self.constantShape = SignalGeneratorConstantShape(self)

        # # if i open a window here to let the user edit some properties, it needs to be updated to show
        # #  warnings, if some are active.
        # self.dialogUpdateTimer = QtCore.QTimer()
        # self.dialogUpdateTimer.setSingleShot(False)
        # self.dialogUpdateTimer.timeout.connect(self.updateDialog)

        self.currentDialog = None

        self.sigNumberFont = QtGui.QFont("sans-serif", 10, QtGui.QFont.Normal)
        self.sigNumberRect = QtCore.QRectF(100, 5, 50, 50)

        self.connectTriggerButton()

    def connectTriggerButton(self):
        try:
            self.okButton.clicked.disconnect()
        except TypeError:
            pass

        if self.triggerCommands[self.currentSignalNumber] is not None:
            self.okButton.clicked.connect(self.triggerCommands[self.currentSignalNumber])

    def startDirac(self):
        self.commands.diracNowCommand.setValue(1.0, self)

    def toggleHeavySide(self):
        if self.commands.stepStateCommand.getValue() < 0.5:
            self.commands.stepStateCommand.setValue(1.0, self)
        else:
            self.commands.stepStateCommand.setValue(0.0, self)

    def toggleRamp(self):
        if self.commands.rampState.getValue() < 0.5:
            self.commands.rampState.setValue(1.0, self)
        else:
            self.commands.rampState.setValue(0.0, self)

    def updateDialog(self):
        self.currentDialog.update()

    def oneSignalUp(self, qGraphicsSceneMouseEvent):
        self.currentSignalNumber += 1
        if self.currentSignalNumber >= len(self.signalSymbols):
            self.currentSignalNumber = len(self.signalSymbols) - 1
        self.functionNumberCommand.setValue(self.currentSignalNumber, self)
        self.actualizeSignalSymbol()

    def oneSignalDown(self, qGraphicsSceneMouseEvent):
        self.currentSignalNumber -= 1
        if self.currentSignalNumber <= 0:
            self.currentSignalNumber = 0
        self.functionNumberCommand.setValue(self.currentSignalNumber, self)
        self.actualizeSignalSymbol()

    def settingsButtonClicked(self, qGraphicsSceneMouseEvent):
        lastDialog = self.currentDialog
        if lastDialog is not None:
            lastDialog.hide()

        self.currentDialog = GenericCommandEditorWindow(self.groupedCommandLists[self.currentSignalNumber])

        # self.dialogUpdateTimer.start(50)

        self.currentDialog.show()

    def valueChangedPerWidget(self, widgetInstance):
        if widgetInstance is self:
            pass
        else:
            self.currentSignalNumber = int(round(self.command.getValue()))
            self.actualizeSignalSymbol()


    def differentValueReceived(self):
        super(SignalGenerator, self).differentValueReceived()
        self.currentSignalNumber = int(round(self.command.getValue()))
        self.actualizeSignalSymbol()

    def actualizeSignalSymbol(self):
        self.drawCurrentSignal()
        self.connectTriggerButton()

    def drawCurrentSignal(self):
        for sig in self.signalSymbols:
            sig.hide()
        if len(self.signalSymbols) > 0:
            self.signalSymbols[self.currentSignalNumber].show()
        self.update()

    @property
    def northCoordinates(self):
        return self.mapToScene(QtCore.QPoint(75, 0))

    @property
    def westCoordinates(self):
        return self.mapToScene(QtCore.QPoint(0, 50))

    @property
    def southCoordinates(self):
        return self.mapToScene(QtCore.QPoint(75, 100))

    @property
    def eastCoordinates(self):
        return self.mapToScene(QtCore.QPoint(150, 50))

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        if self.showCommFailureWarning is True:
            QPainter.fillPath(self.warningPath, self.commFailureWarningBrush)

        # draw the signal number
        sigNumberText = str(self.currentSignalNumber + 1) + "/5"
        QPainter.setFont(self.sigNumberFont)
        QPainter.drawText(self.sigNumberRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                         QtCore.QString(sigNumberText))

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 150, 100)



class SignalGeneratorConstantShape(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(SignalGeneratorConstantShape, self).__init__(parent)

        # boundingRect
        self.boundingRectPath = QtGui.QPainterPath()
        self.boundingRectPath.moveTo(0, 0)
        self.boundingRectPath.lineTo(0, 100)
        self.boundingRectPath.lineTo(150, 100)
        self.boundingRectPath.lineTo(150, 0)
        self.boundingRectPath.closeSubpath()

        # rects of button areas
        self.boundingRectPath.moveTo(125, 0)
        self.boundingRectPath.lineTo(125, 100)
        self.boundingRectPath.moveTo(150, 25)
        self.boundingRectPath.lineTo(125, 25)
        self.boundingRectPath.moveTo(150, 50)
        self.boundingRectPath.lineTo(125, 50)
        self.boundingRectPath.moveTo(150, 75)
        self.boundingRectPath.lineTo(125, 75)

        self.boundingRectPen = QtGui.QPen()
        self.boundingRectPen.setWidth(2)
        self.boundingRectPen.setCosmetic(True)
        # self.boundingRectPen.setColor(QtCore.Qt.lightGray)

        # coordinate system
        self.cSysPath = QtGui.QPainterPath()
        self.cSysPath.moveTo(10, 85)
        self.cSysPath.lineTo(110, 85)
        self.cSysPath.moveTo(15, 90)
        self.cSysPath.lineTo(15, 15)
        self.cSysPath.moveTo(10, 20)
        self.cSysPath.lineTo(15, 15)
        self.cSysPath.lineTo(20, 20)
        self.cSysPath.moveTo(105, 80)
        self.cSysPath.lineTo(110, 85)
        self.cSysPath.lineTo(105, 90)

        self.cSysPen = QtGui.QPen()
        self.cSysPen.setWidth(1)
        self.cSysPen.setCosmetic(True)
        self.cSysPen.setColor(QtCore.Qt.darkGray)

        # rects for axis label positions
        self.uRect = QtCore.QRectF(5, 20, 15, 15)
        self.tRect = QtCore.QRectF(95, 85, 15, 15)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        # QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.setPen(self.boundingRectPen)
        QPainter.drawPath(self.boundingRectPath)

        QPainter.setPen(self.cSysPen)
        QPainter.drawPath(self.cSysPath)

        QPainter.drawText(self.uRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         QtCore.QString("u"))
        QPainter.drawText(self.tRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         QtCore.QString("t"))

    def mouseDoubleClickEvent(self, QMouseEvent):
        pass

    def confirmationTimeOut(self):
        pass
        # print "hello signalSourceWidget timeOut"

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 151, 101)




class SinusSignal(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(SinusSignal, self).__init__(parent)

        self.path = QtGui.QPainterPath()
        self.path.moveTo(0, 0)
        for i in range(0, 360):
            self.path.lineTo(i, math.sin((math.pi / 180) * i) * 100)

        self.pen = QtGui.QPen()
        self.pen.setWidth(2)
        self.pen.setCosmetic(True)
        self.pen.setColor(QtCore.Qt.black)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.setPen(self.pen)
        QPainter.drawPath(self.path)


class RampSignal(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(RampSignal, self).__init__(parent)

        self.upHillPath = QtGui.QPainterPath()
        self.upHillPath.moveTo(5, 75)
        self.upHillPath.lineTo(15, 75)
        self.upHillPath.lineTo(70, 30)
        self.upHillPath.lineTo(80, 30)

        self.pen = QtGui.QPen()
        self.pen.setWidth(2)
        self.pen.setCosmetic(True)
        self.pen.setColor(QtCore.Qt.black)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.setPen(self.pen)
        QPainter.drawPath(self.upHillPath)


class DiracSignal(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(DiracSignal, self).__init__(parent)

        self.path = QtGui.QPainterPath()
        self.path.moveTo(5, 75)
        self.path.lineTo(20, 75)
        self.path.lineTo(20, 30)
        self.path.lineTo(30, 30)
        self.path.lineTo(30, 75)
        self.path.lineTo(80, 75)

        self.pen = QtGui.QPen()
        self.pen.setWidth(2)
        self.pen.setCosmetic(True)
        self.pen.setColor(QtCore.Qt.black)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.setPen(self.pen)
        QPainter.drawPath(self.path)


class SquareSignal(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(SquareSignal, self).__init__(parent)

        self.path = QtGui.QPainterPath()
        self.path.moveTo(5, 75)
        for i in range(20, 80, 20):
            self.path.lineTo(i, 75)
            self.path.lineTo(i, 30)
            self.path.lineTo(i+10, 30)
            self.path.lineTo(i+10, 75)
        self.path.lineTo(80, 75)


        self.pen = QtGui.QPen()
        self.pen.setWidth(2)
        self.pen.setCosmetic(True)
        self.pen.setColor(QtCore.Qt.black)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.setPen(self.pen)
        QPainter.drawPath(self.path)


class HeaviSideSignal(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(HeaviSideSignal, self).__init__(parent)

        self.upPath = QtGui.QPainterPath()
        self.upPath.moveTo(5, 75)
        self.upPath.lineTo(30, 75)
        self.upPath.lineTo(30, 30)
        self.upPath.lineTo(80, 30)

        self.downPath = QtGui.QPainterPath()
        self.downPath.moveTo(5, 30)
        self.downPath.lineTo(30, 30)
        self.downPath.lineTo(30, 75)
        self.downPath.lineTo(80, 75)

        self.pen = QtGui.QPen()
        self.pen.setWidth(2)
        self.pen.setCosmetic(True)
        self.pen.setColor(QtCore.Qt.black)

        self.currentPath = self.upPath

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.setPen(self.pen)
        QPainter.drawPath(self.currentPath)

    def toggleUpDown(self):
        if self.currentPath == self.upPath:
            self.currentPath = self.downPath
        else:
            self.currentPath = self.upPath
