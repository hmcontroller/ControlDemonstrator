# -*- encoding: utf-8 -*-
import os
import sys
import ctypes
import logging
import webbrowser
import errno
import traceback
import subprocess
import time
import tempfile

from PyQt4 import QtCore, QtGui

from core.hardwareInterfaces import UdpInterface, UsbHidInterface, SerialInterface
from core.messageInterpreter import MessageInterpreter
from core.configFileManager import ConfigFileManager
from core.applicationSettingsManager import ApplicationSettingsManager
from core.model.projectSettings import ProjectSettings
from core.includeFileMaker import IncludeFileMaker
from core.updateChecker import UpdateChecker
from core.backGroundTask import BackgroundTask
from core.updateDownloader import UpdateDownloader

from gui.aboutDialog import AboutDialog
from gui.applicationSettingsDialog import ApplicationSettingsDialog
from gui.projectMiscSettingsDialog import ProjectMiscSettingsDialog
from gui.channelSettingsDialog import ChannelSettingsDialog
from gui.commandSettingsDialog import CommandSettingsDialog
from gui.valuesToInitialValuesDialog import ValuesToInitialValuesDialog

from gui.constants import *
from gui.tabWaterLineExperiment import TabWaterLineExperiment
from gui.tabGenericView import TabGenericView
from gui.tabSmallGenericView import TabSmallGenericView
from gui.resources import *

from gui.serialMonitor import SerialMonitor


