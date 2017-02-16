# -*- encoding: utf-8 -*-


from PyQt4 import QtGui, QtCore

from baseCommand import BaseCommand
from gui.graphicItems.floatValidator import FloatValidator
from gui.graphicItems.lineEditDoubleClickSpecial import LineEditDoubleClickSpecial

from gui.constants import *


class GenericCommand(BaseCommand):

    valueChanged = QtCore.pyqtSignal(float)

    def __init__(self, command):

        self.minLineEdit = self._addLineEdit(LineEditDoubleClickSpecial())
        self.maxLineEdit = self._addLineEdit(LineEditDoubleClickSpecial())
        self.valueLineEdit = self._addLineEdit(LineEditDoubleClickSpecial())

        super(GenericCommand, self).__init__(command)

        self.valueLineEditProxy = QtGui.QGraphicsProxyWidget(self)
        self.valueLineEditProxy.setWidget(self.valueLineEdit)

        self.minLineEditProxy = QtGui.QGraphicsProxyWidget(self)
        self.minLineEditProxy.setWidget(self.minLineEdit)

        self.maxLineEditProxy = QtGui.QGraphicsProxyWidget(self)
        self.maxLineEditProxy.setWidget(self.maxLineEdit)



        self.width = 400
        self.height = 80
        self.labelAreaHeight = 30
        self.editAreaHeight = self.height - self.labelAreaHeight



        self.hCenterEditArea = self.labelAreaHeight + 0.5 * self.editAreaHeight

        self.minLineEdit.move(45, self.labelAreaHeight + 0.5 * self.editAreaHeight - 0.5 * self.minLineEdit.height())
        self.minLineEditValidator = FloatValidator()
        self.minLineEdit.setValidator(self.minLineEditValidator)
        self.minLineEdit.editingFinished.connect(self.minEditingFinished)
        self.minLineEdit.setText(str(self.command.lowerLimit))

        self.maxLineEdit.move(167, self.labelAreaHeight + 0.5 * self.editAreaHeight - 0.5 * self.minLineEdit.height())
        self.maxLineEditValidator = FloatValidator()
        self.maxLineEdit.setValidator(self.maxLineEditValidator)
        self.maxLineEdit.editingFinished.connect(self.maxEditingFinished)
        self.maxLineEdit.setText(str(self.command.upperLimit))

        self.valueLineEdit.move(self.width - 10 - self.valueLineEdit.width(), self.hCenterEditArea - 0.5 * self.valueLineEdit.height())
        self.valueLineEditValidator = FloatValidator()
        self.valueLineEdit.setValidator(self.valueLineEditValidator)
        self.valueLineEdit.editingFinished.connect(self.valueEditingFinished)


        self.boundingRectPath = QtGui.QPainterPath()
        self.boundingRectPath.addRect(0, 0, 200, self.height)

        self.headerAreaPath = QtGui.QPainterPath()
        self.headerAreaPath.addRect(0, 0, self.width, self.labelAreaHeight)
        self.headerAreaBrush = QtGui.QBrush(QtGui.QColor(0, 153, 153, 50))

        self.editAreaPath = QtGui.QPainterPath()
        self.editAreaPath.addRect(0, self.labelAreaHeight, self.width, self.editAreaHeight)
        self.editAreaBrush = QtGui.QBrush(QtGui.QColor(0, 153, 250, 30))

        self.commandNameFont = QtGui.QFont("sans-serif", 12, QtGui.QFont.Bold)
        self.otherFont = QtGui.QFont("sans-serif", 12)
        self.blackPen = QtGui.QPen(QtCore.Qt.black)

        self.labelRect = QtCore.QRectF(10, 0, self.width - 10, self.labelAreaHeight)
        self.minRect = QtCore.QRectF(10, self.labelAreaHeight, 50, self.editAreaHeight)
        self.maxRect = QtCore.QRectF(130, self.labelAreaHeight, 50, self.editAreaHeight)
        self.valueRect = QtCore.QRectF(280, self.labelAreaHeight, 50, self.editAreaHeight)

        self.onePixelGrayPen = QtGui.QPen()
        self.onePixelGrayPen.setWidth(1)
        self.onePixelGrayPen.setCosmetic(True)
        self.onePixelGrayPen.setColor(QtCore.Qt.darkGray)

    def _addLineEdit(self, lineEdit):
        lineEdit.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        lineEdit.setFixedSize(63, 25)
        p = QtGui.QPalette()
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(QtGui.QColor(0,0,0,0)))
        # label.setStyleSheet("""border: none; background-color: rgba(0, 0, 0, 0);""")     #; margin-top: 8px """)
        lineEdit.setPalette(p)
        # lineEdit.move(self.width - 10 - self.valueLineEdit.width(), self.labelAreaHeight + 0.5 * self.editAreaHeight - 0.5 * self.valueLineEdit.height())
        lineEdit.setText("0.0")
        # lineEdit.setMaxLength(6)
        lineEdit.setFont(QtGui.QFont("sans-serif", 12))
        return lineEdit

    def valueEditingFinished(self):
        self.valueLineEditProxy.clearFocus()

        text = self.valueLineEdit.text()
        print "Editfinished", text

        if text == "":
            self.valueLineEdit.setText(str(self.command.lowerLimit))
            self.valueChanged.emit(self.command.lowerLimit)
            self.showUserInputWarning()
            return

        text = text.replace(",", ".")

        number = float(text)
        if number < self.command.lowerLimit:
            self.valueLineEdit.setText(str(self.command.lowerLimit))
            self.valueChanged.emit(self.command.lowerLimit)
            self.showUserInputWarning()
        elif number > self.command.upperLimit:
            self.valueChanged.emit(self.command.upperLimit)
            self.valueLineEdit.setText(str(self.command.upperLimit))
            self.showUserInputWarning()
        else:
            self.valueChanged.emit(number)

    def minEditingFinished(self):
        self.minLineEditProxy.clearFocus()

        text = self.minLineEdit.text()
        if text == "":
            min = 0
        else:
            min = float(text)
        self.command.lowerLimit = min

    def maxEditingFinished(self):
        self.maxLineEditProxy.clearFocus()

        text = self.maxLineEdit.text()
        if text == "":
            max = 0
        else:
            max = float(text)
        self.command.upperLimit = max

    def setValue(self, value):
        self.valueLineEdit.setText(str(value))

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        # draw background of the label
        QPainter.fillPath(self.headerAreaPath, self.headerAreaBrush)

        # draw background of edit area
        QPainter.fillPath(self.editAreaPath, self.editAreaBrush)

        # draw red in front of gray
        if self.showUserInputWarning is True:
            QPainter.fillPath(self.editAreaPath, self.userInputWarningBrush)

        # draw confirmation warning in front of all other colors
        if self.showConfirmationTimeoutWarning is True:
            QPainter.fillPath(self.editAreaPath, self.unconfirmedWarningBrush)

        QPainter.setPen(self.blackPen)

        # draw the command name
        QPainter.setFont(self.commandNameFont)
        QPainter.drawText(self.labelRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         QtCore.QString(self.command.name))

        # draw some text
        QPainter.setFont(self.otherFont)
        QPainter.drawText(self.minRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         QtCore.QString("min"))

        # draw some text
        QPainter.drawText(self.maxRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         QtCore.QString("max"))

        # draw some text
        QPainter.drawText(self.valueRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         QtCore.QString("value"))

        # draw bounding paths
        QPainter.setPen(self.onePixelGrayPen)
        QPainter.drawPath(self.headerAreaPath)
        QPainter.drawPath(self.editAreaPath)


    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.width, self.height)

