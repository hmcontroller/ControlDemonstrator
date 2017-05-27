# -*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from core.valueChannel import ValueChannel

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

        self.initializeTable()

        self.tableWidget.cellClicked.connect(self.cellClicked)

        plusPixmap = QtGui.QPixmap(greenPlusPath)
        plusIcon = QtGui.QIcon(plusPixmap)
        self.toolButtonAddChannel.setIcon(plusIcon)
        self.toolButtonAddChannel.clicked.connect(self.createChannel)

    def updateChannels(self):

        self.resizeDialogToTableWidth()

        answer = self.exec_()

        if answer == QtGui.QDialog.Accepted:

            # clear old channels
            self.channels.channels = list()

            for rowNumber in range(0, self.tableWidget.rowCount()):
                channel = ValueChannel(self.applicationSettings.bufferLength)

                channel.id = rowNumber

                channel.name = unicode(self.tableWidget.item(rowNumber, self.VARIABLE_NAME_COLUMN).text()).replace(" ", "")

                channel.displayName = unicode(self.tableWidget.item(rowNumber, self.DISPLAY_NAME_COLUMN).text())

                if self.tableWidget.item(rowNumber, self.ACTIVE_COLUMN).checkState() == QtCore.Qt.Checked:
                    channel.isRequested = True
                else:
                    channel.isRequested = False

                colorTuple = unicode(self.tableWidget.item(rowNumber, self.HIDDEN_COLOR_COLUMN).text()).split(";")
                channel.colorRgbTuple = (int(colorTuple[0]), int(colorTuple[1]), int(colorTuple[2]))

                # append them silently, so that the changed signal will not be emitted
                self.channels.channels.append(channel)

            # emit changed only once after new state is complete
            self.channels.changed.emit(self.channels)

            return self.channels

        else:
            return self.channels



    def initializeTable(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        for channel in self.channels.channels:
            self.addChannelToTable(channel)

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
            self.removeChannelFromTable(row)

    def createChannel(self):
        # create a temp channel to get the standard init values
        tempChannel = ValueChannel(self.applicationSettings.bufferLength)
        self.addChannelToTable(tempChannel)

    def addChannelToTable(self, channel):

        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)

        nameItem = QtGui.QTableWidgetItem(unicode(channel.name))
        self.tableWidget.setItem(row, self.VARIABLE_NAME_COLUMN, nameItem)

        displayNameItem = QtGui.QTableWidgetItem(unicode(channel.displayName))
        self.tableWidget.setItem(row, self.DISPLAY_NAME_COLUMN, displayNameItem)

        activeItem = QtGui.QTableWidgetItem()
        activeItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

        if channel.isRequested is True:
            activeItem.setCheckState(QtCore.Qt.Checked)
        else:
            activeItem.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget.setItem(row, self.ACTIVE_COLUMN, activeItem)

        colorString = "{};{};{}".format(channel.colorRgbTuple[0], channel.colorRgbTuple[1], channel.colorRgbTuple[2])

        colorItem = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(row, self.COLOR_COLUMN, colorItem)
        colorItem.setBackground(QtGui.QColor(channel.colorRgbTuple[0], channel.colorRgbTuple[1], channel.colorRgbTuple[2]))

        colorStringItem = QtGui.QTableWidgetItem(colorString)
        self.tableWidget.setItem(row, self.HIDDEN_COLOR_COLUMN, colorStringItem)

        pixmap = QtGui.QPixmap(redCrossPngPath)
        qIcon = QtGui.QIcon(pixmap)
        iconItem = QtGui.QTableWidgetItem()
        iconItem.setIcon(qIcon)
        iconItem.setToolTip("delete")
        self.tableWidget.setItem(row, self.DELETE_COLUMN, iconItem)

        idItem = QtGui.QTableWidgetItem(unicode(channel.id))
        self.tableWidget.setItem(row, self.ID_COLUMN, idItem)

    def removeChannelFromTable(self, row):
        self.tableWidget.removeRow(row)

    def resizeDialogToTableWidth(self, logicalIndex=0, oldSize=0, newSize=0):
        widthSum = 0
        for i in range(0, self.tableWidget.columnCount()):
            widthSum += self.tableWidget.columnWidth(i)

        self.resize(widthSum + 24, 700)

