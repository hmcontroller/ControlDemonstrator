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
C_CONFIG_FILE_PATH = "config.h"



def run():
    nameWidth = 40
    valueWidth = 6

    # First read the whole config file
    config = ConfigParser.SafeConfigParser(allow_no_value=True)
    config.optionxform = str
    config.read(P_CONFIG_FILE_PATH)

    loopCycleTime = config.getint("misc", "loopCycleTimeUS")

    # # this feature has been removed
    # # read the sensor mapping
    # mappingString = config.get("Sensors", "mapping")
    # mappingString = mappingString.replace("\n", "").replace(" ", "")
    # sensorMapping = json.loads(mappingString)
    #
    # sensorCount = 0
    # requSensorCount = 0
    # for map in sensorMapping:
    #     sensorCount += 1
    #     if map[2] == 1:
    #         requSensorCount += 1


    availableFastParameters = list()
    for i, section in enumerate(config.options('availableFastParameters')):
        availableFastParameters.append(section)
    availableFastParametersCount = len(availableFastParameters)

    requestedFastParams = list()
    for i, section in enumerate(config.options('requestedFastParameters')):
        if section in availableFastParameters:
            requestedFastParams.append(section)
        else:
            raise Exception("channel {} not available".format(section))
    requestedFastParamsCount = len(requestedFastParams)


    availableControlledParameters = list()
    for i, section in enumerate(config.options('availableControlledParameters')):
        availableControlledParameters.append(section)
    availableControlledParameterCount = len(availableControlledParameters)

    requestedControlledParams = list()
    for i, section in enumerate(config.options('requestedControlledParameters')):
        if section in availableControlledParameters:
            requestedControlledParams.append(section)
        else:
            raise Exception("command {} not available".format(section))
    requestedControlledParameterCount = len(requestedControlledParams)







    # now put all stuff in the new file C_CONFIG_FILE_PATH


    with open(C_CONFIG_FILE_PATH, "w") as f:
        # include guard
        f.write("#ifndef CONFIG_H\n"
                "#define CONFIG_H\n")
        f.write("\n")

        # some important variables here
        f.write("// must have parameters\n")
        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "LOOP_CYCLE_TIME_US", loopCycleTime, nameWidth=nameWidth, valueWidth=valueWidth))

        # f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
        #     "SENSOR_COUNT", sensorCount, nameWidth=nameWidth, valueWidth=valueWidth))
        # f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
        #     "REQUESTED_SENSOR_COUNT", requSensorCount, nameWidth=nameWidth, valueWidth=valueWidth))

        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "FAST_PARAMETER_COUNT", availableFastParametersCount, nameWidth=nameWidth, valueWidth=valueWidth))
        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "REQUESTED_FAST_PARAMETER_COUNT", requestedFastParamsCount, nameWidth=nameWidth, valueWidth=valueWidth))

        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "CONTROLLED_PARAMETER_COUNT", availableControlledParameterCount, nameWidth=nameWidth, valueWidth=valueWidth))
        f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
            "REQUESTED_CONTROLLED_PARAMETER_COUNT", requestedControlledParameterCount, nameWidth=nameWidth, valueWidth=valueWidth))

        f.write("\n")


        # all available fast parameters
        f.write('// all available fast parameters\n' +
                '// define names for parameters, that can be send to the connected pc.\n' +
                '// These names are referred to in the whole code.\n' +
                '// The list is generated automatically from a python script\n' +
                '// On the controller all values are stored in "float fastParameterValues[FAST_PARAMETER_COUNT]"\n'
                )
        for i, param in enumerate(availableFastParameters):
            f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
                param, i, nameWidth=nameWidth, valueWidth=valueWidth))
        f.write("\n")

        # all available controlled parameters
        f.write('// all available controlled parameters\n' +
                '// define names for parameters, that can be set from the connected pc.\n' +
                '// These names are referred to in the whole code.\n' +
                '// The list is generated automatically from a python script\n' +
                '// On the controller all values are stored in "float controlledParameterValues[CONTROLLED_PARAMETER_COUNT]"\n'
                )
        for i, param in enumerate(availableControlledParameters):
            f.write("#define {:{nameWidth}} {:>{valueWidth}}\n".format(
                param, i, nameWidth=nameWidth, valueWidth=valueWidth))
        f.write("\n")


        # # start creating the needed mapping arrays
        #
        # # sensor mapping
        # f.write('// sensor channels, that will be measured\n' +
        #         '// [0]: switchCase for aquisition method, see "void aquireSensordata()"\n' +
        #         '// [1]: a parameter for the aquistion method\n' +
        #         '// [2]: storage destination (also used for messageOut position)\n' +
        #         '// if storage destination is <0, the channel will not be send to the pc\n'
        #         )
        # f.write("int sensorMapping[SENSOR_COUNT][3] = \n")
        # f.write(json.dumps(sensorMapping).replace("[", "{").replace("]", "}") + ";\n")
        # f.write("\n")

        # fastParameter mapping
        f.write("// parameters that will be send to the pc at every loop cycle\n")
        f.write("int requestedFastParameters[REQUESTED_FAST_PARAMETER_COUNT] = {\n")
        tString = ""
        for i, param in enumerate(requestedFastParams):
            tString += "    {},\n".format(param)
        tString = tString.rstrip(",\n")
        tString += "\n"
        f.write(tString)
        f.write("};\n")
        f.write("\n")

        # controlledParameter mapping
        f.write("// parameters that will be set from the pc\n")
        f.write("int requestedControlledParameters[CONTROLLED_PARAMETER_COUNT] = {\n")
        tString = ""
        for i, param in enumerate(requestedControlledParams):
            tString += "    {},\n".format(param)
        tString = tString.rstrip(",\n")
        tString += "\n"
        f.write(tString)
        f.write("};\n")
        f.write("\n")

        # include guard end
        f.write("#endif")

if __name__ == "__main__":
    run()