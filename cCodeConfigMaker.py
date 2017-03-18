# -*- encoding: utf-8 -*-

"""
cCodeConfigMaker is a script to generate C-code for a microcontroller.
It reads the config.txt file, that must reside in the same directory.

At the time being, it generates a file called "config.h",
which one can copy to the microcontroller sourcecode directory.
"""

import ConfigParser
import json

P_CONFIG_FILE_PATH = "config.txt"
C_CONFIG_FILE_HEADER_PATH = "config.h"
C_CONFIG_FILE_CPP_PATH = "config.cpp"



def run():
    nameWidth = 40
    valueWidth = 6

    # First read the whole config file
    config = ConfigParser.SafeConfigParser(allow_no_value=True)
    config.optionxform = str
    config.read(P_CONFIG_FILE_PATH)

    loopCycleTime = config.getint("misc", "loopCycleTimeUS")

    availableChannels = list()
    for i, section in enumerate(config.options('availableChannels')):
        availableChannels.append(section)
    availableChannelsCount = len(availableChannels)

    requestedChannels = list()
    for i, section in enumerate(config.options('requestedChannels')):
        if section in availableChannels:
            requestedChannels.append(section)
        else:
            raise Exception("channel {} not available".format(section))
    requestedChannelCount = len(requestedChannels)


    availableParameters = list()
    for i, section in enumerate(config.options('availableParameters')):
        availableParameters.append(section)
    availableParameterCount = len(availableParameters)

    requestedParameters = list()
    for i, section in enumerate(config.options('requestedParameters')):
        if section in availableParameters:
            requestedParameters.append(section)
        else:
            raise Exception("command {} not available".format(section))
    requestedParameterCount = len(requestedParameters)







    # now put all defines in the new file C_CONFIG_FILE_HEADER_PATH, will be overwritten
    # and all variables in C_CONFIG_FILE_CPP_PATH

    with open(C_CONFIG_FILE_HEADER_PATH, "w") as f:
        # include guard
        f.write("#ifndef CONFIG_H\n"
                "#define CONFIG_H\n")
        f.write("\n")

        # some important variables here
        f.write("// must have parameters\n")
        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "LOOP_CYCLE_TIME_US", loopCycleTime, nameWidth=nameWidth, valueWidth=valueWidth))

        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "AVAILABLE_CHANNEL_COUNT", availableChannelsCount, nameWidth=nameWidth, valueWidth=valueWidth))
        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "REQUESTED_CHANNEL_COUNT", requestedChannelCount, nameWidth=nameWidth, valueWidth=valueWidth))

        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "AVAILABLE_PARAMETER_COUNT", availableParameterCount, nameWidth=nameWidth, valueWidth=valueWidth))
        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "REQUESTED_PARAMETER_COUNT", requestedParameterCount, nameWidth=nameWidth, valueWidth=valueWidth))

        f.write("\n")


        # all available channels
        f.write('// All available channels\n' +
                '// Define names for parameters, that can be send to the connected pc.\n' +
                '// These names are referred to in the whole code.\n' +
                '// The list is generated automatically from a python script.\n' +
                '// On the controller all values are stored in "float channels[AVAILABLE_CHANNEL_COUNT]."\n'
                )
        for i, param in enumerate(availableChannels):
            f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
                param, i, nameWidth=nameWidth, valueWidth=valueWidth))
        f.write("\n")

        # all available parameters
        f.write('// all available parameters\n' +
                '// Define names for parameters, that can be set from the connected pc.\n' +
                '// These names are referred to in the whole code.\n' +
                '// The list is generated automatically from a python script.\n' +
                '// On the controller all values are stored in "float parameters[AVAILABLE_PARAMETER_COUNT]."\n'
                )
        for i, param in enumerate(availableParameters):
            f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
                param, i, nameWidth=nameWidth, valueWidth=valueWidth))
        f.write("\n")


        # mark variables defined in the cpp file as extern
        f.write("extern int requestedChannels[REQUESTED_CHANNEL_COUNT];\n")
        f.write("extern int requestedParameters[REQUESTED_PARAMETER_COUNT];\n")

        # include guard end
        f.write("#endif")



    with open(C_CONFIG_FILE_CPP_PATH, "w") as f:
        #
        f.write('#include "config.h"\n')

        # channel mapping
        f.write("// Channel values that will be send to the pc at every loop cycle\n")
        f.write("int requestedChannels[REQUESTED_CHANNEL_COUNT] = {\n")
        tString = ""
        for i, param in enumerate(requestedChannels):
            tString += "    {},\n".format(param)
        tString = tString.rstrip(",\n")
        tString += "\n"
        f.write(tString)
        f.write("};\n")
        f.write("\n")

        # controlledParameter mapping
        f.write("// Parameters that can be set from the pc.\n")
        f.write("int requestedParameters[REQUESTED_PARAMETER_COUNT] = {\n")
        tString = ""
        for i, param in enumerate(requestedParameters):
            tString += "    {},\n".format(param)
        tString = tString.rstrip(",\n")
        tString += "\n"
        f.write(tString)
        f.write("};\n")
        f.write("\n")


if __name__ == "__main__":
    run()