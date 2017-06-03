# -*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from gui.designerfiles.applicationSettingsDialog import Ui_ApplicationSettingsDialog
from core.model.applicationSettings import ApplicationSettings

class ApplicationSettingsDialog(QtGui.QDialog, Ui_ApplicationSettingsDialog):
    def __init__(self, settings, parent=None):
        super(ApplicationSettingsDialog, self).__init__(parent)
        self.settings = settings
        self.setupUi(self)


        self.lineEditBufferLength.setValidator(QtGui.QIntValidator(1, 100000))


        self.buttonBox.accepted.connect(self.verifyInput)
        self.buttonBox.rejected.connect(self.dialogRejected)

        self.openedDialog = None


    @staticmethod
    def updateSettings(settings, portChanged=False):

        dialog = ApplicationSettingsDialog(settings)

        # set settings to form
        dialog.lineEditBufferLength.setText(unicode(dialog.settings.bufferLength))

        if dialog.settings.guiUpdateIntervalLengthInMs != 0:
            frameRate = 1000 / dialog.settings.guiUpdateIntervalLengthInMs
        else:
            frameRate = 40
        dialog.spinBoxGuiUpdateFrameRate.setValue(frameRate)

        if dialog.settings.autoSaveAfterCodeGeneration is True:
            dialog.checkBoxAutosaveAfterCodeGeneration.setCheckState(QtCore.Qt.Checked)
        else:
            dialog.checkBoxAutosaveAfterCodeGeneration.setCheckState(QtCore.Qt.Unchecked)

        answer = dialog.exec_()

        if answer == QtGui.QDialog.Accepted:
            dialog.settings.bufferLength = int(dialog.lineEditBufferLength.text())

            dialog.settings.guiUpdateIntervalLengthInMs = 1000 / int(dialog.spinBoxGuiUpdateFrameRate.value())

            if dialog.checkBoxAutosaveAfterCodeGeneration.checkState() == QtCore.Qt.Checked:
                dialog.settings.autoSaveAfterCodeGeneration = True
            else:
                dialog.settings.autoSaveAfterCodeGeneration = False

            return QtGui.QDialog.Accepted
        else:
            return QtGui.QDialog.Rejected


    def verifyInput(self):
        if int(self.lineEditBufferLength.text()) == 0:
            return

        self.accept()

    def dialogRejected(self):
        self.reject()

