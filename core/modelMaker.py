# -*- encoding: utf-8 -*-
import ConfigParser
import json

from core.settingsModel import Settings
from core.command import Command


class ModelMaker():
    def __init__(self, configFilePath):
        self.configFilePath = configFilePath
        self.config = ConfigParser.SafeConfigParser(allow_no_value=True)
        self.config.optionxform = str
        self.config.read(self.configFilePath)

    def getCommands(self):
        commands = dict()
        for i, name in enumerate(self.config.options('requestedControlledParameters')):
            cmd = Command()
            cmd.value = 0
            cmd.id = i
            cmd.name = name
            commands[name] = cmd
        return commands

    def getMeasurementDataModel(self):
        pass

    def getMessageFormatList(self):
        pass

    def getSensorMapping(self):
        mappingString = self.config.get("Sensors", "mapping")
        mappingString = mappingString.replace("\n", "").replace(" ", "")
        return json.loads(mappingString)

    def getMiscSettings(self):
        settingsModel = Settings()
        settingsModel.controllerLoopCycleTime = self.config.getint("misc", "loopCycleTimeUS")
        settingsModel.bufferLength = self.config.getint("misc", "bufferSizePC")
        return settingsModel

