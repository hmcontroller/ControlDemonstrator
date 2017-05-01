# -*- encoding: utf-8 -*-
import os

from PyQt4 import QtCore, QtGui

from gui.constants import *
from gui.resources import *

class SymbolButton(QtGui.QGraphicsObject):

    clicked = QtCore.pyqtSignal(object)

    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4
    SETTINGS = 5   
    OK = 6
    TEXT = 7

    def __init__(self, symbol, parent=None):
        super(SymbolButton, self).__init__(parent)
        self.setAcceptHoverEvents(True)

        self.drawBorder = True

        self.currentBackgroundBrush = None

        self.symbol = None
        
        if symbol == self.UP:
            self.symbol = ArrowSymbol(ArrowSymbol.UP, parent=self)
        elif symbol == self.LEFT:
            self.symbol = ArrowSymbol(ArrowSymbol.LEFT, parent=self)
        elif symbol == self.DOWN:
            self.symbol = ArrowSymbol(ArrowSymbol.DOWN, parent=self)
        elif symbol == self.RIGHT:
            self.symbol = ArrowSymbol(ArrowSymbol.RIGHT, parent=self)
        elif symbol == self.SETTINGS:
            self.symbol = SettingsSymbol(parent=self)
        elif symbol == self.OK:
            self.symbol = OkSymbol(parent=self)
        elif symbol == self.TEXT:
            self.symbol = TextSymbol(parent=self)

        self.symbol.setPos(0, 0)

        self.borderPath = QtGui.QPainterPath()
        self.borderPath.moveTo(0, 0)
        self.borderPath.lineTo(25, 0)
        self.borderPath.lineTo(25, 25)
        self.borderPath.lineTo(0, 25)
        self.borderPath.closeSubpath()

        self.borderPen = CABLE_PEN

        self.normalBackgroundBrush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 0))
        self.hoverBackgroundBrush = QtGui.QBrush(HOVER_COLOR)
        self.clickBackgroundBrush = QtGui.QBrush(MOUSE_DOWN_COLOR)

        self.currentBackgroundBrush = self.normalBackgroundBrush

        self.clickReleaseTimer = QtCore.QTimer()
        self.clickReleaseTimer.setSingleShot(True)
        self.clickReleaseTimer.timeout.connect(self.clickRelease)

    # def hoverEnterEvent(self, QGraphicsSceneMouseEvent):
    #     self.currentBackgroundBrush = self.hoverBackgroundBrush
    #     QtGui.QGraphicsItem.hoverEnterEvent(self, QGraphicsSceneMouseEvent)
    #     self.update()
    #
    # def hoverLeaveEvent(self, QGraphicsSceneMouseEvent):
    #     self.currentBackgroundBrush = self.normalBackgroundBrush
    #     QtGui.QGraphicsItem.hoverLeaveEvent(self, QGraphicsSceneMouseEvent)
    #     self.update()

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        self.currentBackgroundBrush = self.clickBackgroundBrush

        # this causes the buttons to react slow while clicking them at a fast interval
        # QtGui.QGraphicsItem.mousePressEvent(self, QGraphicsSceneMouseEvent)

        self.clickReleaseTimer.start(50)
        self.update()
        self.clicked.emit(QGraphicsSceneMouseEvent)


    def clickRelease(self):
        self.currentBackgroundBrush = self.normalBackgroundBrush
        self.update()

    def paint(self, qPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        
        qPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        qPainter.setPen(self.borderPen)

        if self.isUnderMouse() is True:
            qPainter.fillPath(self.borderPath, self.hoverBackgroundBrush)


        qPainter.fillPath(self.borderPath, self.currentBackgroundBrush)
        if self.drawBorder is True:
            qPainter.drawPath(self.borderPath)


    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)


class ArrowSymbol(QtGui.QGraphicsItem):

    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4

    def __init__(self, direction, parent=None):
        super(ArrowSymbol, self).__init__(parent)

        self.arrowPath = QtGui.QPainterPath()
        self.arrowPath.moveTo(0 + 4.5, 6 + 8)
        self.arrowPath.lineTo(8 + 4.5, 0 + 8)
        self.arrowPath.lineTo(16 + 4.5, 6 + 8)

        self.direction = direction

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)

        if self.direction == self.UP:
            QPainter.translate(0, 0)
            QPainter.rotate(0)
        elif self.direction == self.LEFT:
            QPainter.translate(0, 25)
            QPainter.rotate(270)
        elif self.direction == self.DOWN:
            QPainter.translate(25, 25)
            QPainter.rotate(180)
        elif self.direction == self.RIGHT:
            QPainter.translate(25, 0)
            QPainter.rotate(90)

        QPainter.drawPath(self.arrowPath)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)



class SettingsSymbol(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(SettingsSymbol, self).__init__(parent)

        self.outerPath = QtGui.QPainterPath()
        self.outerPath.moveTo(0, 0)
        self.outerPath.lineTo(8 + 4.5, 6 + 12)

        self.pixmapItem = QtGui.QGraphicsPixmapItem(self)

        # absDir = os.path.dirname(os.path.realpath(__file__))
        # absPath = os.path.join(absDir, "settings.png")

        self.pixmap = QtGui.QPixmap(settingsPngPath)
        self.pixmapItem.setPixmap(self.pixmap)
        self.pixmapItem.scale(0.04, 0.04)
        self.pixmapItem.setPos(2, 2)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        pass

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)


class OkSymbol(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(OkSymbol, self).__init__(parent)

        self.path = QtGui.QPainterPath()
        self.path.moveTo(8, 13)
        self.path.lineTo(12.5, 20)
        self.path.lineTo(18, 8)

        self.pen = QtGui.QPen()
        self.pen.setWidth(1)
        self.pen.setCosmetic(True)
        self.pen.setColor(QtCore.Qt.black)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.setPen(self.pen)
        QPainter.drawPath(self.path)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)


class PendingSymbol(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(PendingSymbol, self).__init__(parent)


        self.pendingRect = QtCore.QRectF(0, 0, 25, 25)

        self.grayPen = QtGui.QPen()
        self.grayPen.setColor(QtCore.Qt.gray)

        self.redPen = QtGui.QPen()
        self.redPen.setColor(QtCore.Qt.red)

        self.font =  QtGui.QFont("sans-serif", 12)
        self.font.setBold(True)

        self.currentPen = self.grayPen

    def setToRed(self):
        self.currentPen = self.redPen
        self.update()

    def setToGray(self):
        self.currentPen = self.grayPen
        self.update()

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        # QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.setPen(self.currentPen)

        QPainter.setFont(self.font)
        QPainter.drawText(self.pendingRect,
                         QtCore.Qt.AlignCenter,
                         QtCore.QString(u"P"))

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)


class TextSymbol(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(TextSymbol, self).__init__(parent)


        self.textRect = QtCore.QRectF(0, 0, 25, 25)

        self.font =  QtGui.QFont("sans-serif", 12)
        self.font.setBold(True)
        self.pen = QtGui.QPen(QtCore.Qt.black)
        self.text = u"0"

    def setText(self, text):
        self.text = text
        self.update()

    def currentText(self):
        return self.text

    def setColor(self, color):
        self.pen = QtGui.QPen(color)

    def setFont(self, font):
        self.font = font
        self.font.setBold(True)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)

        QPainter.setPen(self.pen)
        QPainter.setFont(self.font)

        QPainter.drawText(self.textRect,
                         QtCore.Qt.AlignCenter,
                         QtCore.QString(self.text))

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 25)



