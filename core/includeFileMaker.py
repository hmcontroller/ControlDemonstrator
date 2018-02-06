# -*- encoding: utf-8 -*-


from core.includeFileTemplates import *
from gui.constants import AVAILABLE_FRAMEWORKS
from core.command import Command

class IncludeFileMaker(object):
    def __init__(self):
        self.nameWidth = 40
        self.valueWidth = 6
        self.headerFileString = ""
        self.cFileString = ""
        self.projectSettings = None
        self.channels = None
        self.commands = None
        self.requestedChannels = list()
        self.unrequestedChannels = list()
        self.cFileName = "microRay.cpp"
        self.headerFileName = "microRay.h"



    @staticmethod
    def generateIncludeFiles(projectSettings, channels, commands):
        iMaker = IncludeFileMaker()
        iMaker.projectSettings = projectSettings
        iMaker.channels = channels
        iMaker.commands = commands

        iMaker.analyseModel()

        iMaker.makeHeaderFileString()
        iMaker.makeCFileString()

        iMaker.writeFilesToDisk()

    def analyseModel(self):
        for channel in self.channels.channels:
            if channel.isRequested:
                self.requestedChannels.append(channel)
            else:
                self.unrequestedChannels.append(channel)

    def makeHeaderFileString(self):
        self.addIncludeGuardStart()
        self.addFrameworkAndInterfaceDefinition()
        self.addSomeImportantMacros()
        self.addChannelsToHeaderFile()
        self.addCommandsToHeaderFile()
        self.addSerialAsExtern()

        self.addHeaderTemplate()

        self.addIncludeGuardEnd()

    def makeCFileString(self):
        # self.addIncludeToCFile()
        self.addIndependentFunctions()
        self.addSetInitialValuesFunctionToCFile()
        self.addCTemplate()

    def writeFilesToDisk(self):
        targetPathHeaderFile = os.path.join(self.projectSettings.pathToControllerCodeFolder, self.headerFileName)
        targetPathCFile = os.path.join(self.projectSettings.pathToControllerCodeFolder, self.cFileName)

        with open(targetPathHeaderFile, "w") as f:
            f.write(self.headerFileString)

        with open(targetPathCFile, "w") as f:
            f.write(self.cFileString)



    def addIncludeGuardStart(self):
        self.headerFileString += "#ifndef CONFIG_H\n"
        self.headerFileString += "#define CONFIG_H\n\n"

    def addIncludeGuardEnd(self):
        self.headerFileString += "#endif"

    def addFrameworkAndInterfaceDefinition(self):
        self.headerFileString += "#define {}\n\n".format(self.projectSettings.controllerFrameworkAndInterface)


    def addSomeImportantMacros(self):
        self.headerFileString +=  "// must have parameters\n"
        self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "loopCycleTimeUs", self.projectSettings.controllerLoopCycleTimeInUs,
            nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "CHANNELS_AVAILABLE_COUNT", len(self.channels.channels),
            nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "CHANNELS_REQUESTED_COUNT", len(self.requestedChannels),
            nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "CHANNELS_UNREQUESTED_COUNT", len(self.unrequestedChannels),
            nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "PARAMETER_COUNT", len(self.commands),
            nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "SPECIAL_COMMANDS_COUNT", len(self.commands.specialCmdList),
            nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "BAUD_RATE", self.projectSettings.comPortBaudRate,
            nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "INT_TYPE", Command.INT_TYPE,
            nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "FLOAT_TYPE", Command.FLOAT_TYPE,
            nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        if self.projectSettings.suppressParameterConfirmation is True:
            self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
                "SUPPRESS_PARAM_CONFIRMATION", "1",
                nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "RECORD_BUFFER_LENGTH", self.projectSettings.recordBufferLength,
            nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        pauseAfterRecord = 0
        if self.projectSettings.pauseAfterRecord is True:
            pauseAfterRecord = 1
        self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "PAUSE_AFTER_RECORD", pauseAfterRecord,
            nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        if self.projectSettings.debugMode is True:
            self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
                "mrDEBUG", "",
                nameWidth=self.nameWidth, valueWidth=self.valueWidth)

        messageSkipMode = 0
        if self.projectSettings.messageSkipMode is True:
            messageSkipMode = 1
        self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "MESSAGE_SKIP_MODE", messageSkipMode,
            nameWidth=self.nameWidth, valueWidth=self.valueWidth)



        self.headerFileString += "\n"


    def addChannelsToHeaderFile(self):
        # all requested channels
        self.headerFileString += "// All requested channels\n"
        for i, channel in enumerate(self.requestedChannels):
            macro = "(messageOutBuffer.channels[{}])".format(i)
            self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
                channel.name, macro, nameWidth=self.nameWidth, valueWidth=self.valueWidth)
        self.headerFileString += "\n"


        # all unrequested channels
        self.headerFileString += "// All unrequested channels\n"
        for i, channel in enumerate(self.unrequestedChannels):
            macro = "(unrequestedChannels[{}])".format(i)
            self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
                channel.name, macro, nameWidth=self.nameWidth, valueWidth=self.valueWidth)
        self.headerFileString += "\n"


    def addCommandsToHeaderFile(self):
        # all parameters
        self.headerFileString += "// all parameters\n"
        for i, command in enumerate(self.commands):
            macro = ""
            if command._valueType == Command.INT_TYPE:
                macro = "(parameters[{}]){}".format(i, ".valueInt")
            elif command._valueType == Command.FLOAT_TYPE:
                macro = "(parameters[{}]){}".format(i, ".valueFloat")
            self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
                command.name, macro, nameWidth=self.nameWidth, valueWidth=self.valueWidth)
        self.headerFileString += "\n"

        # all special parameters
        self.headerFileString += "// all special parameters\n"
        for i, command in enumerate(self.commands.specialCmdList):
            macro = "(specialCommands[{}])".format(i)
            self.headerFileString += "#define {:{nameWidth}} {:>{valueWidth}}\n".format(
                command.name, macro, nameWidth=self.nameWidth, valueWidth=self.valueWidth)
        self.headerFileString += "\n"


    def addSerialAsExtern(self):
        pass
        # if self.projectSettings.controllerFrameworkAndInterface == "MBED_OS_SERIAL":
        #     self.headerFileString += "extern Serial mrSerial;"



    def addHeaderTemplate(self):
        with open(headerTemplatePath, "r") as headerTemplate:
            lines = headerTemplate.readlines()
        templateText = "".join(lines)

        self.headerFileString += templateText

    def addIncludeToCFile(self):
        self.cFileString += '#include "{}"\n\n'.format(self.headerFileName)

    def addIndependentFunctions(self):
        with open(cIndependentFunctionsPath, "r") as cTemplate:
            lines = cTemplate.readlines()
        templateText = "".join(lines)

        self.cFileString += templateText


    def addSetInitialValuesFunctionToCFile(self):
        self.cFileString += "\n"

        self.cFileString += "Parameter parameters[] = {\n"
        for command in self.commands:
            if command._valueType == command.INT_TYPE:
                self.cFileString += "    {{ {dType}, {{ .valueInt = {value}}} }},\n".format(
                    dType=command._valueType, value=int(command.initialValue))
            elif command._valueType == command.FLOAT_TYPE:
                self.cFileString += "    {{ {dType}, {{ .valueFloat = {value}f}} }},\n".format(
                    dType=command._valueType, value=float(command.initialValue))
        self.cFileString = self.cFileString.rstrip(",\n")
        self.cFileString += "\n};\n\n"


        self.cFileString += "int specialCommands[] = {\n"
        for command in self.commands.specialCmdList:
            self.cFileString += "    {},\n".format(command.initialValue)
        self.cFileString = self.cFileString.rstrip(",\n")
        self.cFileString += "\n};\n\n"


    def addCTemplate(self):
        for aDict in AVAILABLE_FRAMEWORKS:
            if aDict["macroName"] == self.projectSettings.controllerFrameworkAndInterface:
                templateFileName = aDict["template"]
                templatePath = os.path.join(templateDir, templateFileName)
                with open(templatePath, "r") as cTemplate:
                    lines = cTemplate.readlines()
                templateText = "".join(lines)

                self.cFileString += templateText
