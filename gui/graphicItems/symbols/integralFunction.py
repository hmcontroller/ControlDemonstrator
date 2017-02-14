# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class IntegralFunctionBlock(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(IntegralFunctionBlock, self).__init__(parent)

        self.boundingRectPath = QtGui.QPainterPath()
        self.boundingRectPath.addRect(0, 0, 50, 50)

        self.fractionBarPath = QtGui.QPainterPath()
        self.fractionBarPath.moveTo(15, 25)
        self.fractionBarPath.lineTo(35, 25)

        # rect for numerator
        self.oneRect = QtCore.QRectF(0, 0, 50, 25)

        # rect for denominator
        self.sRect = QtCore.QRectF(0, 25, 50, 25)

        self.font = QtGui.QFont("sans-serif", 10)

        self.pen = QtGui.QPen()
        self.pen.setWidth(2)
        self.pen.setCosmetic(True)


    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        # QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.setPen(self.pen)
        QPainter.drawPath(self.boundingRectPath)
        QPainter.drawPath(self.fractionBarPath)

        QPainter.setFont(self.font)
        QPainter.drawText(self.oneRect,
                         QtCore.Qt.AlignCenter or QtCore.Qt.AlignVCenter,
                         QtCore.QString("1"))
        QPainter.drawText(self.sRect,
                         QtCore.Qt.AlignCenter or QtCore.Qt.AlignVCenter,
                         QtCore.QString("s"))

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 10)

    @property
    def northCoordinates(self):
        return self.mapToScene(QtCore.QPoint(25, 0))

    @property
    def westCoordinates(self):
        return self.mapToScene(QtCore.QPoint(0, 25))

    @property
    def southCoordinates(self):
        return self.mapToScene(QtCore.QPoint(25, 50))

    @property
    def eastCoordinates(self):
        return self.mapToScene(QtCore.QPoint(50, 25))
