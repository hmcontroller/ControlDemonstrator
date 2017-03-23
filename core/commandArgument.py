# -*- encoding: utf-8 -*-

class CommandArguments(object):
    def __init__(self):
        self.value = None
        self.min = None
        self.max = None
        self.name = None
        self.pendingMode = None


class CommandArgument(object):

    ARGUMENT_SEPARATOR = ";"
    KEY_VALUE_SEPARATOR = "="

    def __init__(self, name, attributeName, dataType, setterMethod=None):
        self.name = name
        self.attributeName = attributeName
        self.value = None
        self.uninterpretedValue = None
        self.dataType = dataType
        self.setterMethod = setterMethod


AVAILABLE_COMMAND_ARGUMENTS = {
    "value": CommandArgument("value", None, float, "setValueWithLimitsAdaptation"),
    "min": CommandArgument("min", None, float, "setLowerLimit"),
    "Min": CommandArgument("Min", None, float, "setLowerLimit"),
    "max": CommandArgument("max", None, float, "setUpperLimit"),
    "Max": CommandArgument("Max", None, float, "setUpperLimit"),
    "name": CommandArgument("name", "displayName", unicode),
    "Name": CommandArgument("Name", "displayName", unicode),
    "pending": CommandArgument("pending", None, None, "setPendingSendMode"),
}