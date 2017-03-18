# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'smallGenericCommandSettingsWindow.ui'
#
# Created: Fri Mar 17 20:38:23 2017
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

class Ui_smallGenericCommandSettingsWindow(object):
    def setupUi(self, smallGenericCommandSettingsWindow):
        smallGenericCommandSettingsWindow.setObjectName(_fromUtf8("smallGenericCommandSettingsWindow"))
        smallGenericCommandSettingsWindow.resize(286, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(smallGenericCommandSettingsWindow)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(smallGenericCommandSettingsWindow)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(smallGenericCommandSettingsWindow)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEditMin = QtGui.QLineEdit(smallGenericCommandSettingsWindow)
        self.lineEditMin.setObjectName(_fromUtf8("lineEditMin"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditMin)
        self.label_4 = QtGui.QLabel(smallGenericCommandSettingsWindow)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lineEditMax = QtGui.QLineEdit(smallGenericCommandSettingsWindow)
        self.lineEditMax.setObjectName(_fromUtf8("lineEditMax"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEditMax)
        self.lineEditDisplayName = QtGui.QLineEdit(smallGenericCommandSettingsWindow)
        self.lineEditDisplayName.setObjectName(_fromUtf8("lineEditDisplayName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditDisplayName)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(smallGenericCommandSettingsWindow)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.radioButtonValueMode = QtGui.QRadioButton(smallGenericCommandSettingsWindow)
        self.radioButtonValueMode.setObjectName(_fromUtf8("radioButtonValueMode"))
        self.buttonGroupInputMode = QtGui.QButtonGroup(smallGenericCommandSettingsWindow)
        self.buttonGroupInputMode.setObjectName(_fromUtf8("buttonGroupInputMode"))
        self.buttonGroupInputMode.addButton(self.radioButtonValueMode)
        self.verticalLayout.addWidget(self.radioButtonValueMode)
        self.radioButtonSwitchMode = QtGui.QRadioButton(smallGenericCommandSettingsWindow)
        self.radioButtonSwitchMode.setObjectName(_fromUtf8("radioButtonSwitchMode"))
        self.buttonGroupInputMode.addButton(self.radioButtonSwitchMode)
        self.verticalLayout.addWidget(self.radioButtonSwitchMode)
        self.radioButtonToggleMode = QtGui.QRadioButton(smallGenericCommandSettingsWindow)
        self.radioButtonToggleMode.setObjectName(_fromUtf8("radioButtonToggleMode"))
        self.buttonGroupInputMode.addButton(self.radioButtonToggleMode)
        self.verticalLayout.addWidget(self.radioButtonToggleMode)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.checkBoxPendingMode = QtGui.QCheckBox(smallGenericCommandSettingsWindow)
        self.checkBoxPendingMode.setObjectName(_fromUtf8("checkBoxPendingMode"))
        self.verticalLayout.addWidget(self.checkBoxPendingMode)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(smallGenericCommandSettingsWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(smallGenericCommandSettingsWindow)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), smallGenericCommandSettingsWindow.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), smallGenericCommandSettingsWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(smallGenericCommandSettingsWindow)

    def retranslateUi(self, smallGenericCommandSettingsWindow):
        smallGenericCommandSettingsWindow.setWindowTitle(_translate("smallGenericCommandSettingsWindow", "Dialog", None))
        self.label_2.setText(_translate("smallGenericCommandSettingsWindow", "Anzeigename", None))
        self.label_3.setText(_translate("smallGenericCommandSettingsWindow", "Min", None))
        self.label_4.setText(_translate("smallGenericCommandSettingsWindow", "Max", None))
        self.label.setText(_translate("smallGenericCommandSettingsWindow", "Art der Eingabe", None))
        self.radioButtonValueMode.setText(_translate("smallGenericCommandSettingsWindow", "Zahleneingabe", None))
        self.radioButtonSwitchMode.setText(_translate("smallGenericCommandSettingsWindow", "Schalter", None))
        self.radioButtonToggleMode.setText(_translate("smallGenericCommandSettingsWindow", "Taster", None))
        self.checkBoxPendingMode.setText(_translate("smallGenericCommandSettingsWindow", "Wert erst nach Bestätigung senden (p)", None))

