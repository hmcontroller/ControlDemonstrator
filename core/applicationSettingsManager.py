# -*- encoding: utf-8 -*-

import json
from collections import deque

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

        jsonMiscSettingsDict["guiUpdateIntervalLengthInMs"] = self.settings.guiUpdateIntervalLengthInMs
        jsonMiscSettingsDict["receiveMessageIntervalLengthInMs"] = self.settings.receiveMessageIntervalLengthInMs
        jsonMiscSettingsDict["sendMessageIntervalLengthInMs"] = self.settings.sendMessageIntervalLengthInMs
        jsonMiscSettingsDict["bufferLength"] = self.settings.bufferLength

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
        self.settings.guiUpdateIntervalLengthInMs = jsonMiscSettings["guiUpdateIntervalLengthInMs"]
        self.settings.receiveMessageIntervalLengthInMs = jsonMiscSettings["receiveMessageIntervalLengthInMs"]
        self.settings.sendMessageIntervalLengthInMs = jsonMiscSettings["sendMessageIntervalLengthInMs"]
        self.settings.bufferLength = jsonMiscSettings["bufferLength"]

        recentPathes = deque(maxlen=5)
        for recentPath in jsonMiscSettings["recentProjects"]:
            recentPathes.append(recentPath)
        self.settings.recentProjectFilePathes = recentPathes

        self.settings.changed.connect(self.saveSettings)

        return self.settings

    def loadJsonFile(self):
        with open(self.pathToSettingsFile, "r") as f:
            content = f.read()
            return json.loads(content)


    def appendRecentProjectPath(self, path):
        newRecentPathes = deque(maxlen=5)

        for i in range(0, len(self.settings.recentProjectFilePathes)):
            if not self.settings.recentProjectFilePathes[i] == path:
                newRecentPathes.append(self.settings.recentProjectFilePathes[i])

        self.settings.recentProjectFilePathes = newRecentPathes
        self.settings.recentProjectFilePathes.appendleft(path)
