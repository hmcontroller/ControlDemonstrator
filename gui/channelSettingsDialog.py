# -*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from core.valueChannel import ValueChannel

from gui.designerfiles.channelSettingsDialog import Ui_ChannelSettingsDialog
from gui.resources import *

class ChannelSettingsDialog(QtGui.QDialog, Ui_ChannelSettingsDialog):
    def __init__(self, channels, applicationSettings, parent=None):
        super(ChannelSettingsDialog, self).__init__(parent)
        self.setupUi(self)

        self.channels = channels
        self.finalChannelIds = list()

        self.applicationSettings = applicationSettings

        for channel in self.channels.channels:
            self.finalChannelIds.append(channel.id)

        self.tableWidget.verticalHeader().setVisible(False)


        # self.tableWidget.setColumnWidth(0, 30)

        horItemOne = QtGui.QTableWidgetItem("Id")
        horItemOne.setTextAlignment(QtCore.Qt.AlignLeft)
        self.tableWidget.setHorizontalHeaderItem(2, horItemOne)

        self.tableWidget.setHorizontalHeaderLabels([u"Variablenname", u"Anzeigename", u"aktiv", u"Farbe", u"" ])


        self.setChannelsToTable()

        self.tableWidget.cellChanged.connect(self.cellChanged)
        self.tableWidget.cellClicked.connect(self.cellClicked)

        plusPixmap = QtGui.QPixmap(greenPlusPath)
        plusIcon = QtGui.QIcon(plusPixmap)
        self.toolButtonAddChannel.setIcon(plusIcon)
        self.toolButtonAddChannel.clicked.connect(self.addChannel)



    def cellChanged(self, row, column):
        print "changed", row, column

    def cellClicked(self, row, column):
        print "clicked", row, column
        if column == 3:
            colorDialog = QtGui.QColorDialog()
            answer = colorDialog.exec_()
            color = colorDialog.selectedColor()
            colorTuple = (color.red(), color.green(), color.blue())
            print colorTuple
            self.tableWidget.item(row, column).setBackground(color)
            self.tableWidget.item(row, column).setText("{};{};{}".format(colorTuple[0], colorTuple[1], colorTuple[2]))
            self.tableWidget.clearSelection()

    def removeChannel(self, id):
        for i in range(0, len(self.finalCommandIDs)):
            if self.finalCommandIDs[i] == id:
                self.finalCommandIDs.pop(i)
                break
        self.setCommandsToTable()

    def addChannel(self):
        newId = 0
        for channelId in self.finalChannelIds:
            if channelId > newId:
                newId = channelId + 1
        self.finalChannelIds.append(newId)
        self.setChannelsToTable()


    def setChannelsToTable(self):
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(len(self.finalChannelIds))

        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 35)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 30)

        for i, channelId in enumerate(self.finalChannelIds):

            try:
                channel = self.channels.getChannelById(channelId)
            except Exception:
                channel = ValueChannel(self.applicationSettings.bufferLength)

            # idItem = QtGui.QTableWidgetItem(str(channel.id))
            # idItem.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
            # self.tableWidget.setItem(i, 0, idItem)

            nameItem = QtGui.QTableWidgetItem(unicode(channel.name))
            self.tableWidget.setItem(i, 0, nameItem)

            displayNameItem = QtGui.QTableWidgetItem(unicode(channel.name))
            self.tableWidget.setItem(i, 1, displayNameItem)

            activeItem = QtGui.QTableWidgetItem()
            activeItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if channel.isRequested is True:
                activeItem.setCheckState(QtCore.Qt.Checked)
            else:
                activeItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(i, 2, activeItem)

            # myWidget = QtGui.QWidget()
            # newCheckBoxItem = QtGui.QCheckBox()
            # newCheckBoxItem.setCheckState(QtCore.Qt.Checked)
            # self.layout = QtGui.QHBoxLayout(myWidget)
            # self.layout.addWidget(newCheckBoxItem)
            # self.layout.setAlignment(QtCore.Qt.AlignCenter)
            # myWidget.setLayout(self.layout)
            # self.tableWidget.setCellWidget(0, 2, myWidget)

            colorString = "{};{};{}".format(channel.colorRgbTuple[0], channel.colorRgbTuple[1], channel.colorRgbTuple[2])
            colorItem = QtGui.QTableWidgetItem(colorString)
            self.tableWidget.setItem(i, 3, colorItem)
            colorItem.setBackground(QtGui.QColor(channel.colorRgbTuple[0], channel.colorRgbTuple[1], channel.colorRgbTuple[2]))


            pixmap = QtGui.QPixmap(redCrossPngPath)
            qIcon = QtGui.QIcon(pixmap)
            iconItem = QtGui.QTableWidgetItem()
            iconItem.setIcon(qIcon)
            iconItem.setToolTip("delete")
            self.tableWidget.setItem(i, 4, iconItem)




    def updateSettings(self):


        # set settings to form


        answer = self.exec_()

        if answer == QtGui.QDialog.Accepted:
            print "ok"
        else:
            print "dann nicht"



class LineItem(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LineItem, self).__init__(parent)

