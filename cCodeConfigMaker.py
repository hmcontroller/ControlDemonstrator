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
C_FILE_HEADER_PATH = "controlDemonstrator.h"
C_FILE_CPP_PATH = "controlDemonstrator.cpp"
C_HEADER_TEMPLATE = "c_template.h"
C_C_TEMPLATE = "c_template.c"

AVAILABLE_FRAMEWORKS = {
    "mbed_2_udp": "MBED_2_UDP",
    "mbed_OS_udp": "MBED_OS_UDP",
    "arduino_udp": "ARDUINO_UDP"
}

def run():
    nameWidth = 40
    valueWidth = 6

    # First read the whole config file
    config = ConfigParser.SafeConfigParser(allow_no_value=True)
    config.optionxform = str
    config.read(P_CONFIG_FILE_PATH)

    frameworkAndInterface = config.get("misc", "microcontrollerFrameworkAndInterface")
    if not frameworkAndInterface in AVAILABLE_FRAMEWORKS:
        availables = ", ".join(AVAILABLE_FRAMEWORKS.iterkeys())
        raise Exception("please specify a framework out of the following list: {}".format(availables))
    # interface = config.get("misc", "commInterface")

    loopCycleTime = config.getint("misc", "loopCycleTimeUS")

    availableChannels = list()
    for i, section in enumerate(config.options('availableChannels')):
        availableChannels.append((i, section))
    availableChannelsCount = len(availableChannels)

    requestedChannels = list()
    for i, section in enumerate(config.options('requestedChannels')):
        foundOne = False
        for channel in availableChannels:
            if section == channel[1]:
                requestedChannels.append(channel)
                foundOne = True
        if foundOne is False:
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







    # now put all defines in the new file C_FILE_HEADER_PATH, will be overwritten
    # and all variables in C_FILE_CPP_PATH

    with open(C_FILE_HEADER_PATH, "w") as f:
        # include guard
        f.write("#ifndef CONFIG_H\n"
                "#define CONFIG_H\n")
        f.write("\n")

        #
        f.write("#define {}\n\n".format(AVAILABLE_FRAMEWORKS[frameworkAndInterface]))

        # some important variables here
        f.write("// must have parameters\n")
        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "LOOP_CYCLE_TIME_US", loopCycleTime, nameWidth=nameWidth, valueWidth=valueWidth))

        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "AVAILABLE_CHANNEL_COUNT", availableChannelsCount, nameWidth=nameWidth, valueWidth=valueWidth))
        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "REQUESTED_CHANNEL_COUNT", requestedChannelCount, nameWidth=nameWidth, valueWidth=valueWidth))

        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "PARAMETER_COUNT", availableParameterCount, nameWidth=nameWidth, valueWidth=valueWidth))
        # f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
        #     "REQUESTED_PARAMETER_COUNT", requestedParameterCount, nameWidth=nameWidth, valueWidth=valueWidth))

        f.write("\n")

        # # mark variables defined in the cpp file as extern
        # f.write("extern int channels[REQUESTED_CHANNEL_COUNT];\n\n")
        # f.write("extern int parameters[PARAMETER_COUNT];\n\n")

        # all available channels
        f.write('// All available channels\n' +
                '// Define names for parameters, that can be send to the connected pc.\n' +
                '// These names are referred to in the whole code.\n' +
                '// The list is generated automatically from a python script.\n' +
                '// On the controller all values are stored in "float channels[AVAILABLE_CHANNEL_COUNT]."\n'
                )
        for i, param in enumerate(availableChannels):
            macro = "(channels[{}])".format(i)
            f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
                param[1], macro, nameWidth=nameWidth, valueWidth=valueWidth))
        f.write("\n")

        # all available parameters
        f.write('// all available parameters\n' +
                '// Define names for parameters, that can be set from the connected pc.\n' +
                '// These names are referred to in the whole code.\n' +
                '// The list is generated automatically from a python script.\n' +
                '// On the controller all values are stored in "float parameters[AVAILABLE_PARAMETER_COUNT]."\n'
                )
        for i, param in enumerate(availableParameters):
            macro = "(parameters[{}])".format(i)
            f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
                param, macro, nameWidth=nameWidth, valueWidth=valueWidth))
        f.write("\n")

        with open(C_HEADER_TEMPLATE, "r") as headerTemplate:
            lines = headerTemplate.readlines()
        wholeText = "".join(lines)
        f.write(wholeText)
        f.write("\n")
        f.write("\n")

        # include guard end
        f.write("#endif")



    with open(C_FILE_CPP_PATH, "w") as f:
        #
        f.write('#include "controlDemonstrator.h"\n\n')

        # channel mapping
        f.write("// Channel values that will be send to the pc at every loop cycle\n")
        f.write("int requestedChannels[REQUESTED_CHANNEL_COUNT] = {\n")
        tString = ""
        for channel in requestedChannels:
            tString += "    {},\n".format(channel[0])
        tString = tString.rstrip(",\n")
        tString += "\n"
        f.write(tString)
        f.write("};\n")
        f.write("\n")

        with open(C_C_TEMPLATE, "r") as cTemplate:
            lines = cTemplate.readlines()
        wholeText = "".join(lines)
        f.write(wholeText)


if __name__ == "__main__":
    run()