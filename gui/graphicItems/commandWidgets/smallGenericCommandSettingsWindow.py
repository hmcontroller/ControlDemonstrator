# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.designerfiles.smallGenericCommandSettingsWindow import Ui_smallGenericCommandSettingsWindow

class SmallGenericCommandSettingsWindow(QtGui.QDialog, Ui_smallGenericCommandSettingsWindow):
    def __init__(self, parent=None):
        super(SmallGenericCommandSettingsWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("Konfiguration")