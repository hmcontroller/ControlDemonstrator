# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class TankGauge(QtGui.QGraphicsItem):
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)

        self.level = -50

        self.width = 20
        self.height = -100

        self.symbolBorder = QtGui.QPainterPath()
        self.symbolBorder.addRect(-10, self.height - 20, self.width + 60, -self.height + 40)

        self.symbolBorderPen = QtGui.QPen()
        self.symbolBorderPen.setColor(QtGui.QColor(0, 0, 0))
        self.symbolBorderPen.setCosmetic(True)
        self.symbolBorderPen.setWidth(2)


        self.tankBorder = QtGui.QPainterPath()
        self.tankBorder.addRect(0, 0, self.width, self.height)

        self.tankBorderPen = QtGui.QPen()
        self.tankBorderPen.setColor(QtGui.QColor(100, 100, 100))
        self.tankBorderPen.setCosmetic(True)
        self.tankBorderPen.setWidth(1)

        self.blackPen = QtGui.QPen()
        self.blackPen.setColor(QtGui.QColor(0, 0, 0))
        self.blackPen.setCosmetic(True)
        self.blackPen.setWidth(1)

        self.fillRect = QtGui.QPainterPath()
        self.fillRect.moveTo(0, 0)
        self.fillRect.lineTo(self.width, 0)
        self.fillRect.lineTo(self.width, self.level)
        self.fillRect.lineTo(0, self.level)
        self.fillRect.closeSubpath()

        self.digitBorder = QtGui.QPainterPath()
        self.digitBorder.moveTo(self.width + 5, self.level)
        self.digitBorder.lineTo(self.width + 10, self.level - 10)
        self.digitBorder.lineTo(self.width + 40, self.level - 10)
        self.digitBorder.lineTo(self.width + 40, self.level + 10)
        self.digitBorder.lineTo(self.width + 10, self.level + 10)
        self.digitBorder.closeSubpath()

        self.tankColor = QtGui.QBrush(QtGui.QColor(0, 153, 255))

        self.textRect = QtCore.QRectF(self.width + 10, self.level + 10, self.width + 40, self.level - 10)

    def reposition(self):
        self.digitBorder.setElementPositionAt(0, self.width + 1, self.level)
        self.digitBorder.setElementPositionAt(1, self.width + 10, self.level - 10)
        self.digitBorder.setElementPositionAt(2, self.width + 40, self.level - 10)
        self.digitBorder.setElementPositionAt(3, self.width + 40, self.level + 10)
        self.digitBorder.setElementPositionAt(4, self.width + 10, self.level + 10)
        self.digitBorder.setElementPositionAt(5, self.width + 1, self.level)
        self.fillRect.setElementPositionAt(2, self.width, self.level)
        self.fillRect.setElementPositionAt(3, 0, self.level)
        self.textRect = QtCore.QRectF(self.width + 10, self.level - 10, 28, 20)

    def paint(self, painter, QStyleOptionGraphicsItem, QWidget_widget=None):
        self.reposition()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.setPen(self.symbolBorderPen)
        painter.drawPath(self.symbolBorder)

        painter.setPen(self.tankBorderPen)
        painter.drawPath(self.tankBorder)
        painter.fillPath(self.tankBorder, QtGui.QColor(240, 240, 240))

        painter.fillPath(self.fillRect, self.tankColor)

        painter.drawPath(self.digitBorder)
        painter.fillPath(self.digitBorder, QtGui.QColor(240, 240, 240))

        painter.setPen(self.blackPen)
        painter.setFont(QtGui.QFont("Sans Serif", 12))
        painter.drawText(self.textRect,
                         QtCore.Qt.AlignRight or QtCore.Qt.AlignVCenter,
                         QtCore.QString(str(self.level * -1)))

    def boundingRect(self):
        return QtCore.QRectF(-10, -120, 70, 20)

    def setColor(self, color):
        # accepts a tuple with three int values or a QtGui.QColor
        if isinstance(color, tuple):
            self.tankColor = QtGui.QColor(color[0], color[1], color[2])
        else:
            self.tankColor = color
        self.update()

    def setValue(self, value):
        self.level = int(value * -1)
        self.reposition()
        self.update()

    @property
    def northCoordinates(self):
        return self.mapToScene(QtCore.QPoint(30, -120))

    @property
    def westCoordinates(self):
        return self.mapToScene(QtCore.QPoint(-10, -50))

    @property
    def southCoordinates(self):
        return self.mapToScene(QtCore.QPoint(30, 20))

    @property
    def eastCoordinates(self):
        return self.mapToScene(QtCore.QPoint(70, -50))

