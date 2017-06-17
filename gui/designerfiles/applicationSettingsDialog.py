# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'applicationSettingsDialog.ui'
#
# Created: Fri Jun 09 08:28:07 2017
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ApplicationSettingsDialog(object):
    def setupUi(self, ApplicationSettingsDialog):
        ApplicationSettingsDialog.setObjectName(_fromUtf8("ApplicationSettingsDialog"))
        ApplicationSettingsDialog.resize(360, 167)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ApplicationSettingsDialog.sizePolicy().hasHeightForWidth())
        ApplicationSettingsDialog.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(ApplicationSettingsDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_3 = QtGui.QLabel(ApplicationSettingsDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEditBufferLength = QtGui.QLineEdit(ApplicationSettingsDialog)
        self.lineEditBufferLength.setObjectName(_fromUtf8("lineEditBufferLength"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditBufferLength)
        self.label = QtGui.QLabel(ApplicationSettingsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.spinBoxGuiUpdateFrameRate = QtGui.QSpinBox(ApplicationSettingsDialog)
        self.spinBoxGuiUpdateFrameRate.setMinimum(1)
        self.spinBoxGuiUpdateFrameRate.setMaximum(25)
        self.spinBoxGuiUpdateFrameRate.setObjectName(_fromUtf8("spinBoxGuiUpdateFrameRate"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBoxGuiUpdateFrameRate)
        self.label_2 = QtGui.QLabel(ApplicationSettingsDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.checkBoxAutosaveAfterCodeGeneration = QtGui.QCheckBox(ApplicationSettingsDialog)
        self.checkBoxAutosaveAfterCodeGeneration.setText(_fromUtf8(""))
        self.checkBoxAutosaveAfterCodeGeneration.setObjectName(_fromUtf8("checkBoxAutosaveAfterCodeGeneration"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.checkBoxAutosaveAfterCodeGeneration)
        self.label_4 = QtGui.QLabel(ApplicationSettingsDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.checkBoxAutoUpdate = QtGui.QCheckBox(ApplicationSettingsDialog)
        self.checkBoxAutoUpdate.setText(_fromUtf8(""))
        self.checkBoxAutoUpdate.setCheckable(False)
        self.checkBoxAutoUpdate.setObjectName(_fromUtf8("checkBoxAutoUpdate"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.checkBoxAutoUpdate)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(ApplicationSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(ApplicationSettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(ApplicationSettingsDialog)

    def retranslateUi(self, ApplicationSettingsDialog):
        ApplicationSettingsDialog.setWindowTitle(_translate("ApplicationSettingsDialog", "Programmeinstellungen", None))
        self.label_3.setText(_translate("ApplicationSettingsDialog", "buffer length for incoming data", None))
        self.lineEditBufferLength.setText(_translate("ApplicationSettingsDialog", "10000", None))
        self.label.setText(_translate("ApplicationSettingsDialog", "Plot update rate in frames per second", None))
        self.label_2.setText(_translate("ApplicationSettingsDialog", "autosave project after generating c-code", None))
        self.label_4.setText(_translate("ApplicationSettingsDialog", "automatically check for updates", None))

