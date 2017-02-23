# -*- encoding: utf-8 -*-
import os
import logging

from PyQt4 import QtCore, QtGui

from core.modelMaker import ModelMaker
from core.communicator import UdpCommunicator
from core.messageInterpreter import MessageInterpreter

from gui.constants import *
from gui.tabWaterLineExperiment import TabWaterLineExperiment
from gui.tabGenericView import TabGenericView

class ControlDemonstratorMainWindow(QtGui.QMainWindow):
    def __init__(self, rootFolder):
        QtGui.QMainWindow.__init__(self)
        self.setupUi()

        self.setWindowTitle("ControlDemonstrator")

        self.screenRect = QtGui.QApplication.desktop().screenGeometry()
        self.setGeometry(self.screenRect.width() * 0.05, self.screenRect.height() * 0.05,
                         self.screenRect.width() * 0.9, self.screenRect.height() * 0.9)

        # show a splash image
        splashImagePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Regelkreis.gif")
        splashMap = QtGui.QPixmap(splashImagePath)
        splashScreen = QtGui.QSplashScreen(splashMap)
        splashScreen.show()
        QtGui.qApp.processEvents()
        splashScreen.showMessage(u"Regulator wird geladen...", QtCore.Qt.AlignCenter)
        QtGui.qApp.processEvents()

        # generate model objects according to the config file
        configFilePath = os.path.join(rootFolder, "config.txt")
        modelMaker = ModelMaker(configFilePath)
        # self.sensorMapping = modelMaker.getSensorMapping()
        self.settings = modelMaker.getMiscSettings()

        # TODO it is dirty how the messageData list will be generated in model maker - check single source problem
        self.messageFormat = modelMaker.getMessageFormatList()

        # TODO - do not differentiate between analog channels and fastParameterChannels
        # TODO remove sensorMapping from the config file
        self.channels = modelMaker.getMeasurementDataModel()

        self.commands = modelMaker.getCommands()

        self.communicator = UdpCommunicator(self.settings)
        self.communicator.setMessageMap(self.messageFormat)

        # # add a tab for the waterLineExperiment
        self.tabWaterLineExperiment = TabWaterLineExperiment(self.commands, self.channels, self.settings)
        self.tabWaterLineExperimentLayout.addWidget(self.tabWaterLineExperiment)

        # add a tab for generic control
        self.tabGeneric = TabGenericView(self.commands, self.channels, self.settings)
        self.tabGenericViewLayout.addWidget(self.tabGeneric)


        # setup a timer, that triggers to read from the controller
        self.receiveTimer = QtCore.QTimer()
        self.receiveTimer.setSingleShot(False)
        self.receiveTimer.timeout.connect(self.receive)
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

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tabWaterLineExperimentLayout = QtGui.QHBoxLayout(self.tab)
        self.tabWaterLineExperimentLayout.setSpacing(0)
        self.tabWaterLineExperimentLayout.setMargin(0)
        self.tabWaterLineExperimentLayout.setObjectName("tabWaterLineExperimentLayout")
        self.tabWidget.addTab(self.tab, "Wasserstandexperiment")

        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.tabGenericViewLayout = QtGui.QHBoxLayout(self.tab_1)
        self.tabGenericViewLayout.setSpacing(0)
        self.tabGenericViewLayout.setMargin(0)
        self.tabGenericViewLayout.setObjectName("tabGenericView")
        self.tabWidget.addTab(self.tab_1, "generische Ansicht")

        self.centralWidgetLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralwidget)

    def receive(self):
        messages = self.communicator.receive()
        if messages is None:
            return
        self.handleNewData(messages)
        self.calculateSomeStuff(messages)
        self.send()

    def send(self):
        self.communicator.send(self.commands)

    def refreshGui(self):
        self.tabWaterLineExperiment.updateTab(self.channels)
        self.tabGeneric.updateTab(self.channels)

    def handleNewData(self, messages):
        MessageInterpreter.mapUserChannels(self.channels, messages)

        for message in messages:
            returnedCommand = MessageInterpreter.getMicroControllerCommandReturned(message)
            self.commands[returnedCommand.id].checkMicroControllerReturnValue(returnedCommand)

    def calculateSomeStuff(self, messages):
        loopCycleDuration = MessageInterpreter.getLoopCycleDuration(messages[-1])
        # calculate some statistics
        if loopCycleDuration < self.loopDurationMin:
            self.loopDurationMin = loopCycleDuration
        elif loopCycleDuration > self.loopDurationMax:
            self.loopDurationMax = loopCycleDuration

        self.loopDurationSum += loopCycleDuration
        self.loopDurationCounter += 1
        self.loopDurationAverage = self.loopDurationSum / float(self.loopDurationCounter)

    def printLoopPerformance(self):
        print "min", self.loopDurationMin, "max", self.loopDurationMax, "avg", self.loopDurationAverage

    def closeEvent(self, *args, **kwargs):
        QtGui.QApplication.quit()

