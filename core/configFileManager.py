# -*- encoding: utf-8 -*-

import json


class ConfigFileManager(object):
    def __init__(self, applicationSettings, channels, commands):
        self.applicationSettings = applicationSettings
        self.channels = channels
        self.commands = commands

    def save(self):
        channels = list()
        for channel in self.channels.channels:
            channelDict = dict()
            channelDict["color"] = channel.colorRgbTuple
            channelDict["show"] = channel.show
            channelDict["id"] = channel.id
            channelDict["name"] = channel.name
            channels.append(channelDict)

        commands = list()
        for command in self.commands:
            commandDict = dict()
            commandDict["id"] = command.id
            commandDict["name"] = command.name
            commandDict["displayName"] = command.displayName
            commandDict["min"] = command._lowerLimit
            commandDict["max"] = command._upperLimit
            commandDict["value"] = command._value
            commandDict["pendingMode"] = command._pendingSendMode
            commands.append(commandDict)


        miscSettings = dict()

        miscSettings["controllerLoopCycleTimeInUs"] = self.applicationSettings.controllerLoopCycleTimeInUs
        miscSettings["bufferLength"] = self.applicationSettings.bufferLength
        miscSettings["guiUpdateIntervalLengthInMs"] = self.applicationSettings.guiUpdateIntervalLengthInMs
        miscSettings["receiveMessageIntervalLengthInMs"] = self.applicationSettings.receiveMessageIntervalLengthInMs
        miscSettings["sendMessageIntervalLengthInMs"] = self.applicationSettings.sendMessageIntervalLengthInMs
        miscSettings["computerIP"] = self.applicationSettings.computerIP
        miscSettings["controllerIP"] = self.applicationSettings.controllerIP
        miscSettings["udpPort"] = self.applicationSettings.udpPort
        miscSettings["controllerFrameworkAndInterface"] = self.applicationSettings.controllerFrameworkAndInterface


        everythingDict = dict()
        everythingDict["miscSettings"] = miscSettings
        everythingDict["channels"] = channels
        everythingDict["commands"] = commands


        with open("testConfig.txt", "w") as f:
            f.write(json.dumps(everythingDict, indent=4))



