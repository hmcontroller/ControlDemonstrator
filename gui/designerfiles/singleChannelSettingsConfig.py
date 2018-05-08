# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'singleChannelSettingsConfig.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_singleChannelSettingsConfig(object):
    def setupUi(self, singleChannelSettingsConfig):
        singleChannelSettingsConfig.setObjectName(_fromUtf8("singleChannelSettingsConfig"))
        singleChannelSettingsConfig.resize(465, 336)
        self.horizontalLayout = QtGui.QHBoxLayout(singleChannelSettingsConfig)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(singleChannelSettingsConfig)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEditVariableName = QtGui.QLineEdit(singleChannelSettingsConfig)
        self.lineEditVariableName.setObjectName(_fromUtf8("lineEditVariableName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditVariableName)
        self.label_2 = QtGui.QLabel(singleChannelSettingsConfig)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEditDisplayName = QtGui.QLineEdit(singleChannelSettingsConfig)
        self.lineEditDisplayName.setObjectName(_fromUtf8("lineEditDisplayName"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditDisplayName)
        self.colorLabel = QtGui.QLabel(singleChannelSettingsConfig)
        self.colorLabel.setObjectName(_fromUtf8("colorLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.colorLabel)
        self.pushButtonColor = QtGui.QPushButton(singleChannelSettingsConfig)
        self.pushButtonColor.setObjectName(_fromUtf8("pushButtonColor"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.pushButtonColor)
        self.label_3 = QtGui.QLabel(singleChannelSettingsConfig)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEditScaleFactor = QtGui.QLineEdit(singleChannelSettingsConfig)
        self.lineEditScaleFactor.setObjectName(_fromUtf8("lineEditScaleFactor"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEditScaleFactor)
        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(singleChannelSettingsConfig)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(singleChannelSettingsConfig)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), singleChannelSettingsConfig.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), singleChannelSettingsConfig.reject)
        QtCore.QMetaObject.connectSlotsByName(singleChannelSettingsConfig)

    def retranslateUi(self, singleChannelSettingsConfig):
        singleChannelSettingsConfig.setWindowTitle(_translate("singleChannelSettingsConfig", "Dialog", None))
        self.label.setText(_translate("singleChannelSettingsConfig", "Variablenname", None))
        self.label_2.setText(_translate("singleChannelSettingsConfig", "Anzeigename", None))
        self.colorLabel.setText(_translate("singleChannelSettingsConfig", "ColorLabel", None))
        self.pushButtonColor.setText(_translate("singleChannelSettingsConfig", "Change color", None))
        self.label_3.setText(_translate("singleChannelSettingsConfig", "Display scale", None))