class MicroRayMainWindow(QtGui.QMainWindow):

    displayMessage = QtCore.pyqtSignal(object, object)

    def __init__(self, exceptionMagnet, logger, rootFolder, tempFolder, settingsFolder, splashScreen):
        QtGui.QMainWindow.__init__(self)

        exceptionMagnet.caughtException.connect(self.uncaughtExceptionOccured)

        self.logger = logger

        self.runningFromSource = True
        if getattr(sys, 'frozen', False):
            self.runningFromSource = False

        self.programRootFolder = rootFolder
        self.microRayTempFolder = tempFolder
        self.programSettingsFolder = settingsFolder

        # pipe stdout
        self.myPrinter = MyPrinter(self)

        self.lastDutyCycleTimeExceededWarning = u""
        self.lastTransmissionLagWarning = u""

        # some calculations for debugging purpose
        self.loopDurationMin = 1000000
        self.loopDurationMax = 0
        self.loopDurationAverage = 0
        self.loopDurationSum = 0
        self.loopDurationCounter = 0


        splashScreen.setProgress(0.4)
        splashScreen.setMessage(u"loading settings")

        QtGui.qApp.processEvents()


        pixmap = QtGui.QPixmap(iconPath)
        icon = QtGui.QIcon(pixmap)
        QtGui.QApplication.setWindowIcon(icon)

        appSettingsPath = os.path.join(self.programSettingsFolder, RELATIVE_PATH_TO_APPLICATION_SETTINGS)

        self.appSettingsManager = ApplicationSettingsManager(appSettingsPath)
        if os.path.isfile(appSettingsPath):
            self.applicationSettings = self.appSettingsManager.restoreSettingsFromFile()
        else:
            self.applicationSettings = self.appSettingsManager.settings

        self.applicationSettings.currentVersion = VERSION_NUMBER
        self.appSettingsManager.saveSettings()

        self.applicationSettings.changed.connect(self.appSettingsChanged)
        self.applicationSettings.bufferLengthChanged.connect(self.bufferLengthChanged)


        self.setWindowTitle("microRay {}".format(self.applicationSettings.currentVersion))

        self.serialMonitor = SerialMonitor()
        self.serialMonitor.commandInput.connect(self.sendRawCommand)

        # setup a timer, that triggers to read from the controller
        self.receiveTimer = QtCore.QTimer()
        self.receiveTimer.setSingleShot(False)
        self.receiveTimer.timeout.connect(self.receiveAndSend)


        self.projectConfigManager = ConfigFileManager(self.applicationSettings)


        self.setupUi()

        splashScreen.setProgress(0.5)
        QtGui.qApp.processEvents()




        self.screenRect = QtGui.QApplication.desktop().screenGeometry()
        self.setGeometry(self.screenRect.width() * 0.05, self.screenRect.height() * 0.05,
                         self.screenRect.width() * 0.9, self.screenRect.height() * 0.9)


        # show the application on the second monitor as maximized window
        if self.runningFromSource:
            self.screenRectSecondMonitor = QtGui.QApplication.desktop().screenGeometry(1)
            self.setGeometry(self.screenRect.width(), 0,
                             self.screenRectSecondMonitor.width() * 0.9, self.screenRectSecondMonitor.height() * 0.9)
        self.showMaximized()


        splashScreen.setProgress(0.6)
        splashScreen.setMessage(u"loading project")
        QtGui.qApp.processEvents()




        # self.setInitialValuesTimer = QtCore.QTimer()
        # self.setInitialValuesTimer.setSingleShot(True)
        # self.setInitialValuesTimer.timeout.connect(self.setInitialValues)


        if len(sys.argv) > 1:
            pathToProjectFile = u""
            try:
                pathToProjectFile = unicode(sys.argv[1])
                self.loadProject(pathToProjectFile)
            except IOError:
                dialog = QtGui.QErrorMessage(self)
                dialog.showMessage(u"Projektdatei wurde nicht gefunden.\n\n{}".format(pathToProjectFile))
            except:
                dialog = QtGui.QErrorMessage()
                dialog.showMessage(u"Projektdatei konnte nicht geladen werden.")

        elif len(self.applicationSettings.recentProjectFilePathes) > 0:
            try:
                self.loadProject(self.applicationSettings.recentProjectFilePathes[0])
            except IOError:
                dialog = QtGui.QErrorMessage()
                dialog.showMessage(u"Projektdatei wurde nicht gefunden.\n\n{}".format(self.applicationSettings.recentProjectFilePathes[0]))
            except:
                dialog = QtGui.QErrorMessage()
                dialog.showMessage(u"Projektdatei konnte nicht geladen werden.")

        # self.receiveTimer.start(self.applicationSettings.receiveMessageIntervalLengthInMs)

        splashScreen.setProgress(0.8)
        QtGui.qApp.processEvents()

        # for debugging purpose
        self.loopReportTimer = QtCore.QTimer()
        self.loopReportTimer.setSingleShot(False)
        self.connect(self.loopReportTimer, QtCore.SIGNAL("timeout()"), self.printLoopPerformance)
        self.loopReportTimer.start(5000)



        # self.displayMessage.emit("Dev version 30", "normal")

        self.updateCheckerTask = BackgroundTask(UpdateChecker, self.updateCheckFinished)
        self.downloadUpdateTask = BackgroundTask(UpdateDownloader, self.updateDownloadFinished, self.updateDownloadProgress)

        self.updateCheckerTask.startWork()

        # time.sleep(3)
        splashScreen.finish(self)
        self.logger.info("GUI load complete")


        # self.testWindow = TestMessageBoardWindow()
        # self.testWindow.show()




    def updateCheckFinished(self, something):
        if something[0] is None:
            # self.displayMessage.emit("Update check failed:\n{}".format(something[1]), "softWarning")
            self.displayMessage.emit(u"Could not check for updates.", "softWarning")
        else:
            availableVersion = something[0]
            pathToArchive = something[1]

            if availableVersion > self.applicationSettings.currentVersion:

                dialog = QtGui.QMessageBox(self)
                dialog.setWindowTitle(u"New version alert")
                dialog.setText(u"Good morning. A new version of microRay called v{} is available.".format(availableVersion))
                dialog.setInformativeText(u"Would you like to download it now?")
                dialog.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)

                # prevents the cancel button to be shown
                # dialog.setDefaultButton(QtGui.QMessageBox.Ok)

                userResponse = dialog.exec_()

                if userResponse == QtGui.QMessageBox.Ok:
                    if self.runningFromSource is False:
                        self.displayMessage.emit(u"Download of update started to {}.".format(self.microRayTempFolder), "normal")
                        fullUri = MRAY_URI + "/" + pathToArchive
                        self.downloadUpdateTask.startWork((fullUri, self.microRayTempFolder))
                else:
                    pass
            else:
                self.displayMessage.emit("Newest version installed.", "normal")


    def updateDownloadProgress(self, progress):
        self.displayMessage.emit(progress, "normal")

    def updateDownloadFinished(self, something):
        if something[0] is not None:
            dialog = QtGui.QMessageBox(self)
            dialog.setWindowTitle(u"Last update")
            dialog.setText(u"Update complete. Restart now?")
            dialog.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            # dialog.setDefaultButton(QtGui.QMessageBox.Ok)
            userResponse = dialog.exec_()

            if userResponse == QtGui.QMessageBox.Ok:
                self.restartMRayAndApplyUpdate()

    def restartMRayAndApplyUpdate(self):
        if self.runningFromSource is False:
            exePath = u'"{}"'.format(os.path.join(self.programRootFolder, u"ucomplete1.exe"))

            pathToExtractedUpdateFolder = os.path.join(self.microRayTempFolder, "extractedUpdate\\microRay")
            pathToExtractedUpdateFolder = u'"{}"'.format(pathToExtractedUpdateFolder)

            targetDirectory = u'"{}"'.format(self.programRootFolder)

            exeArgs = pathToExtractedUpdateFolder + u" " + targetDirectory

            try:
                # subprocess.Popen([exePath, pathToExtractedFolder, targetDirectory])

                # hopefully this asks for UAC elevation, because ucomplete needs admin rights
                returnCode = ctypes.windll.shell32.ShellExecuteW(None, u"runas", exePath, exeArgs, None, 1)
                if returnCode == 42:
                    QtGui.QApplication.quit()
                else:
                    self.displayMessage.emit("could not restart microRay, errorCode {}".format(returnCode), "softWarning")

                # das nicht nehmen
                # sys.exit(0)
            except:
                self.displayMessage.emit(traceback.format_exc(), "warning")
                self.logger.info(traceback.format_exc())

    def setupUi(self):
        self.centralwidget = BackgroundWidget(self)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        # styleSheetPartOne = "{" + "background-image: url({});".format("./gui/resources/iconWithoutBackground.png") + "}"
        # styleSheet = "BackgroundWidget#centralwidget {}".format(styleSheetPartOne)
        # self.centralwidget.setStyleSheet(styleSheet)

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
                classInstance = TabWaterLineExperiment(self.commands,
                                                       self.channels,
                                                       self.applicationSettings,
                                                       self.projectSettings,
                                                       self.communicator,
                                                       self,
                                                       self.serialMonitor)
            elif givenTab.className == "TabSmallGenericView":
                classInstance = TabSmallGenericView(self.commands,
                                                    self.channels,
                                                    self.applicationSettings,
                                                    self.projectSettings,
                                                    self.communicator,
                                                    self,
                                                    self.serialMonitor)
            elif givenTab.className == "TabGenericView":
                classInstance = TabGenericView(self.commands,
                                               self.channels,
                                               self.applicationSettings,
                                               self.projectSettings,
                                               self.communicator,
                                               self,
                                               self.serialMonitor)
            else:
                raise ValueError("inappropriate tab given in project file")


            tabLayout.addWidget(classInstance)





        # tabPath = "D:\\00 eigene Daten\\000 FH\\S 4\\Regelungstechnik\\Regelungsversuch\\microRay\\tabWaterLineExperiment.py"
        # # tabClassName = "TabWaterLineExperiment"
        # #
        # # tabContentClass = getattr(import_module(tabPath), tabClassName)
        # # tabContentClassInstance = tabContentClass(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator)
        #
        # tabContentClass = imp.load_source("tabWaterLineExperiment.TabWaterLineExperiment", tabPath)
        #
        # tabContentClassInstance = tabContentClass(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator)
        #
        # tab = QtGui.QWidget()
        # tab.setFont(font)
        # tabLayout = QtGui.QHBoxLayout(tab)
        # tabLayout.setSpacing(0)
        # tabLayout.setMargin(0)
        # self.tabWidget.addTab(tab, u"TESTTAB")
        #
        # # don't do this dynamically, otherwise pyinstaller stops working
        # # tabContentClass = getattr(import_module(givenTab.pathToClassFile), givenTab.className)
        # # tabContentClassInstance = tabContentClass(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator)
        #
        # tabLayout.addWidget(tabContentClassInstance)






    def addOnlyOneWidget(self, tabs):
        tab = tabs[0]

        classInstance = None

        # don't do this dynamically, otherwise pyinstaller stops working
        # tabContentClass = getattr(import_module(givenTab.pathToClassFile), givenTab.className)
        # tabContentClassInstance = tabContentClass(self.commands, self.channels, self.applicationSettings, self.projectSettings, self.communicator)

        if tab.className == "TabWaterLineExperiment":
            classInstance = TabWaterLineExperiment(self.commands,
                                                   self.channels,
                                                   self.applicationSettings,
                                                   self.projectSettings,
                                                   self.communicator,
                                                   self,
                                                   self.serialMonitor)
        elif tab.className == "TabSmallGenericView":
            classInstance = TabSmallGenericView(self.commands,
                                                self.channels,
                                                self.applicationSettings,
                                                self.projectSettings,
                                                self.communicator,
                                                self,
                                                self.serialMonitor)
        elif tab.className == "TabGenericView":
            classInstance = TabGenericView(self.commands,
                                           self.channels,
                                           self.applicationSettings,
                                           self.projectSettings,
                                           self.communicator,
                                           self,
                                           self.serialMonitor)
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

        editAppSettingsAction = QtGui.QAction(u"Einstellungen...", self)
        editAppSettingsAction.triggered.connect(self.editApplicationSettings)

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

        self.fileMenu.addSeparator()

        self.fileMenu.addAction(editAppSettingsAction)

        self.fileMenu.addSeparator()

        self.fileMenu.addAction(closeAction)


        editProjectMiscSettingsAction = QtGui.QAction(u"Projekteinstellungen...", self)
        editProjectMiscSettingsAction.triggered.connect(self.editProjectMiscSettings)


        editCommandsAction = QtGui.QAction(u"Parametereinstellungen...", self)
        editCommandsAction.triggered.connect(self.editCommands)

        editChannelsAction = QtGui.QAction(u"Kanaleinstellungen...", self)
        editChannelsAction.triggered.connect(self.editChannels)



        generateCCodeAction = QtGui.QAction(u"C-Code generieren", self)
        generateCCodeAction.setShortcut("Ctrl+G")
        generateCCodeAction.triggered.connect(self.generateCCode)

        actualValuesToInitialValuesAction = QtGui.QAction(u"aktuelle Parameterwerte als Startwerte übernehmen...", self)
        actualValuesToInitialValuesAction.triggered.connect(self.setActualValuesToInitialValues)

        editMenu = mainMenu.addMenu("Schnittstelle")
        editMenu.addAction(editProjectMiscSettingsAction)
        editMenu.addAction(editCommandsAction)
        editMenu.addAction(editChannelsAction)

        editMenu.addSeparator()

        editMenu.addAction(generateCCodeAction)

        editMenu.addSeparator()

        editMenu.addAction(actualValuesToInitialValuesAction)


        showHelpAction = QtGui.QAction(u"Hilfe anzeigen...", self)
        showHelpAction.setShortcut("Ctrl+H")
        showHelpAction.setStatusTip(u"todo")
        showHelpAction.triggered.connect(self.showHelp)

        showOnlineHelpAction = QtGui.QAction(u"Onlinehilfe anzeigen...", self)
        showOnlineHelpAction.triggered.connect(self.showOnlineHelp)

        showOfficialWebsiteAction = QtGui.QAction(u"inoffizielle Website anzeigen...", self)
        showOfficialWebsiteAction.triggered.connect(self.showWebsite)


        aboutAction = QtGui.QAction(u"Über das Programm...", self)
        aboutAction.triggered.connect(self.showAboutWindow)

        helpMenu = mainMenu.addMenu("Hilfe")
        helpMenu.addAction(showHelpAction)
        helpMenu.addAction(showOnlineHelpAction)
        helpMenu.addAction(showOfficialWebsiteAction)
        helpMenu.addSeparator()
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
            self.projectSettings.changed.connect(self.projectSettingsChanged)

            tempPath = os.path.join(self.programSettingsFolder, "tempNewProject.mRay")

            self.saveAs(None, tempPath)
            self.loadProject(tempPath)
            self.projectSettings.openedFrom = u""
            self.applicationSettings.recentProjectFilePathes.popleft()
            self.refreshRecentProjectsMenu()


    def makeEmptyProject(self):
        self.projectSettings, self.channels, self.commands, self.messageFormatList, self.communicator = self.projectConfigManager.buildEmptyModel()
        self.projectSettings.changed.connect(self.projectSettingsChanged)

        for cmd in self.commands.specialCmdList:
            # attention this must also be changed in self.loadProject
            cmd.specialCommandReceived.connect(self.specialCommandCheck)

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
                                                              "mRay project (*.mRay *.json *)")
        # projectFilePath = unicode(projectFilePath)

        self.logger.info(type(projectFilePath))

        # das geht nicht
        # self.logger.info(type(projectFilePath.toUnicode()))

        # das geht auch nicht
        # projectFilePath = projectFilePath.decode('utf-8')

        projectFilePath = unicode(projectFilePath)

        self.logger.info(type(projectFilePath))
        self.logger.info(projectFilePath)


        if projectFilePath == u"":
            return
        else:
            self.loadProject(projectFilePath)

    def openRecent(self, *args):
        recentPath = unicode(self.sender().data().toString())
        try:
            self.loadProject(recentPath)
        except IOError:
            self.displayMessage.emit("Konnte die Projektdatei nicht finden", "warning")

    def loadProject(self, pathToProjectFile):

        self.closeCurrentProject()

        self.projectSettings, self.channels, self.commands, self.messageFormatList, self.communicator = self.projectConfigManager.buildModelFromConfigFile(pathToProjectFile)
        self.projectSettings.changed.connect(self.projectSettingsChanged)
        self.channels.changed.connect(self.channelSetupChanged)

        for cmd in self.commands.specialCmdList:
            # attention this must also be changed in self.makeEmptyProject
            cmd.specialCommandReceived.connect(self.specialCommandCheck)

        self.communicator.setMessageMap(self.messageFormatList)
        self.communicator.connectToController()


        self.addTabs(self.projectSettings.tabSettingsDescriptions)

        self.applicationSettings.addRecentProjectPath(pathToProjectFile)

        displayPath = self.getProjectDisplayPath(pathToProjectFile)

        # self.setWindowTitle(u"microRay - {}".format(displayPath))
        self.setWindowTitle(u"microRay {}    -    {}".format(self.applicationSettings.currentVersion, displayPath))

        self.receiveTimer.start(self.applicationSettings.receiveMessageIntervalLengthInMs)

        # self.setInitialValuesTimer.start(2000)

    def getProjectDisplayPath(self, fullProjectFilePath):
        displayPath = unicode(fullProjectFilePath)
        # displayPath = os.path.split(displayPath)[1]
        # displayPath = displayPath.replace(".mRay", "")
        return displayPath


    def setInitialValues(self):
        self.commands.sendInitialValues()

    def projectSettingsChanged(self, newSettings):

        # self.receiveTimer.stop()
        # self.communicator.disconnectFromController()

        newWindowTitle = self.getProjectDisplayPath(self.projectSettings.openedFrom)
        if self.projectSettings.unsavedChanges is True:
            newWindowTitle += u" (unsaved)"
        self.setWindowTitle(u"microRay {} - {}".format(self.applicationSettings.currentVersion, newWindowTitle))
        # todo rebuild communicator


        # self.communicator = self.projectConfigManager.makeCommunicator(self.projectSettings)
        # self.communicator.setMessageMap(self.messageFormatList)
        # self.communicator.connectToController()
        #
        # self.receiveTimer.start(self.applicationSettings.receiveMessageIntervalLengthInMs)

    def save(self):
        try:
            self.projectConfigManager.save(self.projectSettings, self.channels, self.commands)
            self.projectSettings.unsavedChanges = False
            self.displayMessage.emit("Project file saved.", "normal")
        except IOError:
            # self.displayMessage.emit("could not save project file", "warning")
            self.saveAs(None)

    def saveAs(self, something, path=None):

        if path is None:
            filePathSuggestion = self.getSavePathSuggestion()

            ## when using this, an ugly qt dialog will be shown...
            # fileDialog = QtGui.QFileDialog(self,
            #                               "Projekt speichern unter...",
            #                               filePathSuggestion)
            # fileDialog.setDefaultSuffix(".mRay")
            # # fileDialog.setFileMode(QtGui.QFileDialog.E)
            #
            # projectFilePath = fileDialog.exec_()


            projectFilePath = QtGui.QFileDialog.getSaveFileName(self,
                                                                  "Projekt speichern unter...",
                                                                  filePathSuggestion,
                                                                  "mRay project (*.mRay *)")
            projectFilePath = unicode(projectFilePath)
        else:
            projectFilePath = unicode(path)

        if len(projectFilePath) == 0:
            return
        else:
            if projectFilePath.endswith(".mRay"):
                pass
            else:
                projectFilePath += ".mRay"
            try:
                self.projectConfigManager.saveAs(projectFilePath, self.projectSettings, self.channels, self.commands)
                self.applicationSettings.addRecentProjectPath(projectFilePath)
                self.projectSettings.unsavedChanges = False
                self.displayMessage.emit(u"Project file saved under {}.".format(projectFilePath), "normal")
            except IOError:
                self.displayMessage.emit(u"could not save project file", "warning")
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


    def editApplicationSettings(self):
        # self.communicator.disconnectFromController()
        accepted = ApplicationSettingsDialog.updateSettings(self.applicationSettings)

        if accepted:
            self.appSettingsManager.saveSettings()
            # self.channels.actualizeBufferLength(self.applicationSettings.bufferLength)

        # self.communicator.connectToController()


    def bufferLengthChanged(self):
        self.communicator.disconnectFromController()
        self.channels.actualizeBufferLength(self.applicationSettings.bufferLength)
        self.communicator.connectToController()

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


        accepted = ProjectMiscSettingsDialog.updateSettings(settings)

        if accepted and hasattr(self, "communicator"):
            self.receiveTimer.stop()
            self.communicator.setInterface(self.messageFormatList)
            newMessageMap = self.projectConfigManager.getMessageFormatList(self.channels, self.projectSettings)
            self.communicator.setMessageMap(newMessageMap)

            self.receiveTimer.start(self.applicationSettings.receiveMessageIntervalLengthInMs)
        return accepted



    def editChannels(self, settings):
        # raise Exception(u"guuä")
        dialog = ChannelSettingsDialog(self.channels, self.applicationSettings)
        self.channels = dialog.updateChannels()

        self.receiveTimer.stop()

        newMessageMap = self.projectConfigManager.getMessageFormatList(self.channels, self.projectSettings)
        self.communicator.setMessageMap(newMessageMap)

        self.receiveTimer.start(self.applicationSettings.receiveMessageIntervalLengthInMs)

    def channelSetupChanged(self):
        pass

    def editCommands(self):
        dialog = CommandSettingsDialog(self.commands)
        while 1:
            try:
                dialog.updateSettings()
                break
            except:
                break

    def appSettingsChanged(self, settings):
        self.refreshRecentProjectsMenu()

    def generateCCode(self):

        if isinstance(self.communicator.interface, SerialInterface) and self.projectSettings.controllerFrameworkAndInterface == "ARDUINO_SERIAL":
            self.communicator.disconnectFromController()

        showControllerPathHint = False

        try:
            IncludeFileMaker.generateIncludeFiles(self.projectSettings, self.channels, self.commands)
            if len(self.projectSettings.pathToControllerCodeFolder) == 0:
                path = self.programRootFolder
                showControllerPathHint = True

            else:
                path = self.projectSettings.pathToControllerCodeFolder
            self.displayMessage.emit(u"Include file generated in {}".format(path), "normal")
            if showControllerPathHint is True:
                self.displayMessage.emit(u"You can specify the include files target folder in the project settings.", "softWarning")
            self.save()
        except IOError as ex:
            if ex.errno == errno.ENOENT:
                self.displayMessage.emit(u"failed to generate code. Please specify output folder.", "warning")
        except:
            errorMessage = traceback.format_exc()
            self.displayMessage.emit(u"failed to generate code. Errormessage:\n{}".format(errorMessage), "warning")

        # if isinstance(self.communicator.interface, SerialInterface):
        #     self.displayMessage.emit(u"Communication paused, please recompile your controller code.", "warning")
        # else:
        #     self.displayMessage.emit(u"Please recompile your controller code.", "warning")

    def setActualValuesToInitialValues(self):
        dialog = ValuesToInitialValuesDialog(self.commands)
        self.commands = dialog.doIt()

    def showHelp(self):
        pathToIndexHtml = os.path.abspath(os.path.join(self.programRootFolder, "documentation/index.html"))
        url = "file://" + pathToIndexHtml
        webbrowser.open(url)

    def showOnlineHelp(self):
        webbrowser.open(MRAY_ONLINE_HELP)

    def showWebsite(self):
        webbrowser.open(MRAY_WEBSITE)

    def showAboutWindow(self):
        aboutDialog = AboutDialog()
        aboutDialog.exec_()

    def receiveAndSend(self):
        self.receive()
        self.send()

    def receive(self):
        receivedData = self.communicator.receive()
        for message in receivedData.messages:
            self.handleNewData(message)
            # self.calculateSomeStuff(message)
        if len(receivedData.messageAsChars) > 0:
            self.serialMonitor.showMessage(receivedData.messageAsChars)

    def send(self):
        self.communicator.send(self.commands)

    def handleNewData(self, message):
        MessageInterpreter.mapUserChannels(self.channels, message)
        MessageInterpreter.checkStatusFlags(self.communicator.microcontrollerStatus, message)
        try:
            returnedCommand = MessageInterpreter.getMicroControllerCommandReturned(message, self.commands)
        except:
            self.communicator.microcontrollerStatus.badData = True

        try:
            command = self.commands.getCommandById(returnedCommand.id)
            self.commands[returnedCommand.id].checkMicroControllerReturnValue(returnedCommand)
        except:
            try:
                command = self.commands.getSpecialCommandById(returnedCommand.id)
                command.checkSpecialCommandReturnValue(returnedCommand)
            except:
                self.communicator.microcontrollerStatus.badData = True
                # self.communicator.commState.state = CommState.WRONG_CONFIG

    def sendRawCommand(self, command):
        self.communicator.sendRawCommand(command)

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
        if len(exceptionString) > 0 and exceptionString != '' and exceptionString != ' ' and exceptionString != '\n':
            if isinstance(exceptionString, str):
                try:
                    exceptionString = exceptionString.decode('utf-8')
                except:
                    return

            # self.displayMessage.emit(exceptionString, "warning")

            slotCount = self.receivers(self.displayMessage.signal)
            if slotCount > 0:
                self.displayMessage.emit(u"PRINT: {}".format(exceptionString), "warning")
                self.logger.error(u"uncaught exception")
                self.logger.error(u"".format(exceptionString))
            else:
                messageBox = QtGui.QErrorMessage(self)
                messageBox.showMessage(u"PRINT: {}".format(exceptionString))
                self.logger.error(u"".format(exceptionString))


    def specialCommandCheck(self, command):

        # duty cylce time exceeded
        if command.id == -1:
            if command.valueOfLastResponse > 0.2:

                warning = "Duty cycle time exceeded by {} us.".format(command.valueOfLastResponse)
                if warning != self.lastDutyCycleTimeExceededWarning:
                    self.displayMessage.emit(warning, "warning")
                    self.lastDutyCycleTimeExceededWarning = warning

        # serial send took took too long
        if command.id == -2:
            # print command.valueOfLastResponse
            if command.valueOfLastResponse > 0.2:
                # self.skippedData.emit(int(command.valueOfLastResponse))
                warning = "Transmission lag. {} bytes from last loop. Deactivate some channels or increase your loop time.".format(int(command.valueOfLastResponse))
                if warning != self.lastTransmissionLagWarning:
                    # self.displayMessage.emit(warning, "warning")
                    self.lastTransmissionLagWarning = warning


class BackgroundWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(BackgroundWidget, self).__init__(parent)

    # def paintEvent(self, QPaintEvent):
    #     styleOption = QtGui.QStyleOption()
    #     styleOption.init(self)
    #     painter = QtGui.QPainter(self)
    #     self.style().drawPrimitive(QtGui.QStyle.PE_Widget, styleOption, painter, self)

    def paintEvent(self, QPaintEvent):
        pixmap = QtGui.QPixmap(iconWithLightBackgroundPath)
        painter = QtGui.QPainter(self)
        pixmap = pixmap.scaled(200, 200)
        painter.drawPixmap((self.width() / 2) - 100, (self.height() / 2) - 100, pixmap)

        # pen = QtGui.QPen(QtCore.Qt.darkGray)
        # painter.setPen(pen)
        #
        # font = QtGui.QFont("Monospace", 60)
        # font.setStyleHint(QtGui.QFont.TypeWriter)
        # painter.setFont(font)
        #
        # textRect = QtCore.QRect(0, 0, self.width(), self.height())
        #
        #
        #
        # painter.drawText(textRect,
        #                  QtCore.Qt.AlignCenter,
        #                  QtCore.QString(u"μR"))



class MyPrinter(object):
    def __init__(self, mainW):
        sys.stdout = self
        self.mainW = mainW

    def write(self, someString):
        if len(someString) > 0 and someString != '' and someString != ' ' and someString != '\n':
            if isinstance(someString, str):
                someString = someString.decode('utf-8')

            slotCount = self.mainW.receivers(self.mainW.displayMessage.signal)
            if slotCount > 0:
                self.mainW.displayMessage.emit(u"PRINT: {}".format(someString), "softWarning")
            else:
                messageBox = QtGui.QErrorMessage(self.mainW)
                messageBox.showMessage(u"PRINT: {}".format(someString))
