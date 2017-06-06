# -*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from gui.resources import *

class SplashScreen(QtGui.QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()

        self.pen = QtGui.QPen()
        self.pen.setWidth(5)
        self.pen.setCosmetic(True)
        self.pen.setBrush(QtGui.QBrush(QtCore.Qt.lightGray))

        self.otherPen = QtGui.QPen()
        self.otherPen.setWidth(5)
        self.otherPen.setCosmetic(True)
        self.otherPen.setBrush(QtGui.QBrush(QtCore.Qt.darkGray))

        self.splashPixMap = QtGui.QPixmap(iconPath)
        self.splashPixMap = self.splashPixMap.scaled(400, 400)
        self.setPixmap(self.splashPixMap)

        self.font = QtGui.QFont("sans-serif", 8)

        self.progress = 0.0
        self.message = u""

    def drawContents(self, painter):
        super(SplashScreen, self).drawContents(painter)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(self.pen)

        painter.setFont(self.font)
        painter.drawText(QtCore.QRectF(38, 360, 250, 20),
                         QtCore.Qt.AlignLeft,
                         QtCore.QString(self.message))


        progressBackgroundPath = QtGui.QPainterPath()
        progressBackgroundPath.moveTo(38, 380)
        progressBackgroundPath.lineTo(370, 380)

        painter.setPen(self.otherPen)
        painter.drawPath(progressBackgroundPath)

        progressPixel = 38 + (380 - 38) * self.progress

        progressPath = QtGui.QPainterPath()
        progressPath.moveTo(38, 380)
        progressPath.lineTo(progressPixel, 380)

        painter.setPen(self.pen)
        painter.drawPath(progressPath)


    def setProgress(self, progress):
        self.progress = progress
        self.update()

    def setMessage(self, message):
        self.message = message