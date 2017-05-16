# -*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from core.valueChannel import ValueChannel
from core.measurementData import MeasurementData

from gui.designerfiles.channelSettingsDialog import Ui_ChannelSettingsDialog
from gui.resources import *

class ChannelSettingsDialog(QtGui.QDialog, Ui_ChannelSettingsDialog):

    VARIABLE_NAME_COLUMN = 0
    DISPLAY_NAME_COLUMN = 1
    ACTIVE_COLUMN = 2
    COLOR_COLUMN = 3
    DELETE_COLUMN = 4
    ID_COLUMN = 5
    HIDDEN_COLOR_COLUMN = 6

    def __init__(self, channels, applicationSettings, parent=None):
        super(ChannelSettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.applicationSettings = applicationSettings


        self.channels = channels
        self.finalChannelIds = list()
        self.newMeasurementData = MeasurementData(self.applicationSettings.bufferLength)
        self.freshChannels = list()

        for channel in self.channels.channels:
            self.finalChannelIds.append(channel.id)

        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setFrameStyle(QtGui.QFrame.NoFrame)
        self.tableWidget.setColumnCount(7)

        self.tableHeader = QtGui.QHeaderView(QtCore.Qt.Horizontal, self.tableWidget)
        self.tableWidget.setHorizontalHeader(self.tableHeader)
        self.tableHeader.setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableHeader.setResizeMode(self.VARIABLE_NAME_COLUMN, QtGui.QHeaderView.Interactive)
        self.tableHeader.setResizeMode(self.DISPLAY_NAME_COLUMN, QtGui.QHeaderView.Stretch)
        self.tableHeader.setResizeMode(self.ACTIVE_COLUMN, QtGui.QHeaderView.Fixed)
        self.tableHeader.setResizeMode(self.COLOR_COLUMN, QtGui.QHeaderView.Fixed)
        self.tableHeader.setResizeMode(self.DELETE_COLUMN, QtGui.QHeaderView.Fixed)


        self.tableWidget.setColumnHidden(self.ID_COLUMN, True)
        self.tableWidget.setColumnHidden(self.HIDDEN_COLOR_COLUMN, True)


        columnNames = [u"Variablenname", u"Anzeigename", u"aktiv", u"Farbe", u"" ]

        for i, name in enumerate(columnNames):
            horItem = QtGui.QTableWidgetItem(name)
            horItem.setTextAlignment(QtCore.Qt.AlignLeft)
            horItem.setBackground(QtGui.QBrush(QtCore.Qt.darkGray))
            self.tableWidget.setHorizontalHeaderItem(i, horItem)

        self.tableWidget.horizontalHeader().setStyleSheet(" QHeaderView::section { "
                        "spacing: 10px; background-color: lightgray; border: 3px solid lightgray; }")

        self.tableWidget.setColumnWidth(self.VARIABLE_NAME_COLUMN, 250)
        self.tableWidget.setColumnWidth(self.DISPLAY_NAME_COLUMN, 250)
        self.tableWidget.setColumnWidth(self.ACTIVE_COLUMN, 32)
        self.tableWidget.setColumnWidth(self.COLOR_COLUMN, 37)
        self.tableWidget.setColumnWidth(self.DELETE_COLUMN, 24)

        self.setChannelsToTable()

        self.tableWidget.cellChanged.connect(self.cellChanged)
        self.tableWidget.cellClicked.connect(self.cellClicked)

        plusPixmap = QtGui.QPixmap(greenPlusPath)
        plusIcon = QtGui.QIcon(plusPixmap)
        self.toolButtonAddChannel.setIcon(plusIcon)
        self.toolButtonAddChannel.clicked.connect(self.addChannel)



    def cellChanged(self, row, column):
        pass

    def cellClicked(self, row, column):
        if column == self.COLOR_COLUMN:
            colorDialog = QtGui.QColorDialog()
            answer = colorDialog.exec_()
            color = colorDialog.selectedColor()
            colorTuple = (color.red(), color.green(), color.blue())
            self.tableWidget.item(row, self.COLOR_COLUMN).setBackground(color)
            self.tableWidget.item(row, self.HIDDEN_COLOR_COLUMN).setText("{};{};{}".format(colorTuple[0], colorTuple[1], colorTuple[2]))
            self.tableWidget.clearSelection()

        if column == self.DELETE_COLUMN:
            idToDelete = int(self.tableWidget.item(row, self.ID_COLUMN).text())
            self.removeChannel(idToDelete)

    def removeChannel(self, id):
        for i in range(0, len(self.finalChannelIds)):
            if self.finalChannelIds[i] == id:
                self.finalChannelIds.pop(i)
                break
        self.setChannelsToTable()

    def addChannel(self):
        newId = 0
        for channelId in self.finalChannelIds:
            if channelId >= newId:
                newId = channelId + 1
        self.finalChannelIds.append(newId)

        channel = ValueChannel(self.applicationSettings.bufferLength)
        channel.id = newId
        self.freshChannels.append(channel)

        self.setChannelsToTable()


    def setChannelsToTable(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(self.finalChannelIds))


        for i, channelId in enumerate(self.finalChannelIds):

            try:
                channel = self.channels.getChannelById(channelId)
            except Exception:
                try:
                    channel = self.newMeasurementData.getChannelById(channelId)
                except Exception:
                    for freshChannel in self.freshChannels:
                        if freshChannel.id == channelId:
                            channel = freshChannel

            nameItem = QtGui.QTableWidgetItem(unicode(channel.name))
            self.tableWidget.setItem(i, self.VARIABLE_NAME_COLUMN, nameItem)

            displayNameItem = QtGui.QTableWidgetItem(unicode(channel.name))
            self.tableWidget.setItem(i, self.DISPLAY_NAME_COLUMN, displayNameItem)

            activeItem = QtGui.QTableWidgetItem()
            activeItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

            if channel.isRequested is True:
                activeItem.setCheckState(QtCore.Qt.Checked)
            else:
                activeItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(i, self.ACTIVE_COLUMN, activeItem)

            # myWidget = QtGui.QWidget()
            # newCheckBoxItem = QtGui.QCheckBox()
            # newCheckBoxItem.setCheckState(QtCore.Qt.Checked)
            # self.layout = QtGui.QHBoxLayout(myWidget)
            # self.layout.addWidget(newCheckBoxItem)
            # self.layout.setAlignment(QtCore.Qt.AlignCenter)
            # myWidget.setLayout(self.layout)
            # self.tableWidget.setCellWidget(0, 2, myWidget)

            colorString = "{};{};{}".format(channel.colorRgbTuple[0], channel.colorRgbTuple[1], channel.colorRgbTuple[2])

            colorItem = QtGui.QTableWidgetItem()
            self.tableWidget.setItem(i, self.COLOR_COLUMN, colorItem)
            colorItem.setBackground(QtGui.QColor(channel.colorRgbTuple[0], channel.colorRgbTuple[1], channel.colorRgbTuple[2]))

            colorStringItem = QtGui.QTableWidgetItem(colorString)
            self.tableWidget.setItem(i, self.HIDDEN_COLOR_COLUMN, colorStringItem)

            pixmap = QtGui.QPixmap(redCrossPngPath)
            qIcon = QtGui.QIcon(pixmap)
            iconItem = QtGui.QTableWidgetItem()
            iconItem.setIcon(qIcon)
            iconItem.setToolTip("delete")
            self.tableWidget.setItem(i, self.DELETE_COLUMN, iconItem)

            idItem = QtGui.QTableWidgetItem(unicode(channelId))
            self.tableWidget.setItem(i, self.ID_COLUMN, idItem)

    def resizeDialogToTableWidth(self, logicalIndex=0, oldSize=0, newSize=0):
        widthSum = 0
        for i in range(0, self.tableWidget.columnCount()):
            widthSum += self.tableWidget.columnWidth(i)

        self.resize(widthSum + 24, 700)

    def updateChannels(self):

        self.resizeDialogToTableWidth()

        answer = self.exec_()

        if answer == QtGui.QDialog.Accepted:

            for rowNumber, channelId in enumerate(self.finalChannelIds):
                try:
                    channel = self.channels.getChannelById(channelId)
                except:
                    for freshChannel in self.freshChannels:
                        if freshChannel.id == channelId:
                            channel = freshChannel

                channel.name = unicode(self.tableWidget.item(rowNumber, self.VARIABLE_NAME_COLUMN).text())
                channel.displayName = unicode(self.tableWidget.item(rowNumber, self.DISPLAY_NAME_COLUMN).text())
                if self.tableWidget.item(rowNumber, self.ACTIVE_COLUMN).checkState() == QtCore.Qt.Checked:
                    channel.isRequested = True
                else:
                    channel.isRequested = False

                colorTuple = unicode(self.tableWidget.item(rowNumber, self.HIDDEN_COLOR_COLUMN).text()).split(";")
                channel.colorRgbTuple = (int(colorTuple[0]), int(colorTuple[1]), int(colorTuple[2]))



            oldChannels = list()
            for channel in self.channels.channels:
                oldChannels.append(channel)
            for oldChannel in oldChannels:
                if oldChannel.id not in self.finalChannelIds:
                    self.channels.removeChannel(oldChannel)

            for channel in self.freshChannels:
                self.channels.addChannel(channel)
            return self.channels



        else:
            return self.channels


