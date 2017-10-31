# -*- encoding: utf-8 -*-

import json
from collections import deque
import os

from core.model.applicationSettings import ApplicationSettings

class ApplicationSettingsManager():
    def __init__(self, pathToSetttingsFile):
        self.settings = ApplicationSettings()
        self.pathToSettingsFile = pathToSetttingsFile

        self.settings.changed.connect(self.saveSettings)

    def saveSettings(self):
        jsonDicts = self.makeJsonDicts()
        with open(self.pathToSettingsFile, "w") as f:
            f.write(json.dumps(jsonDicts, indent=4))

    def makeJsonDicts(self):
        jsonAllSettingsDict = dict()
        jsonMiscSettingsDict = dict()

        jsonMiscSettingsDict["currentVersion"] = self.settings.currentVersion
        jsonMiscSettingsDict["guiUpdateIntervalLengthInMs"] = self.settings.guiUpdateIntervalLengthInMs
        jsonMiscSettingsDict["receiveMessageIntervalLengthInMs"] = self.settings.receiveMessageIntervalLengthInMs
        jsonMiscSettingsDict["sendMessageIntervalLengthInMs"] = self.settings.sendMessageIntervalLengthInMs
        jsonMiscSettingsDict["bufferLength"] = self.settings.bufferLength
        jsonMiscSettingsDict["autoSaveAfterCodeGeneration"] = self.settings.autoSaveAfterCodeGeneration

        recentProjects = list()
        for recentPath in self.settings.recentProjectFilePathes:
            recentProjects.append(recentPath)
        jsonMiscSettingsDict["recentProjects"] = recentProjects

        jsonAllSettingsDict["miscSettings"] = jsonMiscSettingsDict

        return jsonAllSettingsDict

    def restoreSettingsFromFile(self):
        jsonDicts = self.loadJsonFile()
        jsonMiscSettings = jsonDicts["miscSettings"]

        self.settings = ApplicationSettings()

        if "currentVersion" in jsonMiscSettings:
            self.settings.currentVersion = jsonMiscSettings["currentVersion"]

        if "guiUpdateIntervalLengthInMs" in jsonMiscSettings:
            self.settings.guiUpdateIntervalLengthInMs = jsonMiscSettings["guiUpdateIntervalLengthInMs"]

        if "receiveMessageIntervalLengthInMs" in jsonMiscSettings:
            self.settings.receiveMessageIntervalLengthInMs = jsonMiscSettings["receiveMessageIntervalLengthInMs"]

        if "sendMessageIntervalLengthInMs" in jsonMiscSettings:
            self.settings.sendMessageIntervalLengthInMs = jsonMiscSettings["sendMessageIntervalLengthInMs"]

        if "bufferLength" in jsonMiscSettings:
            self.settings.bufferLength = jsonMiscSettings["bufferLength"]


        if "recentProjects" in jsonMiscSettings:
            recentPathes = deque(maxlen=self.settings.maxRecentPathesCount)
            for recentPath in jsonMiscSettings["recentProjects"]:
                if os.path.isfile(recentPath):
                    recentPathes.append(recentPath)
            self.settings.recentProjectFilePathes = recentPathes

        if "autoSaveAfterCodeGeneration" in jsonMiscSettings:
            self.settings.autoSaveAfterCodeGeneration = jsonMiscSettings["autoSaveAfterCodeGeneration"]



        self.settings.changed.connect(self.saveSettings)

        return self.settings

    def loadJsonFile(self):
        with open(self.pathToSettingsFile, "r") as f:
            content = f.read()
            return json.loads(content)

