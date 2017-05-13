# -*- encoding: utf-8 -*-

from PyQt4 import QtGui

from gui.designerfiles.aboutDialog import Ui_AboutDIalog


class AboutDialog(QtGui.QDialog, Ui_AboutDIalog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
