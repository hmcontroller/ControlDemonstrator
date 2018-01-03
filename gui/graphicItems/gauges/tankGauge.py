# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class TankGauge(QtGui.QGraphicsItem):
    def __init__(self):
        """
        Keep in mind, that the Qt coordinate system has its origin in the upper left corner and
        the y axis values increase from top to bottom.
        """
        QtGui.QGraphicsItem.__init__(self)

        self.width = 20
        self.height = 100


        self.tankTopPixel = 20
        self.tankBottomPixel = self.height
        self.calculatedPixelLevel = self.tankBottomPixel - 1
        self.absoluteDisplayValue = 0
        self.relativeDisplayValue = 0

        self.lowerLimit = 0
        self.upperLimit = 1
        self.value = 0
        self.isRelativeScale = True
        self.isValueBelowLimit = False
        self.isValueAboveLimit = False


        self.tankBorder = QtGui.QPainterPath()
        self.tankBorder.addRect(0, self.tankTopPixel, self.width, self.tankBottomPixel - self.tankTopPixel)

        self.tankBorderPen = QtGui.QPen()
        self.tankBorderPen.setColor(QtGui.QColor(100, 100, 100))
        self.tankBorderPen.setCosmetic(True)
        self.tankBorderPen.setWidth(1)

        self.blackPen = QtGui.QPen()
        self.blackPen.setColor(QtGui.QColor(0, 0, 0))
        self.blackPen.setCosmetic(True)
        self.blackPen.setWidth(1)

        self.fillRect = QtGui.QPainterPath()
        self.fillRect.moveTo(0, self.tankBottomPixel)
        self.fillRect.lineTo(self.width, self.tankBottomPixel)
        self.fillRect.lineTo(self.width, self.calculatedPixelLevel)
        self.fillRect.lineTo(0, self.calculatedPixelLevel)
        self.fillRect.closeSubpath()

        self.digitBorder = QtGui.QPainterPath()
        self.digitBorder.moveTo(self.width + 5, self.calculatedPixelLevel)
        self.digitBorder.lineTo(self.width + 10, self.calculatedPixelLevel - 10)
        self.digitBorder.lineTo(self.width + 40, self.calculatedPixelLevel - 10)
        self.digitBorder.lineTo(self.width + 40, self.calculatedPixelLevel + 10)
        self.digitBorder.lineTo(self.width + 10, self.calculatedPixelLevel + 10)
        self.digitBorder.closeSubpath()

        self.tankColor = QtGui.QBrush(QtGui.QColor(0, 153, 255))

        self.textRect = QtCore.QRectF(self.width + 10, self.calculatedPixelLevel + 10, self.width + 40, self.calculatedPixelLevel - 10)
        self.warningTextRect = QtCore.QRectF(0, self.tankTopPixel, self.width, self.tankBottomPixel - self.tankTopPixel)

        self.calculatePixelLevel()
        self.reposition()
        # self.update()

        # self.warningBelowPath = QtGui.QPainterPath()
        # for i in range(0, 3):
        #     pass
        #
        # self.warningAbovePath = QtGui.QPainterPath()

    def setColor(self, color):
        # accepts a tuple with three int values or a QtGui.QColor
        if isinstance(color, tuple) or isinstance(color, list):
            self.tankColor = QtGui.QColor(color[0], color[1], color[2])
        else:
            self.tankColor = color
        self.update()

    def setValue(self, value):
        self.isValueBelowLimit = False
        self.isValueAboveLimit = False

        self.value = value

        if self.value < self.lowerLimit:
            self.isValueBelowLimit = True
            self.absoluteDisplayValue = 0
            self.relativeDisplayValue = "x"
        elif self.value > self.upperLimit:
            self.isValueAboveLimit = True
            self.absoluteDisplayValue = 0
            self.relativeDisplayValue = "x"
        else:
            self.absoluteDisplayValue = self.value
            self.relativeDisplayValue = int(100 * self.percentageOfRange(self.value))

        self.calculatePixelLevel()
        self.reposition()
        self.update()

    def newValueArrived(self, channel):
        self.setValue(channel[-1])

    def valueToAbsolute(self):
        pass

    def calculatePixelLevel(self):
        valueInPercent = self.percentageOfRange(self.value)
        self.calculatedPixelLevel = float(self.tankBottomPixel) - float((self.tankBottomPixel - self.tankTopPixel)) * valueInPercent
        if self.calculatedPixelLevel < self.tankTopPixel:
            self.calculatedPixelLevel = self.tankTopPixel
        if self.calculatedPixelLevel > self.tankBottomPixel:
            self.calculatedPixelLevel = self.tankBottomPixel

    def percentageOfRange(self, value):
        return (float(value) - float(self.lowerLimit)) / (float(self.upperLimit) - float(self.lowerLimit))



    def reposition(self):
        self.digitBorder.setElementPositionAt(0, self.width + 1, self.calculatedPixelLevel)
        self.digitBorder.setElementPositionAt(1, self.width + 10, self.calculatedPixelLevel - 10)
        self.digitBorder.setElementPositionAt(2, self.width + 40, self.calculatedPixelLevel - 10)
        self.digitBorder.setElementPositionAt(3, self.width + 40, self.calculatedPixelLevel + 10)
        self.digitBorder.setElementPositionAt(4, self.width + 10, self.calculatedPixelLevel + 10)
        self.digitBorder.setElementPositionAt(5, self.width + 1, self.calculatedPixelLevel)
        self.fillRect.setElementPositionAt(2, self.width, self.calculatedPixelLevel)
        self.fillRect.setElementPositionAt(3, 0, self.calculatedPixelLevel)
        self.textRect = QtCore.QRectF(self.width + 10, self.calculatedPixelLevel - 10, 28, 20)

    def paint(self, painter, QStyleOptionGraphicsItem, QWidget_widget=None):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # painter.setPen(self.symbolBorderPen)
        # painter.drawPath(self.symbolBorder)

        # draw the tank shape
        painter.setPen(self.tankBorderPen)
        painter.drawPath(self.tankBorder)
        painter.fillPath(self.tankBorder, QtGui.QColor(240, 240, 240))

        # draw the shape of the digit display
        painter.drawPath(self.digitBorder)
        painter.fillPath(self.digitBorder, QtGui.QColor(240, 240, 240))


        if self.isValueAboveLimit:
            # draw a warning text
            painter.drawText(self.warningTextRect,
                             QtCore.Qt.AlignHCenter or QtCore.Qt.AlignVCenter,
                             QtCore.QString(u"r\na\nn\ng\ne"))
        elif self.isValueBelowLimit:
            # draw a warning text
            painter.drawText(self.warningTextRect,
                             QtCore.Qt.AlignHCenter or QtCore.Qt.AlignVCenter,
                             QtCore.QString(u"r\na\nn\ng\ne"))
        else:
            # draw the tank level
            painter.fillPath(self.fillRect, self.tankColor)

        # configure text layout for the value
        painter.setPen(self.blackPen)
        painter.setFont(QtGui.QFont("Sans Serif", 12))

        if self.isRelativeScale:
            displayValueToShow = self.relativeDisplayValue
        else:
            displayValueToShow = self.absoluteDisplayValue

        painter.drawText(self.textRect,
                         QtCore.Qt.AlignRight or QtCore.Qt.AlignVCenter,
                         QtCore.QString(str(displayValueToShow)))

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.width + 40, self.height + 20)
