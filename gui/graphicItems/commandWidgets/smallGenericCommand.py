# -*- encoding: utf-8 -*-

import time

from PyQt4 import QtGui, QtCore

from baseCommand import BaseCommand
from gui.graphicItems.floatValidator import FloatValidator
from gui.graphicItems.lineEditDoubleClickSpecial import LineEditDoubleClickSpecial
from gui.graphicItems.button import SymbolButton
from gui.graphicItems.commandWidgets.smallGenericCommandSettingsWindow import SmallGenericCommandSettingsWindow


from gui.constants import *


class SmallGenericCommand(BaseCommand):
    def __init__(self, command):
        super(SmallGenericCommand, self).__init__(command)


        self.width = 400
        self.height = 70

        self.hValueSpace = 100
        self.vValueSpace = 25

        self.labelAreaHeight = 30
        self.editAreaHeight = self.height - self.labelAreaHeight

        self.editAreaHCenter = self.labelAreaHeight + 0.5 * self.editAreaHeight

        self.commandNameFont = QtGui.QFont("sans-serif", 12, QtGui.QFont.Bold)
        self.otherFont = QtGui.QFont("sans-serif", 12)
        self.redFont = QtGui.QFont("sans-serif", 12)
        self.pendingIndicationFont = QtGui.QFont("sans-serif", 12)
        self.pendingIndicationFont.setBold(True)
        self.blackPen = QtGui.QPen(QtCore.Qt.black)


        self.valueLineEdit = self._layoutLineEdit(LineEditDoubleClickSpecial())
        self.toggleButton = QtGui.QPushButton("1 -> 0")
        self.switchBox = QtGui.QCheckBox("1/0")
        self.switchBox.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.switchBox.setFont(self.otherFont)
        # self.switchBox.setStyleSheet(""".QCheckBox.indicator{ width:25px; height: 25px; } """)





        # the order of initializing the proxies affects the tab order

        self.valueLineEditProxy = QtGui.QGraphicsProxyWidget(self)
        self.valueLineEditProxy.setWidget(self.valueLineEdit)

        self.toggleButtonProxy = QtGui.QGraphicsProxyWidget(self)
        self.toggleButtonProxy.setWidget(self.toggleButton)

        self.switchBoxProxy = QtGui.QGraphicsProxyWidget(self)
        self.switchBoxProxy.setWidget(self.switchBox)


        # self.returnValueDisplayProxy = QtGui.QGraphicsProxyWidget(self)
        # self.returnValueDisplayProxy.setWidget(self.returnValueDisplay)




        self.commandNameLabelRect = QtCore.QRectF(10, 0, self.width - 50, self.labelAreaHeight)
        self.inputLabelRect = QtCore.QRectF(10, self.labelAreaHeight, 50, self.editAreaHeight)
        self.pendingLabelRect = QtCore.QRectF(55, self.labelAreaHeight, 10, self.editAreaHeight)
        self.returnLabelRect = QtCore.QRectF(230, self.labelAreaHeight, 50, self.editAreaHeight)
        self.returnValueRect = QtCore.QRectF(self.width - 10 - self.hValueSpace,
                                             self.editAreaHCenter - 0.5 * self.vValueSpace,
                                             self.hValueSpace,
                                             self.vValueSpace)


        self.valueLineEdit.move(75, self.editAreaHCenter - 0.5 * self.valueLineEdit.height())
        self.valueLineEditValidator = FloatValidator()
        self.valueLineEdit.setValidator(self.valueLineEditValidator)
        self.valueLineEdit.setText(str(self.command.getValue()))
        self.valueLineEdit.editingFinished.connect(self.valueEditingFinished)
        self.valueLineEdit.returnPressed.connect(self.valueEditingReturnPressed)
        self.valueLineEdit.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.toggleButton.setGeometry(70, self.editAreaHCenter - 0.3 * self.editAreaHeight,
                                      100, 0.6 * self.editAreaHeight)
        self.toggleButton.clicked.connect(self.switchToOneAndThenToZero)
        self.toggleButton.hide()


        self.switchBox.setGeometry(70, self.editAreaHCenter - 0.3 * self.editAreaHeight,
                                      100, 0.6 * self.editAreaHeight)

        if self.command.getValue() > 0.5:
            self.switchBox.setChecked(True)
        else:
            self.switchBox.setChecked(False)
        self.switchBox.stateChanged.connect(self.toggleOneAndZero)
        self.switchBox.hide()

        # self.returnValueDisplay.move(self.width - 10 - self.returnValueDisplay.width(),
        #                              self.editAreaHCenter - 0.5 * self.valueLineEdit.height())
        # self.returnValueDisplay.setText(str(self.command.getValue()))
        # self.returnValueDisplay.setStyleSheet(
        #     """.LineEditDoubleClickSpecial { background-color: lightgray;
        #                                      border-style: solid;
        #                                      border-color: black; }""")








        self.settingsButton = SymbolButton(SymbolButton.SETTINGS, self)
        self.settingsButton.setPos(self.width - self.settingsButton.boundingRect().width() - 5, 2)
        self.settingsButton.drawBorder = False
        self.settingsButton.clicked.connect(self.showSettingsWindow)

        self.settingsWindow = SmallGenericCommandSettingsWindow()
        self.settingsWindow.lineEditMin.setValidator(FloatValidator())
        self.settingsWindow.lineEditMax.setValidator(FloatValidator())



        self.onePixelGrayPen = QtGui.QPen()
        self.onePixelGrayPen.setWidth(1)
        self.onePixelGrayPen.setCosmetic(True)
        self.onePixelGrayPen.setColor(QtCore.Qt.darkGray)

        self.pendingValuePen = QtGui.QPen()
        self.pendingValuePen.setColor(PENDING_VALUE_COLOR)
        self.pendingValuePenGray = QtGui.QPen()
        self.pendingValuePenGray.setColor(QtCore.Qt.darkGray)

        self.boundingRectPath = QtGui.QPainterPath()
        self.boundingRectPath.addRect(0, 0, 200, self.height)

        self.headerAreaPath = QtGui.QPainterPath()
        self.headerAreaPath.addRect(0, 0, self.width, self.labelAreaHeight)
        self.headerAreaBrush = QtGui.QBrush(QtGui.QColor(0, 153, 153, 50))

        self.editAreaPath = QtGui.QPainterPath()
        self.editAreaPath.addRect(0, self.labelAreaHeight, self.width, self.editAreaHeight)
        self.editAreaBrush = QtGui.QBrush(QtGui.QColor(0, 153, 250, 30))

        self.returnValueRectPath = QtGui.QPainterPath()
        self.returnValueRectPath.addRect(self.returnValueRect)

        self.littleTimer = QtCore.QTimer()
        self.littleTimer.setSingleShot(True)
        self.littleTimer.timeout.connect(self.switchToZero)


    def _layoutLineEdit(self, lineEdit):

        lineEdit.setFixedSize(self.hValueSpace, self.vValueSpace)
        p = QtGui.QPalette()
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(QtGui.QColor(0,0,0,0)))
        # label.setStyleSheet("""border: none; background-color: rgba(0, 0, 0, 0);""")     #; margin-top: 8px """)
        lineEdit.setPalette(p)
        # lineEdit.move(self.width - 10 - self.valueLineEdit.width(), self.labelAreaHeight + 0.5 * self.editAreaHeight - 0.5 * self.valueLineEdit.height())
        # lineEdit.setText("0.0")
        # lineEdit.setMaxLength(6)
        lineEdit.setFont(QtGui.QFont("sans-serif", 12))
        return lineEdit

    def switchToOneAndThenToZero(self):
        self.command.setValue(1.0)
        self.littleTimer.start(100)

    def switchToZero(self):
        self.command.setValue(0.0)

    def toggleOneAndZero(self):
        newState = self.switchBox.checkState()

        if newState > 0:
            self.command.setValue(1.0)
        else:
            self.command.setValue(0.0)

    def showSettingsWindow(self):
        self.settingsWindow.lineEditDisplayName.setText(self.command.displayName)
        self.settingsWindow.lineEditMin.setText(str(self.command.getLowerLimit()))
        self.settingsWindow.lineEditMax.setText(str(self.command.getUpperLimit()))

        if self.valueLineEdit.isVisible():
            self.settingsWindow.radioButtonValueMode.setChecked(True)
        elif self.toggleButton.isVisible():
            self.settingsWindow.radioButtonToggleMode.setChecked(True)
        elif self.switchBox.isVisible():
            self.settingsWindow.radioButtonSwitchMode.setChecked(True)

        self.settingsWindow.checkBoxPendingMode.setChecked(self.command.getPendingSendMode())

        if self.settingsWindow.exec_() == QtGui.QDialog.Accepted:
            self.setSettingsFromSettingsWindow()
        else:
            pass

    def setSettingsFromSettingsWindow(self):


        self.valueLineEdit.hide()
        self.toggleButton.hide()
        self.switchBox.hide()
        if self.settingsWindow.radioButtonValueMode.isChecked() is True:
            self.valueLineEdit.show()
        if self.settingsWindow.radioButtonSwitchMode.isChecked() is True:
            self.switchBox.show()
        if self.settingsWindow.radioButtonToggleMode.isChecked() is True:
            self.toggleButton.show()

        self.command.displayName = unicode(self.settingsWindow.lineEditDisplayName.text())
        self.command.setPendingSendMode(self.settingsWindow.checkBoxPendingMode.isChecked())

        minText = self.settingsWindow.lineEditMin.text()
        self.setMinimum(minText)

        maxText = self.settingsWindow.lineEditMax.text()
        self.setMaximum(maxText)
        self.update()

    # TODO move to settings window
    def setMinimum(self, text):
        if text == "":
            min = 0
        else:
            min = float(text)
        if min > self.command.getUpperLimit():
            self.command.setLowerLimit(self.command.getUpperLimit(), self)
        else:
            self.command.setLowerLimit(min, self)

    def setMaximum(self, text):
        if text == "":
            max = 0
        else:
            max = float(text)

        if max < self.command.getLowerLimit():
            self.command.setUpperLimit(self.command.getLowerLimit(), self)
        else:
            self.command.setUpperLimit(max, self)

    def valueEditingFinished(self):
        pass

    def valueEditingReturnPressed(self):
        text = self.valueLineEdit.text()
        print "command given", text

        # if nothing is in the textBox, the lower limit of the command will be set
        if len(text) is 0:
            self.valueLineEdit.setText(str(self.command.getLowerLimit()))
            self.valueLineEdit.setCursorPosition(0)
            self.valueLineEdit.selectAll()
            self.activateUserInputWarning()
        else:
            # allowed for the decimal point are a comma and a dot
            text = text.replace(",", ".")

            number = float(text)
            if number < self.command.getLowerLimit():
                self.valueLineEdit.setText(str(self.command.getLowerLimit()))
                self.valueLineEdit.setCursorPosition(0)
                self.valueLineEdit.selectAll()
                self.activateUserInputWarning()
            elif number > self.command.getUpperLimit():
                self.valueLineEdit.setText(str(self.command.getUpperLimit()))
                self.valueLineEdit.setCursorPosition(0)
                self.valueLineEdit.selectAll()
                self.activateUserInputWarning()
            else:
                self.command.setValue(number, self)

        # TODO how to set color back to black
        # if self.command.getPendingSendMode() is True:
        #     self.valueLineEdit.setStyleSheet(""".LineEditDoubleClickSpecial { color: red; }""")



        # self.valueLineEdit.setText(str(self.command.getValue()))
        # self.valueLineEdit.setCursorPosition(0)
        self.valueLineEdit.selectAll()

    def valueChangedPerWidget(self, widgetInstance):
        pass

    def minChangedPerWidget(self, widgetInstance):
        pass

    def maxChangedPerWidget(self, widgetInstance):
        pass

    def sameValueReceived(self):
        super(SmallGenericCommand, self).sameValueReceived()
        # self.returnValueDisplay.setStyleSheet(
        #     """.LineEditDoubleClickSpecial { background-color: lightgray;
        #                                      border-style: solid;
        #                                      border-color: black; }""")
        self.update()

    # overwrites method of super class
    def differentValueReceived(self):
        # this call is needed to start the blink timer
        super(SmallGenericCommand, self).differentValueReceived()

        # self.returnValueDisplay.setStyleSheet(
        #     """.LineEditDoubleClickSpecial { background-color: red;
        #                                      border-style: solid;
        #                                      border-color: black; }""")



        # self.valueLineEdit.setText(str(self.command.getValue()))
        # self.valueLineEdit.setCursorPosition(0)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        # draw background of the label
        QPainter.fillPath(self.headerAreaPath, self.headerAreaBrush)

        # draw background of edit area
        QPainter.fillPath(self.editAreaPath, self.editAreaBrush)


        # draw a warning
        if self.showUserInputWarning is True:
            QPainter.fillPath(self.editAreaPath, self.userInputWarningBrush)

        # draw a warning
        if self.showCommFailureWarning is True:
            QPainter.fillPath(self.editAreaPath, self.commFailureWarningBrush)

        # draw this warning in front of all other colors
        if self.showDifferentValueReceivedWarning is True:
            QPainter.fillPath(self.editAreaPath, self.differentValueReceivedWarningBrush)

        # draw background of return value
        QPainter.fillPath(self.returnValueRectPath, QtGui.QBrush(QtGui.QColor(200, 200, 200)))

        # draw return value
        QPainter.setFont(self.otherFont)
        QPainter.drawText(self.returnValueRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         QtCore.QString(str(self.command.valueOfLastResponse)))

        QPainter.setPen(self.blackPen)

        # draw the command name
        QPainter.setFont(self.commandNameFont)
        if self.command.displayName is not None:
            QPainter.drawText(self.commandNameLabelRect,
                             QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                             QtCore.QString(self.command.displayName))
        else:
            QPainter.drawText(self.commandNameLabelRect,
                             QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                             QtCore.QString(self.command.name))

        # draw some text
        QPainter.setFont(self.otherFont)
        QPainter.drawText(self.inputLabelRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         QtCore.QString(u"Input"))

        # draw pending mode indication
        if self.command.getPendingSendMode() is True:
            QPainter.setPen(self.pendingValuePen)
        else:
            QPainter.setPen(self.pendingValuePenGray)

        QPainter.setFont(self.pendingIndicationFont)
        QPainter.drawText(self.pendingLabelRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         QtCore.QString(u"P"))
        QPainter.setPen(self.blackPen)


        # # TODO very dirty hack here
        # self.returnValueDisplay.setText(str(self.command.valueOfLastResponse))
        # self.returnValueDisplay.setCursorPosition(0)



        # draw some text
        QPainter.setFont(self.otherFont)
        QPainter.drawText(self.returnLabelRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         QtCore.QString(u"aktuell"))

        # draw bounding paths
        QPainter.setPen(self.onePixelGrayPen)
        QPainter.drawPath(self.headerAreaPath)
        QPainter.drawPath(self.editAreaPath)


    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.width, self.height)



