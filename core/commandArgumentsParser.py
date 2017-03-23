# -*- encoding: utf-8 -*-

from core.commandArgument import CommandArgument, CommandArguments
from core.commandArgument import AVAILABLE_COMMAND_ARGUMENTS

class CommandArgumentsParser(object):
    def __init__(self, command):
        self.command = command
        self.splittedArgumentStrings = list()
        self.splittedKeyValuePairs = list()
        self.arguments = list()

    def setCommandAttributesFromConfigFileArguments(self):
        self._splitArgumentString()
        self._splitSplittedArgumentStrings()
        self._createArgumentObjects()
        self._interpreteArgumentValues()
        self._writeArgumentsToCommand()
        return self.command

    def _splitArgumentString(self):
        self.splittedArgumentStrings = list()
        if self.command.rawArgumentString is not None:
            self.splittedArgumentStrings = self.command.rawArgumentString.split(CommandArgument.ARGUMENT_SEPARATOR)
        return self.splittedArgumentStrings

    def _splitSplittedArgumentStrings(self):
        for argument in self.splittedArgumentStrings:
            if CommandArgument.KEY_VALUE_SEPARATOR in argument:
                argParts = argument.split(CommandArgument.KEY_VALUE_SEPARATOR)
                argName = argParts[0].strip()
                argUninterpretedValue = argParts[1].strip()
            else:
                argName = argument.strip()
                argUninterpretedValue = None
            self.splittedKeyValuePairs.append((argName, argUninterpretedValue))
        return self.splittedKeyValuePairs

    def _createArgumentObjects(self):
        self.arguments = list()

        for arg in self.splittedKeyValuePairs:

            argName = arg[0]
            argUninterpretedValue = arg[1]

            if len(argName) == 0:
                continue

            if argName in AVAILABLE_COMMAND_ARGUMENTS:
                argObject = AVAILABLE_COMMAND_ARGUMENTS[argName]
            else:
                raise Exception("invalid option {} for {}".format(argName, self.command.name))

            argObject.name = argName
            argObject.uninterpretedValue = argUninterpretedValue
            self.arguments.append(argObject)
        return self.arguments

    def _interpreteArgumentValues(self):
        for arg in self.arguments:
            if arg.dataType is unicode:
                arg.value = arg.uninterpretedValue.decode('utf-8')
            elif arg.dataType is None:
                arg.value = True
            else:
                arg.value = arg.dataType(arg.uninterpretedValue)
        return self.arguments

    def _writeArgumentsToCommand(self):
        for arg in self.arguments:
            if arg.setterMethod is None:
                if hasattr(self.command, arg.attributeName):
                    setattr(self.command, arg.attributeName, arg.value)
                else:
                    raise Exception("Command has no attribute named {}".format(arg.attributeName))
            else:
                if hasattr(self.command, arg.setterMethod):
                    method = getattr(self.command, arg.setterMethod)
                    method(arg.value)
                else:
                    raise Exception("Command has no setter method named {}".format(arg.setterMethod))
        return self.command

    def createCommandArgumentsObject(self):
        args = CommandArguments()


