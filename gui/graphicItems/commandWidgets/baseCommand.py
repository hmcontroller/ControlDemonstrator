# -*- encoding: utf-8 -*-


from PyQt4 import QtGui, QtCore

from gui.constants import *

## @package baseCommand
#  This is the documentation for the baseCommand namespace, hm but it is only one class.
#
# Here are all the details about the baseCommand NAMESPACE and its thousands of classes.
#

## The BaseCommand class is the base class of all command widgets.
#
#  It sets up all needed signal slot connections to the core.command.Command class and
#  implements flags, that indicate the state of a command.
#
#  The state of a command can be



class BaseCommand(QtGui.QGraphicsObject):

    valueChanged = QtCore.pyqtSignal(float)

    ## Hallo Constructor
    def __init__(self, command):
        super(BaseCommand, self).__init__()

        ## holds the command model from core.command.Command
        self.command = command

        self.setAcceptHoverEvents(True)

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
        self.clearUserInputWarningTimer.timeout.connect(self.deactivateUserInputWarning)

        self.confirmationWarningBlinkTimer = QtCore.QTimer()
        self.confirmationWarningBlinkTimer.setSingleShot(False)
        self.confirmationWarningBlinkTimer.timeout.connect(self.toggleConfirmationFailureIndication)
        self.confirmationWarningBlinkInterval = 200
        self.confirmationWarningBlinkTimer.start(self.confirmationWarningBlinkInterval)

        self.negativeConfirmationWarningBlinkTimer = QtCore.QTimer()
        self.negativeConfirmationWarningBlinkTimer.setSingleShot(False)
        self.negativeConfirmationWarningBlinkTimer.timeout.connect(self.toggleNegativeConfirmationFailureIndication)
        self.negativeConfirmationBlinkInterval = 200

        self.clearNegativeConfirmationWarningTimer = QtCore.QTimer()
        self.clearNegativeConfirmationWarningTimer.setSingleShot(True)
        self.clearNegativeConfirmationWarningTimer.timeout.connect(self.clearNegativeConfirmationWarning)

        self.setValue(self.command.value)
        self.valueChanged.connect(self.command.setValue)

        self.command.minChangedFromController.connect(self.minChangedFromController)
        self.command.maxChangedFromController.connect(self.maxChangedFromController)

        self.command.confirmationTimeOut.connect(self.confirmationTimeOut)
        self.command.confirmation.connect(self.confirmation)
        self.command.negativeConfirmation.connect(self.negativeConfirmation)


    ## Meine Methodendokumentation
    #  @param self The instance pointer
    def activateUserInputWarning(self):
        self.showUserInputWarning = True
        self.clearUserInputWarningTimer.start(200)

    def deactivateUserInputWarning(self):
        self.showUserInputWarning = False

    def confirmationTimeOut(self):
        self.confirmationWarningBlinkTimer.start(self.confirmationWarningBlinkInterval)

    def confirmation(self):
        self.confirmationWarningBlinkTimer.stop()
        self.showConfirmationTimeoutWarning = False

    def negativeConfirmation(self):
        self.negativeConfirmationWarningBlinkTimer.start(self.negativeConfirmationBlinkInterval)
        self.clearNegativeConfirmationWarningTimer.start(2000)

    def toggleConfirmationFailureIndication(self):
        self.showConfirmationTimeoutWarning = not self.showConfirmationTimeoutWarning

    def toggleNegativeConfirmationFailureIndication(self):
        self.showNegativeConfirmationWarning = not self.showNegativeConfirmationWarning

    def clearNegativeConfirmationWarning(self):
        self.negativeConfirmationWarningBlinkTimer.stop()
        self.showNegativeConfirmationWarning = False

    ## Meine Methodendokumentation
    #  @param self The instance pointer
    #  @param command the command, that holds the min to be set to the gui
    def minChangedFromController(self, command):
        pass

    def maxChangedFromController(self, command):
        pass

    def setValue(self, value):
        self.value = value
        self.valueChanged.emit(self.value)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        raise NotImplementedError("abstract method paint must be overwritten")

    def boundingRect(self):
        raise NotImplementedError("abstract method boundingRect must be overwritten")

    def hoverEnterEvent(self, QGraphicsSceneMouseEvent):
        self.showHoverIndication = True

    def hoverLeaveEvent(self, QGraphicsSceneMouseEvent):
        self.showHoverIndication = False
