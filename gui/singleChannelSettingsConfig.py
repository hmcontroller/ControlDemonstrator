# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.designerfiles.singleChannelSettingsConfig import Ui_singleChannelSettingsConfig


class SingleChannelSettingsConfig(QtGui.QDialog, Ui_singleChannelSettingsConfig):
    def __init__(self, channel, parent=None):
        super(SingleChannelSettingsConfig, self).__init__(parent)
        self.channel = channel
        self.setupUi(self)


        self.pushButtonColor.clicked.connect(self.changeColor)
        self.selectedColor = QtGui.QColor()


    def changeColor(self):
        colorDialog = QtGui.QColorDialog()
        answer = colorDialog.exec_()
        color = colorDialog.selectedColor()
        colorTuple = (color.red(), color.green(), color.blue())
        # self.channel.colorRgbTuple = colorTuple
        # self.setColorbox(QtGui.QColor(self.channel.colorRgbTuple[0], self.channel.colorRgbTuple[1], self.channel.colorRgbTuple[2]))
        self.setColorbox(color)

    def setColorbox(self, color):
        self.colorLabel.setText("color")
        self.pushButtonColor.setStyleSheet("background-color: {}".format(color.name()))
        self.selectedColor = color

    @staticmethod
    def updateSettings(channel):
        dialog = SingleChannelSettingsConfig(channel)


        dialog.lineEditVariableName.setText(channel.name)
        dialog.lineEditDisplayName.setText(channel.displayName)
        dialog.lineEditScaleFactor.setText(str(channel.displayScaleFactor))
        dialog.setColorbox(QtGui.QColor(channel.colorRgbTuple[0], channel.colorRgbTuple[1], channel.colorRgbTuple[2]))




        answer = dialog.exec_()

        if answer == QtGui.QDialog.Accepted:
            channel.name = str(dialog.lineEditVariableName.text())
            channel.displayName = unicode(dialog.lineEditDisplayName.text())
            channel.displayScaleFactor = float(dialog.lineEditScaleFactor.text())
            channel.colorRgbTuple = tuple([int(dialog.selectedColor.red()), int(dialog.selectedColor.green()), int(dialog.selectedColor.blue())])


class ColorLineEdit(QtGui.QLabel):

    showColorPicker = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ColorLineEdit, self).__init__(parent)

    def setBackgroundColor(self, color):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, color)
        self.setPalette(palette)

    def mousePressEvent(self, QMouseEvent):
        self.showColorPicker.emit()