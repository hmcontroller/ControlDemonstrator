# -*- encoding: utf-8 -*-


from PyQt4 import QtGui, QtCore

from baseCommand import BaseCommand
from gui.graphicItems.floatValidator import FloatValidator
from gui.graphicItems.lineEditDoubleClickSpecial import LineEditDoubleClickSpecial

from gui.constants import *


class GenericCommand(BaseCommand):
    def __init__(self, command):

        self.commandNameFont = QtGui.QFont("sans-serif", 12, QtGui.QFont.Bold)
        self.otherFont = QtGui.QFont("sans-serif", 12)
        self.blackPen = QtGui.QPen(QtCore.Qt.black)


        self.minLineEdit = self._addLineEdit(LineEditDoubleClickSpecial())
        self.maxLineEdit = self._addLineEdit(LineEditDoubleClickSpecial())
        self.valueLineEdit = self._addLineEdit(LineEditDoubleClickSpecial())
        self.valueLineEdit.downArrowPressed.connect(self.showHistory)

        self.pendingStateCheckbox = QtGui.QCheckBox()
        self.pendingStateCheckbox.setText("Guggu")
        self.pendingStateCheckbox.setFont(self.otherFont)
        self.pendingStateCheckbox.setGeometry(0, 0, 150, 20)
        self.pendingStateCheckbox.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # self.minLineEdit.lostFocus.connect(self.minLostFocus)

        super(GenericCommand, self).__init__(command)

        # the order of initializing the proxies affects the tab order
        self.minLineEditProxy = QtGui.QGraphicsProxyWidget(self)
        self.minLineEditProxy.setWidget(self.minLineEdit)

        self.maxLineEditProxy = QtGui.QGraphicsProxyWidget(self)
        self.maxLineEditProxy.setWidget(self.maxLineEdit)

        self.valueLineEditProxy = QtGui.QGraphicsProxyWidget(self)
        self.valueLineEditProxy.setWidget(self.valueLineEdit)

        self.pendingStateCheckboxProxy = QtGui.QGraphicsProxyWidget(self)
        self.pendingStateCheckboxProxy.setWidget(self.pendingStateCheckbox)

        self.width = 400
        self.height = 100
        self.labelAreaHeight = 30
        self.editAreaHeight = self.height - self.labelAreaHeight

        self.hCenterEditArea = self.labelAreaHeight + 0.5 * self.editAreaHeight

        # self.minLineEdit.move(45, self.labelAreaHeight + 0.5 * self.editAreaHeight - 0.5 * self.minLineEdit.height())
        self.minLineEdit.move(45, self.labelAreaHeight + 0.5 * self.editAreaHeight - 1.1 * self.minLineEdit.height())
        self.minLineEditValidator = FloatValidator()
        self.minLineEdit.setValidator(self.minLineEditValidator)
        self.minLineEdit.setText(str(self.command.getLowerLimit()))

        self.minLineEdit.editingFinished.connect(self.minEditingFinished)
        self.minLineEdit.returnPressed.connect(self.minEditingReturnPressed)

        # self.maxLineEdit.move(167, self.labelAreaHeight + 0.5 * self.editAreaHeight - 0.5 * self.minLineEdit.height())
        self.maxLineEdit.move(45, self.labelAreaHeight + 0.5 * self.editAreaHeight + 0.1 * self.minLineEdit.height())
        self.maxLineEditValidator = FloatValidator()
        self.maxLineEdit.setValidator(self.maxLineEditValidator)
        self.maxLineEdit.setText(str(self.command.getUpperLimit()))

        self.maxLineEdit.editingFinished.connect(self.maxEditingFinished)
        self.maxLineEdit.returnPressed.connect(self.maxEditingReturnPressed)


        self.valueLineEdit.move(self.width - 10 - self.valueLineEdit.width(), self.labelAreaHeight + 0.5 * self.editAreaHeight - 1.1 * self.minLineEdit.height())
        self.valueLineEditValidator = FloatValidator()
        self.valueLineEdit.setValidator(self.valueLineEditValidator)
        self.valueLineEdit.setText(str(self.command.getValue()))

        self.valueLineEdit.editingFinished.connect(self.valueEditingFinished)
        self.valueLineEdit.returnPressed.connect(self.valueEditingReturnPressed)

        self.pendingStateCheckbox.setCheckState(self.command.getPendingSendMode())
        self.pendingStateCheckbox.move(45 + self.minLineEdit.width() + 10, self.labelAreaHeight + 10)# + 0.5 * self.editAreaHeight)
        self.pendingStateCheckbox.setTristate(False)
        self.pendingStateCheckbox.clicked.connect(self.pendingCheckboxClicked)

        # no text is drawn when the
        self.pendingStateCheckbox.setText(u"pending mode")

        self.boundingRectPath = QtGui.QPainterPath()
        self.boundingRectPath.addRect(0, 0, 200, self.height)

        self.headerAreaPath = QtGui.QPainterPath()
        self.headerAreaPath.addRect(0, 0, self.width, self.labelAreaHeight)
        self.headerAreaBrush = QtGui.QBrush(QtGui.QColor(0, 153, 153, 50))

        self.editAreaPath = QtGui.QPainterPath()
        self.editAreaPath.addRect(0, self.labelAreaHeight, self.width, self.editAreaHeight)
        self.editAreaBrush = QtGui.QBrush(QtGui.QColor(0, 153, 250, 30))


        self.labelRect = QtCore.QRectF(10, 0, self.width - 10, self.labelAreaHeight)
        # self.minRect = QtCore.QRectF(10, self.labelAreaHeight, 50, self.editAreaHeight)
        # self.maxRect = QtCore.QRectF(130, self.labelAreaHeight, 50, self.editAreaHeight)
        # self.valueRect = QtCore.QRectF(280, self.labelAreaHeight, 50, self.editAreaHeight)
        self.minRect = QtCore.QRectF(5, 15, 50, self.editAreaHeight)
        self.maxRect = QtCore.QRectF(5, 45, 50, self.editAreaHeight)
        self.valueRect = QtCore.QRectF(280, 45, 50, self.editAreaHeight)
        self.pendingRect = QtCore.QRectF(45 + self.minLineEdit.width() + 30, self.labelAreaHeight + 10, 150, 100)
        self.pendingValueRect = QtCore.QRectF(45 + self.minLineEdit.width() + 10, self.labelAreaHeight + 40, 155, 100)
        self.valueFromControllerRect = QtCore.QRectF(self.width - 10 - self.valueLineEdit.width(),
                                                     self.labelAreaHeight + 0.5 * self.editAreaHeight + 0.1 * self.minLineEdit.height(),
                                                     63,
                                                     25)

        self.onePixelGrayPen = QtGui.QPen()
        self.onePixelGrayPen.setWidth(1)
        self.onePixelGrayPen.setCosmetic(True)
        self.onePixelGrayPen.setColor(QtCore.Qt.darkGray)

        self.pendingValuePen = QtGui.QPen()
        self.pendingValuePen.setColor(PENDING_VALUE_COLOR)


        # timer needed to stop a started userInputWarning
        self.clearUserInputWarningTimer = QtCore.QTimer()
        self.clearUserInputWarningTimer.setSingleShot(True)
        self.clearUserInputWarningTimer.timeout.connect(self.clearUserInputWarning)
        self.userInputWarningDuration = 1000


    # def minLostFocus(self):
    #     self.triggerNoChangeWarning()
    #     self.minLineEdit.setText(self.minLineEdit.oldValueText)
    #
    # def triggerNoChangeWarning(self):
    #     pass

    def showHistory(self):
        print self.command.history

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

    def pendingCheckboxClicked(self, newValue):
        self.command.setPendingSendMode(newValue)

    def valueEditingFinished(self):
        text = self.valueLineEdit.text()

        # if nothing is in the textBox, the lower limit of the command will be set
        if len(text) is 0:
            self.valueLineEdit.setText(str(self.command.getLowerLimit()))
            self.valueLineEdit.setCursorPosition(0)
            self.command.setValue(self.command.getLowerLimit(), self)
            self.activateUserInputWarning()
        else:
            # allowed for the decimal point are a comma and a dot
            text = text.replace(",", ".")

            number = float(text)
            if number < self.command.getLowerLimit():
                self.command.setValue(self.command.getLowerLimit(), self)
                self.valueLineEdit.setText(str(self.command.getLowerLimit()))
                self.valueLineEdit.setCursorPosition(0)
                self.activateUserInputWarning()
            elif number > self.command.getUpperLimit():
                self.command.setValue(self.command.getUpperLimit(), self)
                self.valueLineEdit.setText(str(self.command.getUpperLimit()))
                self.valueLineEdit.setCursorPosition(0)
                self.activateUserInputWarning()
            else:
                self.command.setValue(number, self)

        # self.valueLineEdit.setText(str(self.command.getValue()))
        # self.valueLineEdit.setCursorPosition(0)
        self.update()

    def activateUserInputWarning(self):
        super(GenericCommand, self).activateUserInputWarning()
        self.clearUserInputWarningTimer.start(self.userInputWarningDuration)


    def valueEditingReturnPressed(self):
        self.valueLineEdit.selectAll()

    def minEditingFinished(self):
        # self.minLineEditProxy.clearFocus()
        # self.minLineEdit.selectAll()


        text = self.minLineEdit.text()

        if text == "":
            min = 0
        else:
            min = float(text)
        if min > self.command.getUpperLimit():
            self.command.setLowerLimit(self.command.getUpperLimit(), self)
            self.minLineEdit.setText(str(self.command.getLowerLimit()))
            self.minLineEdit.setCursorPosition(0)
            self.minLineEdit.selectAll()
            self.activateUserInputWarning()
        else:
            self.command.setLowerLimit(min, self)

    def minEditingReturnPressed(self):
        self.minLineEdit.selectAll()

    def maxEditingFinished(self):
        # self.maxLineEditProxy.clearFocus()
        # self.maxLineEdit.selectAll()

        text = self.maxLineEdit.text()

        if text == "":
            max = 0
        else:
            max = float(text)

        if max < self.command.getLowerLimit():
            self.command.setUpperLimit(self.command.getLowerLimit(), self)
            self.maxLineEdit.setText(str(self.command.getUpperLimit()))
            self.maxLineEdit.setCursorPosition(0)
            self.maxLineEdit.selectAll()
            self.activateUserInputWarning()
        else:
            self.command.setUpperLimit(max, self)

    def maxEditingReturnPressed(self):
        self.maxLineEdit.selectAll()

    def valueChangedPerWidget(self, widgetInstance):
        if widgetInstance is self:
            pass
        else:
            pass
            # self.valueLineEdit.setText(str(self.command.getValue()))
            # self.valueLineEdit.setCursorPosition(0)


    def minChangedPerWidget(self, widgetInstance):
        if widgetInstance is self:
            pass
        else:
            self.minLineEdit.setText(str(self.command.getLowerLimit()))
            self.minLineEdit.setCursorPosition(0)

    def maxChangedPerWidget(self, widgetInstance):
        if widgetInstance is self:
            pass
        else:
            self.maxLineEdit.setText(str(self.command.getUpperLimit()))
            self.maxLineEdit.setCursorPosition(0)
            self.update()

    @QtCore.pyqtSlot()
    def pendingModeChanged(self, command):
        super(GenericCommand, self).pendingModeChanged(command)
        self.pendingStateCheckbox.setChecked(self.command.getPendingSendMode())

    # overwrites method of super class
    def differentValueReceived(self):
        # this call is needed to start the blink timer
        super(GenericCommand, self).differentValueReceived()

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

        QPainter.setPen(self.blackPen)

        # draw the command name
        QPainter.setFont(self.commandNameFont)
        if len(self.command.displayName) > 0:
            QPainter.drawText(self.labelRect,
                             QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                             QtCore.QString(self.command.displayName))
        else:
            QPainter.drawText(self.labelRect,
                             QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                             QtCore.QString(self.command.name))

        # draw some text
        QPainter.setFont(self.otherFont)
        QPainter.drawText(self.minRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         QtCore.QString("min"))

        # # draw some text
        # QPainter.setFont(self.otherFont)
        # QPainter.drawText(self.pendingRect,
        #                  QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
        #                  QtCore.QString("pending mode"))

        # draw some text
        if self.command._pendingValue is not None:
            QPainter.setPen(self.pendingValuePen)
            pendingValue = unicode(self.command._pendingValue) + u"  -->"
            QPainter.setFont(self.otherFont)
            QPainter.drawText(self.pendingValueRect,
                             QtCore.Qt.AlignRight | QtCore.Qt.AlignTop,
                             QtCore.QString(pendingValue))
            QPainter.setPen(self.blackPen)

        # draw some text
        QPainter.setFont(self.otherFont)
        QPainter.drawText(self.valueFromControllerRect,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         QtCore.QString(str(self.command.valueOfLastResponse)))

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



class GenericCommandWithoutMinMaxEdit(GenericCommand):
    def __init__(self, command):
        super(GenericCommandWithoutMinMaxEdit, self).__init__(command)
        self.minLineEdit.setReadOnly(True)
        self.maxLineEdit.setReadOnly(True)

        self.minLineEditProxy.setFocusPolicy(QtCore.Qt.NoFocus)
        self.maxLineEditProxy.setFocusPolicy(QtCore.Qt.NoFocus)

        styleSheet = """border: none; background-color: rgba(0, 0, 0, 0);"""
        # styleSheet = """border: none; color: rgb(120, 120, 120); background-color: rgba(0, 0, 0, 0);"""

        p = QtGui.QPalette()
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(QtGui.QColor(0,0,0,0)))

        p = QtGui.QPalette()
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(QtGui.QColor(0,0,0,0)))

        self.minLineEdit.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.minLineEdit.setStyleSheet(styleSheet)
        self.minLineEdit.setPalette(p)

        self.maxLineEdit.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.maxLineEdit.setStyleSheet(styleSheet)
        self.maxLineEdit.setPalette(p)

        self.pendingStateCheckbox.hide()
