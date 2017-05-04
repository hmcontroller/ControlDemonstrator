# -*- encoding: utf-8 -*-

import json

from core.model.applicationSettings import ApplicationSettings

class ApplicationSettingsManager():
    def __init__(self, pathToSetttingsFile):
        self.settings = ApplicationSettings()
        self.pathToSettingsFile = pathToSetttingsFile

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
        return self.settings

    def loadJsonFile(self):
        with open(self.pathToSettingsFile, "r") as f:
            content = f.read()
            return json.loads(content)