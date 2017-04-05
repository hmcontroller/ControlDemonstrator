# -*- encoding: utf-8 -*-
import os
import logging
from importlib import import_module

from PyQt4 import QtCore, QtGui

from core.modelMaker import ModelMaker
from core.communicator import UdpCommunicator
from core.messageInterpreter import MessageInterpreter

from gui.constants import *
from gui.TabWaterLineExperiment import TabWaterLineExperiment
from gui.TabGenericView import TabGenericView
from gui.TabSmallGenericView import TabSmallGenericView

class ControlDemonstratorMainWindow(QtGui.QMainWindow):
    def __init__(self, rootFolder):
        QtGui.QMainWindow.__init__(self)
        self.setupUi()

        self.setWindowTitle("ControlDemonstrator")

        self.screenRect = QtGui.QApplication.desktop().screenGeometry()
        self.setGeometry(self.screenRect.width() * 0.05, self.screenRect.height() * 0.05,
                         self.screenRect.width() * 0.9, self.screenRect.height() * 0.9)


        # show the application on the second monitor as maximized window
        self.screenRectSecondMonitor = QtGui.QApplication.desktop().screenGeometry(1)
        self.setGeometry(self.screenRect.width(), 0,
                         self.screenRectSecondMonitor.width() * 0.9, self.screenRectSecondMonitor.height() * 0.9)
        self.showMaximized()


        # show a splash image
        splashImagePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Regelkreis.gif")
        splashMap = QtGui.QPixmap(splashImagePath)
        splashScreen = QtGui.QSplashScreen(splashMap)
        splashScreen.show()
        QtGui.qApp.processEvents()
        QtGui.qApp.processEvents()

        # generate model objects according to the config file
        configFilePath = os.path.join(rootFolder, "config.txt")
        modelMaker = ModelMaker(configFilePath)
        self.settings = modelMaker.getApplicationSettings()

        # TODO it is ugly how the messageData list will be generated in model maker - check single source problem
        self.messageFormat = modelMaker.getMessageFormatList()

        self.channels = modelMaker.getMeasurementDataModel()

        self.commands = modelMaker.getCommands()

        self.communicator = UdpCommunicator(self.settings)
        self.communicator.setMessageMap(self.messageFormat)
        self.communicator.connectToController()

        tabs = modelMaker.getTabs()

        self.addTabs(tabs)


        # setup a timer, that triggers to read from the controller
        self.receiveTimer = QtCore.QTimer()
        self.receiveTimer.setSingleShot(False)
        self.receiveTimer.timeout.connect(self.receiveAndSend)
        self.receiveTimer.start(self.settings.receiveMessageIntervalLengthInMs)

        # # setup a timer, that triggers to send to the controller
        # self.sendTimer = QtCore.QTimer()
        # self.sendTimer.setSingleShot(False)
        # self.sendTimer.timeout.connect(self.send)
        # self.sendTimer.start(self.settings.sendMessageIntervalLengthInMs)

        # setup a timer, that runs a loop to update the gui
        self.guiUpdateTimer = QtCore.QTimer()
        self.guiUpdateTimer.setSingleShot(False)
        self.guiUpdateTimer.timeout.connect(self.refreshGui)
        self.guiUpdateTimer.start(self.settings.guiUpdateIntervalLengthInMs)

        # for debugging purpose
        self.loopReportTimer = QtCore.QTimer()
        self.loopReportTimer.setSingleShot(False)
        self.connect(self.loopReportTimer, QtCore.SIGNAL("timeout()"), self.printLoopPerformance)
        self.loopReportTimer.start(5000)

        # some calculations for debugging purpose
        self.loopDurationMin = 1000000
        self.loopDurationMax = 0
        self.loopDurationAverage = 0
        self.loopDurationSum = 0
        self.loopDurationCounter = 0

        splashScreen.finish(self)
        logging.info("GUI load complete")

    def setupUi(self):
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        self.centralWidgetLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.centralWidgetLayout.setMargin(0)
        self.centralWidgetLayout.setSpacing(0)

        self.setCentralWidget(self.centralwidget)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")

        self.centralWidgetLayout.addWidget(self.tabWidget)


    def addTabs(self, tabs):
        for givenTab in tabs:
            tabContentClassName = givenTab[0]
            if givenTab[1] is None:
                raise Exception("Please specify a name for the entry {} in the config file under section tabs".format(tabContentClassName))
            tabDisplayName = givenTab[1].decode('utf-8')


            tab = QtGui.QWidget()
            tabLayout = QtGui.QHBoxLayout(tab)
            tabLayout.setSpacing(0)
            tabLayout.setMargin(0)
            self.tabWidget.addTab(tab, tabDisplayName)

            tabContentClass = getattr(import_module('gui.' + tabContentClassName), tabContentClassName)
            tabContentClassInstance = tabContentClass(self.commands, self.channels, self.settings, self.communicator)

            tabLayout.addWidget(tabContentClassInstance)



    def receiveAndSend(self):
        self.receive()
        self.send()

    def receive(self):
        messages = self.communicator.receive()
        for message in messages:
            self.handleNewData(message)
            self.calculateSomeStuff(message)

    def send(self):
        self.communicator.send(self.commands)

    def refreshGui(self):
        pass
        # self.tabWaterLineExperiment.updateTab(self.channels)
        # self.tabGeneric.updateTab(self.channels)

    def handleNewData(self, message):
        MessageInterpreter.mapUserChannels(self.channels, message)
        returnedCommand = MessageInterpreter.getMicroControllerCommandReturned(message)
        self.commands[returnedCommand.id].checkMicroControllerReturnValue(returnedCommand)

    def calculateSomeStuff(self, message):
        loopCycleDuration = MessageInterpreter.getLoopCycleDuration(message)
        # calculate some statistics
        if loopCycleDuration < self.loopDurationMin:
            self.loopDurationMin = loopCycleDuration
        elif loopCycleDuration > self.loopDurationMax:
            self.loopDurationMax = loopCycleDuration

        self.loopDurationSum += loopCycleDuration
        self.loopDurationCounter += 1
        self.loopDurationAverage = self.loopDurationSum / float(self.loopDurationCounter)

    def printLoopPerformance(self):
        pass
        # print "min", self.loopDurationMin, "max", self.loopDurationMax, "avg", self.loopDurationAverage

    def closeEvent(self, *args, **kwargs):
        QtGui.QApplication.quit()

