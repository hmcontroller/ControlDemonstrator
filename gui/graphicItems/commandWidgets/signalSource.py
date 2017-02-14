# -*- encoding: utf-8 -*-
import math
import os

from PyQt4 import QtGui, QtCore

from gui.constants import *


class SignalSource(QtGui.QGraphicsObject):

    # valueChanged = QtCore.pyqtSignal(float)

    def __init__(self):
        super(SignalSource, self).__init__()

        self.showConfirmationFailure = False

        self.isCommandConfirmed = False

        self.warningPath = QtGui.QPainterPath()
        self.warningPath.addRect(100, 5, 20, 20)

        self.warningBrush = QtGui.QBrush(CONFIRMATION_WARNING_COLOR)

        self.upButton = UpButton(self)
        self.upButton.setPos(125, 0)
        self.upButton.clicked.connect(self.oneSignalUp)

        self.okButton = OkButton(self)
        self.okButton.setPos(125, 25)

        self.settingsButton = SettingsButton(self)
        self.settingsButton.setPos(125, 50)

        self.downButton = DownButton(self)
        self.downButton.setPos(125, 75)
        self.downButton.clicked.connect(self.oneSignalDown)

        self.signalSymbols = list()

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

        self.currentSignalNumber = 0
        self.setCurrentSignal()

        self.constantShape = SignalSourceConstantShape(self)

        self.confirmationWarningTimer = QtCore.QTimer()
        self.confirmationWarningTimer.setSingleShot(False)
        self.confirmationWarningTimer.timeout.connect(self.toggleConfirmationFailureIndication)
        self.confirmationWarningBlinkInterval = 200
        self.confirmationWarningTimer.start(self.confirmationWarningBlinkInterval)

    def oneSignalUp(self):
        self.currentSignalNumber += 1
        if self.currentSignalNumber >= len(self.signalSymbols):
            self.currentSignalNumber = len(self.signalSymbols) - 1
        self.setCurrentSignal()

    def oneSignalDown(self):
        self.currentSignalNumber -= 1
        if self.currentSignalNumber <= 0:
            self.currentSignalNumber = 0
        self.setCurrentSignal()

    def setCurrentSignal(self):
        for sig in self.signalSymbols:
            sig.hide()
        self.signalSymbols[self.currentSignalNumber].show()

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
        if self.showConfirmationFailure is True:
            QPainter.fillPath(self.warningPath, self.warningBrush)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 150, 100)


class SignalSourceConstantShape(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(SignalSourceConstantShape, self).__init__(parent)

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
                         QtCore.Qt.AlignLeft or QtCore.Qt.AlignVCenter,
                         QtCore.QString("u"))
        QPainter.drawText(self.tRect,
                         QtCore.Qt.AlignLeft or QtCore.Qt.AlignVCenter,
                         QtCore.QString("t"))

    def mouseDoubleClickEvent(self, QMouseEvent):
        pass

    def confirmationTimeOut(self):
        print "hello signalSourceWidget timeOut"

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 151, 101)



class LittleButton(QtGui.QGraphicsObject):

    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(LittleButton, self).__init__(parent)
        self.setAcceptHoverEvents(True)

        self.currentBackgroundBrush = None

        self.backgroundPath = QtGui.QPainterPath()
        self.backgroundPath.moveTo(0, 0)
        self.backgroundPath.lineTo(25, 0)
        self.backgroundPath.lineTo(25, 25)
        self.backgroundPath.lineTo(0, 25)
        self.backgroundPath.closeSubpath()

        self.normalBackgroundBrush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 0))
        self.hoverBackgroundBrush = QtGui.QBrush(HOVER_COLOR)
        self.clickBackgroundBrush = QtGui.QBrush(MOUSE_DOWN_COLOR)

        self.currentBackgroundBrush = self.normalBackgroundBrush

        self.clickReleaseTimer = QtCore.QTimer()
        self.clickReleaseTimer.setSingleShot(True)
        self.clickReleaseTimer.timeout.connect(self.clickRelease)

    def hoverEnterEvent(self, QGraphicsSceneMouseEvent):
        self.currentBackgroundBrush = self.hoverBackgroundBrush
        QtGui.QGraphicsItem.hoverEnterEvent(self, QGraphicsSceneMouseEvent)

    def hoverLeaveEvent(self, QGraphicsSceneMouseEvent):
        self.currentBackgroundBrush = self.normalBackgroundBrush
        QtGui.QGraphicsItem.hoverLeaveEvent(self, QGraphicsSceneMouseEvent)

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        self.currentBackgroundBrush = self.clickBackgroundBrush
        self.clickReleaseTimer.start(50)
        QtGui.QGraphicsItem.mousePressEvent(self, QGraphicsSceneMouseEvent)
        self.clicked.emit()

    def clickRelease(self):
        self.currentBackgroundBrush = self.hoverBackgroundBrush

    # def mouseDoubleClickEvent(self, QMouseEvent):
    #     print "double"


class UpButton(LittleButton):

    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(UpButton, self).__init__(parent)

        self.arrowPath = QtGui.QPainterPath()
        self.arrowPath.moveTo(0 + 4.5, 6 + 8)
        self.arrowPath.lineTo(8 + 4.5, 0 + 8)
        self.arrowPath.lineTo(16 + 4.5, 6 + 8)

    #     LittleButton.clicked.connect(self.clicki)
    #
    # def clicki(self):
    #     self.clicked.emit()

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.fillPath(self.backgroundPath, self.currentBackgroundBrush)

        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.drawPath(self.arrowPath)



class DownButton(LittleButton):
    def __init__(self, parent=None):
        super(DownButton, self).__init__(parent)

        self.arrowPath = QtGui.QPainterPath()
        self.arrowPath.moveTo(0 + 4.5, 0 + 12)
        self.arrowPath.lineTo(8 + 4.5, 6 + 12)
        self.arrowPath.lineTo(16 + 4.5, 0 + 12)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.fillPath(self.backgroundPath, self.currentBackgroundBrush)

        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.drawPath(self.arrowPath)


class SettingsButton(LittleButton):
    def __init__(self, parent=None):
        super(SettingsButton, self).__init__(parent)

        self.outerPath = QtGui.QPainterPath()
        self.outerPath.moveTo(0, 0)
        self.outerPath.lineTo(8 + 4.5, 6 + 12)

        self.pixmapItem = QtGui.QGraphicsPixmapItem(self)
        absDir = os.path.dirname(os.path.realpath(__file__))
        absPath = os.path.join(absDir, "settings.png")
        self.pixmap = QtGui.QPixmap(absPath)
        self.pixmapItem.setPixmap(self.pixmap)
        self.pixmapItem.scale(0.04, 0.04)
        self.pixmapItem.setPos(2, 2)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.fillPath(self.backgroundPath, self.currentBackgroundBrush)


class OkButton(LittleButton):
    def __init__(self, parent=None):
        super(OkButton, self).__init__(parent)

        self.path = QtGui.QPainterPath()
        self.path.moveTo(8, 13)
        self.path.lineTo(12.5, 20)
        self.path.lineTo(18, 8)

        self.pen = QtGui.QPen()
        self.pen.setWidth(1)
        self.pen.setCosmetic(True)
        self.pen.setColor(QtCore.Qt.black)


    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.fillPath(self.backgroundPath, self.currentBackgroundBrush)
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.setPen(self.pen)
        QPainter.drawPath(self.path)

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