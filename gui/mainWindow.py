# -*- encoding: utf-8 -*-
import os
import logging
from importlib import import_module
import json
import pickle
import collections
import webbrowser
import time
import errno
import traceback

from PyQt4 import QtCore, QtGui
import sip

from core.modelMaker import ModelMaker
from core.communicator import UdpCommunicator, CommState
from core.communicator import SerialCommunicator
from core.messageInterpreter import MessageInterpreter
from core.configFileManager import ConfigFileManager
from core.applicationSettingsManager import ApplicationSettingsManager
from core.model.projectSettings import ProjectSettings
from core.includeFileMaker import IncludeFileMaker
from core.model.tabDescription import TabDescription

from gui.aboutDialog import AboutDialog
from gui.projectMiscSettingsDialog import ProjectMiscSettingsDialog
from gui.channelSettingsDialog import ChannelSettingsDialog
from gui.commandSettingsDialog import CommandSettingsDialog

from gui.constants import *
from gui.tabWaterLineExperiment import TabWaterLineExperiment
from gui.tabGenericView import TabGenericView
from gui.tabSmallGenericView import TabSmallGenericView
from gui.resources import *

class ControlDemonstratorMainWindow(QtGui.QMainWindow):

    displayMessage = QtCore.pyqtSignal(object, object)

    def __init__(self, rootFolder, exceptHook):
        QtGui.QMainWindow.__init__(self)

        exceptHook.caughtException.connect(self.uncaughtExceptionOccured)

        self.programRootFolder = rootFolder

        pixmap = QtGui.QPixmap(icPath)
        icon = QtGui.QIcon(pixmap)
        QtGui.QApplication.setApplicationName(u"microRay")
        QtGui.QApplication.setWindowIcon(icon)

        self.appSettingsManager = ApplicationSettingsManager(PATH_TO_APPLICATION_SETTINGS)
        self.applicationSettings = self.appSettingsManager.restoreSettingsFromFile()
        self.applicationSettings.changed.connect(self.appSettingsChanged)

        # setup a timer, that triggers to read from the controller
        self.receiveTimer = QtCore.QTimer()
        self.receiveTimer.setSingleShot(False)
        self.receiveTimer.timeout.connect(self.receiveAndSend)


        self.projectConfigManager = ConfigFileManager(self.applicationSettings)

        self.includeFileMaker = IncludeFileMaker()

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




        self.setInitialValuesTimer = QtCore.QTimer()
        self.setInitialValuesTimer.setSingleShot(True)
        self.setInitialValuesTimer.timeout.connect(self.setInitialValues)





        if len(self.applicationSettings.recentProjectFilePathes) > 0:
            try:
                self.loadProject(self.applicationSettings.recentProjectFilePathes[0])
            except IOError:
                self.displayMessage.emit("Konnte die Projektdatei nicht finden.", "warning")












        # self.receiveTimer.start(self.applicationSettings.receiveMessageIntervalLengthInMs)


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


        self.setupMainMenu()


    def addTabs(self, tabs):


        if len(tabs) == 1:
            self.addOnlyOneWidget(tabs)
            return

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")

        self.centralWidgetLayout.addWidget(self.tabWidget)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)


        for givenTab in tabs:
            tab = QtGui.QWidget()
            tab.setFont(font)
            tabLayout = QtGui.QHBoxLayout(tab)
            tabLayout.setSpacing(0)
            tabLayout.setMargin(0)
            self.tabWidget.addTab(tab, givenTab.displayName)

            # don't do this dynamically, otherwise pyinstaller stops working
            # tabContentClass = getattr(import_module(givenTab.pathToClassFile), givenTab.className)
            # tabContentClassInstance = tabContentClass(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator)

            classInstance = None
            if givenTab.className == "TabWaterLineExperiment":
                classInstance = TabWaterLineExperiment(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator, self)
            elif givenTab.className == "TabSmallGenericView":
                classInstance = TabSmallGenericView(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator, self)
            elif givenTab.className == "TabGenericView":
                classInstance = TabGenericView(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator, self)
            else:
                raise ValueError("inappropriate tab given in project file")


            tabLayout.addWidget(classInstance)

    def addOnlyOneWidget(self, tabs):
        tab = tabs[0]

        classInstance = None

        # don't do this dynamically, otherwise pyinstaller stops working
        # tabContentClass = getattr(import_module(givenTab.pathToClassFile), givenTab.className)
        # tabContentClassInstance = tabContentClass(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator)

        if tab.className == "TabWaterLineExperiment":
            classInstance = TabWaterLineExperiment(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator, self)
        elif tab.className == "TabSmallGenericView":
            classInstance = TabSmallGenericView(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator, self)
        elif tab.className == "TabGenericView":
            classInstance = TabGenericView(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator, self)
        else:
            raise ValueError("inappropriate tab given in project file")



        self.centralWidgetLayout.addWidget(classInstance)


    def setupMainMenu(self):
        newProjectAction = QtGui.QAction(u"Neues Projekt...", self)
        newProjectAction.setShortcut("Ctrl+N")
        newProjectAction.setStatusTip(u"Legt ein neues Projekt an.")
        newProjectAction.triggered.connect(self.newProject)

        openAction = QtGui.QAction(u"Öffnen...", self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.open)

        saveAction = QtGui.QAction(u"Speichern", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.save)

        saveAsAction = QtGui.QAction(u"Speichern unter...", self)
        saveAsAction.setShortcut("Shift+Ctrl+N")
        saveAsAction.triggered.connect(self.saveAs)

        closeAction = QtGui.QAction(u"Programm beenden...", self)
        closeAction.setShortcut("Ctrl+Q")
        closeAction.triggered.connect(self.close)

        mainMenu = self.menuBar()
        self.fileMenu = mainMenu.addMenu("Datei")
        self.fileMenu.addAction(newProjectAction)
        self.fileMenu.addAction(openAction)

        self.openRecentMenu = self.fileMenu.addMenu("Letze Projekte...")
        self.refreshRecentProjectsMenu()

        self.fileMenu.addAction(saveAction)
        self.fileMenu.addAction(saveAsAction)
        self.fileMenu.addAction(closeAction)


        editProjectMiscSettingsAction = QtGui.QAction(u"Projekteinstellungen...", self)
        editProjectMiscSettingsAction.triggered.connect(self.editProjectMiscSettings)

        editChannelsAction = QtGui.QAction(u"Kanaleinstellungen...", self)
        editChannelsAction.triggered.connect(self.editChannels)

        editCommandsAction = QtGui.QAction(u"Parametereinstellungen...", self)
        editCommandsAction.triggered.connect(self.editCommands)

        generateCCodeAction = QtGui.QAction(u"C-Code generieren", self)
        generateCCodeAction.triggered.connect(self.generateCCode)


        editMenu = mainMenu.addMenu("Bearbeiten")
        editMenu.addAction(editProjectMiscSettingsAction)
        editMenu.addAction(editChannelsAction)
        editMenu.addAction(editCommandsAction)
        editMenu.addAction(generateCCodeAction)


        showHelpAction = QtGui.QAction(u"Hilfe anzeigen...", self)
        showHelpAction.setShortcut("Ctrl+H")
        showHelpAction.setStatusTip(u"todo")
        showHelpAction.triggered.connect(self.showHelp)

        aboutAction = QtGui.QAction(u"Über das Programm...", self)
        aboutAction.triggered.connect(self.showAboutWindow)

        helpMenu = mainMenu.addMenu("Hilfe")
        helpMenu.addAction(showHelpAction)
        helpMenu.addAction(aboutAction)

    def refreshRecentProjectsMenu(self):
        self.openRecentMenu.clear()
        for i, recentPath in enumerate(self.applicationSettings.recentProjectFilePathes):
            displayPath = self.getProjectDisplayPath(recentPath)
            # displayPath = displayPath.split("/")
            # displayPath = displayPath[-1]
            # displayPath = displayPath.replace(".json", "")

            # action = QtGui.QAction(u"{}".format(displayPath), self)
            action = QtGui.QAction(u"{}".format(recentPath), self)
            action.triggered.connect(self.openRecent)
            action.setData(QtCore.QVariant(recentPath))
            self.openRecentMenu.addAction(action)


    def newProject(self):

        tempProjectSettings = ProjectSettings()

        accepted = self.editProjectMiscSettings(tempProjectSettings)

        if accepted == QtGui.QDialog.Accepted:
            self.closeCurrentProject()
            self.makeEmptyProject()
            self.projectSettings = tempProjectSettings
            self.projectSettings.tabSettingsDescriptions.append(TabDescription())
            self.projectSettings.changed.connect(self.projectSettingsChanged)

            tempPath = os.path.join(self.programRootFolder, "tempNew.json")

            self.saveAs(None, tempPath)
            self.loadProject(tempPath)
            self.projectSettings.openedFrom = u""
            self.applicationSettings.recentProjectFilePathes.popleft()
            self.refreshRecentProjectsMenu()


    def makeEmptyProject(self):
        self.projectSettings, self.channels, self.commands, self.messageFormatList, self.communicator = self.projectConfigManager.buildEmptyModel()
        self.projectSettings.changed.connect(self.projectSettingsChanged)

    def closeCurrentProject(self):
        while self.centralWidgetLayout.count() > 0:
            item = self.centralWidgetLayout.takeAt(0)
            item.widget().deleteLater()
        self.receiveTimer.stop()

    def open(self):

        if len(self.applicationSettings.recentProjectFilePathes) > 0:
            folderSuggestion = self.applicationSettings.recentProjectFilePathes[0]
        else:
            folderSuggestion = os.path.expanduser("~")


        projectFilePath = QtGui.QFileDialog.getOpenFileName(self,
                                                              "Open project file",
                                                              folderSuggestion,
                                                              "Project Settings (*.json)")
        projectFilePath = str(projectFilePath)
        if projectFilePath == "":
            return
        else:
            self.loadProject(projectFilePath)

    def openRecent(self, *args):
        recentPath = str(self.sender().data().toString())
        try:
            self.loadProject(recentPath)
        except IOError:
            self.displayMessage.emit("Konnte die Projektdatei nicht finden", "warning")

    def loadProject(self, pathToProjectFile):

        self.closeCurrentProject()

        self.projectSettings, self.channels, self.commands, self.messageFormatList, self.communicator = self.projectConfigManager.buildModelFromConfigFile(pathToProjectFile)
        self.projectSettings.changed.connect(self.projectSettingsChanged)
        self.channels.changed.connect(self.channelSetupChanged)

        self.communicator.setMessageMap(self.messageFormatList)
        self.communicator.connectToController()

        self.addTabs(self.projectSettings.tabSettingsDescriptions)

        self.applicationSettings.addRecentProjectPath(pathToProjectFile)

        displayPath = self.getProjectDisplayPath(pathToProjectFile)

        self.setWindowTitle(u"microRay - {}".format(displayPath))
        self.receiveTimer.start(self.applicationSettings.receiveMessageIntervalLengthInMs)

        self.setInitialValuesTimer.start(2000)

    def getProjectDisplayPath(self, fullProjectFilePath):
        displayPath = unicode(fullProjectFilePath)
        displayPath = os.path.split(displayPath)[1]
        return displayPath.replace(".json", "")


    def setInitialValues(self):
        self.commands.sendInitialValues()

    def projectSettingsChanged(self, newSettings):

        # self.receiveTimer.stop()
        # self.communicator.disconnectFromController()

        newWindowTitle = self.getProjectDisplayPath(self.projectSettings.openedFrom)
        if self.projectSettings.unsavedChanges is True:
            newWindowTitle += u" (unsaved)"
        self.setWindowTitle(u"microRay - {}".format(newWindowTitle))
        # todo rebuild communicator


        # self.communicator = self.projectConfigManager.makeCommunicator(self.projectSettings)
        # self.communicator.setMessageMap(self.messageFormatList)
        # self.communicator.connectToController()
        #
        # self.receiveTimer.start(self.applicationSettings.receiveMessageIntervalLengthInMs)

    def save(self):
        try:
            self.projectConfigManager.save(self.projectSettings, self.channels, self.commands)
        except IOError:
            self.displayMessage.emit("could not save project file", "warning")
            self.saveAs(None)
        self.projectSettings.unsavedChanges = False

    def saveAs(self, something, path=None):

        if path is None:
            filePathSuggestion = self.getSavePathSuggestion()

            projectFilePath = QtGui.QFileDialog.getSaveFileName(self,
                                                                  "Projekt speichern unter...",
                                                                  filePathSuggestion,
                                                                  "Project Settings (*.json)")
            projectFilePath = unicode(projectFilePath)
        else:
            projectFilePath = unicode(path)

        if len(projectFilePath) == 0:
            return
        else:
            try:
                self.projectConfigManager.saveAs(projectFilePath, self.projectSettings, self.channels, self.commands)
                self.applicationSettings.addRecentProjectPath(projectFilePath)
                self.projectSettings.unsavedChanges = False
            except IOError:
                self.displayMessage.emit("could not save project file", "warning")
                return

        # self.loadProject(projectFilePath)

    def getSavePathSuggestion(self):
        if len(self.projectSettings.openedFrom) > 0:
            folderSuggestion = self.projectSettings.openedFrom
        elif len(self.projectSettings.pathToControllerCodeFolder) > 0:
            folderSuggestion = self.projectSettings.pathToControllerCodeFolder
        elif len(self.applicationSettings.recentProjectFilePathes) > 0:
            folderSuggestion = self.applicationSettings.recentProjectFilePathes[0]
        else:
            folderSuggestion = os.path.expanduser("~")

        return folderSuggestion

        # fileNameSuggestion = self.projectSettings.projectName + ".json"
        # filePathSuggestion = os.path.join(folderSuggestion, fileNameSuggestion)


    def close(self):
        if self.projectSettings.unsavedChanges is True:
            pass
            # print "SAVE ?"
        else:
            QtCore.QCoreApplication.quit()


    def editProjectMiscSettings(self, settings):
        if settings is False or None:
            # happens when this function is called from a signal
            settings = self.projectSettings

        dialog = ProjectMiscSettingsDialog(settings)
        return dialog.updateSettings()


    def editChannels(self, settings):
        dialog = ChannelSettingsDialog(self.channels, self.applicationSettings)
        self.channels = dialog.updateChannels()

        self.receiveTimer.stop()

        newMessageMap = self.projectConfigManager.getMessageFormatList(self.channels)
        self.communicator.setMessageMap(newMessageMap)

        self.receiveTimer.start(self.applicationSettings.receiveMessageIntervalLengthInMs)

    def channelSetupChanged(self):
        pass

    def editCommands(self):
        dialog = CommandSettingsDialog(self.commands)
        dialog.updateSettings()

    def appSettingsChanged(self, settings):
        self.refreshRecentProjectsMenu()

    def generateCCode(self):

        self.communicator.disconnectFromController()
        try:
            self.includeFileMaker.generateIncludeFiles(self.projectSettings, self.channels, self.commands)
            if len(self.projectSettings.pathToControllerCodeFolder) == 0:
                path = self.programRootFolder
                self.displayMessage.emit(u"You can specify the include files target folder in the project settings.", "softWarning")
            else:
                path = self.projectSettings.pathToControllerCodeFolder
            self.displayMessage.emit(u"Include file generated in {}".format(path), "normal")
        except IOError as ex:
            if ex.errno == errno.ENOENT:
                self.displayMessage.emit(u"failed to generate code. Please specify output folder.", "warning")
        except:
            errorMessage = traceback.format_exc()
            self.displayMessage.emit(u"failed to generate code. Errormessage:\n{}".format(errorMessage), "warning")

        self.displayMessage.emit(u"Communication paused, recompile your controller code.", "softWarning")


    def showHelp(self):
        pathToIndexHtml = os.path.abspath(os.path.join(os.getcwd(), "documentation/index.html"))
        url = "file://" + pathToIndexHtml
        webbrowser.open(url)

    def showAboutWindow(self):
        aboutDialog = AboutDialog()
        aboutDialog.exec_()


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

    def handleNewData(self, message):
        MessageInterpreter.mapUserChannels(self.channels, message)
        returnedCommand = MessageInterpreter.getMicroControllerCommandReturned(message)

        try:
            command = self.commands.getCommandById(returnedCommand.id)
            self.commands[returnedCommand.id].checkMicroControllerReturnValue(returnedCommand)
        except:
            self.communicator._commState.state = CommState.WRONG_CONFIG
            self.communicator.commStateChanged.emit(self.communicator._commState)


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
        # print "bye bye"
        QtGui.QApplication.quit()

    def uncaughtExceptionOccured(self, exceptionString):
        print exceptionString