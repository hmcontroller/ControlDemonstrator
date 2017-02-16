# -*- encoding: utf-8 -*-


from PyQt4 import QtGui, QtCore

from gui.constants import *


class BaseCommand(QtGui.QGraphicsObject):

    valueChanged = QtCore.pyqtSignal(float)

    def __init__(self, command):
        super(BaseCommand, self).__init__()

        self.command = command

        self.showHoverIndication = False
        self.showUserInputWarning = False
        self.showConfirmationTimeoutWarning = False
        self.showNegativeConfirmationWarning = False

        self.userInputWarningBrush = QtGui.QBrush(USER_INPUT_WARNING_COLOR)
        self.unconfirmedWarningBrush = QtGui.QBrush(CONFIRMATION_TIMEOUT_WARNING_COLOR)
        self.negativeConfirmedWarningBrush = QtGui.QBrush(NEGATIVE_CONFIRMATION_WARNING_COLOR)
        self.hoverBrush = QtGui.QBrush(HOVER_COLOR)

        self.cablePen = CABLE_PEN

        self.clearUserInputWarningTimer = QtCore.QTimer()
        self.clearUserInputWarningTimer.setSingleShot(True)
        self.clearUserInputWarningTimer.timeout.connect(self.clearUserInputWarning)

        self.confirmationWarningBlinkTimer = QtCore.QTimer()
        self.confirmationWarningBlinkTimer.setSingleShot(False)
        self.confirmationWarningBlinkTimer.timeout.connect(self.toggleConfirmationFailureIndication)
        self.confirmationWarningBlinkInterval = 200
        self.confirmationWarningBlinkTimer.start(self.confirmationWarningBlinkInterval)

        self.negativeConfirmationWarningBlinkTimer = QtCore.QTimer()
        self.negativeConfirmationWarningBlinkTimer.setSingleShot(False)
        self.negativeConfirmationWarningBlinkTimer.timeout.connect(self.toggleNegativeConfirmationFailureIndication)
        self.negativeConfirmationBlinkInterval = 200

        self.setValue(self.command.value)
        self.valueChanged.connect(self.command.setValue)

        self.command.confirmationTimeOut.connect(self.confirmationTimeOut)
        self.command.confirmation.connect(self.confirmation)
        self.command.negativeConfirmation.connect(self.negativeConfirmation)

    def showUserInputWarning(self):
        self.showUserInputWarning = True
        self.clearUserInputWarningTimer.start(200)

    def clearUserInputWarning(self):
        self.showUserInputWarning = False

    def confirmationTimeOut(self):
        self.confirmationWarningBlinkTimer.start(self.confirmationWarningBlinkInterval)

    def confirmation(self):
        self.confirmationWarningBlinkTimer.stop()
        self.showConfirmationTimeoutWarning = False

    def negativeConfirmation(self):
        self.negativeConfirmationWarningBlinkTimer.start(self.negativeConfirmationBlinkInterval)
        self.setValue(self.command.value)

    # def negativeConfirmation(self):
    #     raise NotImplementedError(
    #         "abstract method negativeConfirmation must be overwritten.\n "
    #         "Put this line at the beginning:\n "
    #         "self.negativeConfirmationWarningBlinkTimer.start(self.negativeConfirmationBlinkInterval).")

    def toggleConfirmationFailureIndication(self):
        self.showConfirmationTimeoutWarning = not self.showConfirmationTimeoutWarning

    def toggleNegativeConfirmationFailureIndication(self):
        self.showNegativeConfirmationWarning = not self.showNegativeConfirmationWarning

    def setValue(self, value):
        self.value = value
        self.valueChanged.emit(self.value)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        raise NotImplementedError("abstract method paint must be overwritten")

    def boundingRect(self):
        raise NotImplementedError("abstract method boundingRect must be overwritten")
