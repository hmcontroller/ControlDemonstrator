# -*- encoding: utf-8 -*-

from core.command import CommandConfirmation

class MessageInterpreter():
    def __init__(self):
        pass

    def mapUserChannels(self, measurementDataModel, messages):
        for i, message in enumerate(messages):
            if message.isUserChannel is True:
                measurementDataModel.channels[i].values.append(message.value)
            elif message.name == "loopStartTime":
                measurementDataModel.timeValues.append(message.value)

    def getLoopCycleDuration(self, messages):
        for i, message in enumerate(messages):
            if message.name == "lastLoopDuration":
                return message.value
        return None

    def getCommandConfirmation(self, messages):
        cmd = CommandConfirmation()
        for i, message in enumerate(messages):
            if message.name == "parameterNumber":
                cmd.id = message.value
            if message.name == "parameterValue":
                cmd.returnValue = message.value
        return cmd

