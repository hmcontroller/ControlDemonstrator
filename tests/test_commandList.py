# -*- encoding: utf-8 -*-
from unittest import TestCase

from core.command import Command, CommandList

class TestCommandList(TestCase):
    def setUp(self):
        self.command = Command()
        self.command.id = 3
        self.command.name = u"dudu3ä"

        self.commandList = CommandList()


    def test_append(self):
        self.commandList.append(self.command)
        self.assertIn(self.command, self.commandList)

    def test_removeCommand(self):
        self.commandList.append(self.command)
        self.assertIn(self.command, self.commandList)
        self.commandList.removeCommand(self.command)
        self.assertNotIn(self.command, self.commandList)

    def test_getCommandById(self):
        self.commandList.append(self.command)
        self.assertIn(self.command, self.commandList)
        self.assertIs(self.commandList.getCommandById(3), self.command)

    def test_getCommandByName(self):
        self.commandList.append(self.command)
        self.assertIn(self.command, self.commandList)
        self.assertIs(self.commandList.getCommandByName(self.command.name), self.command)

    # def test_commandChanged(self):
    #     self.fail()
    #
    # def test_sendPendingCommands(self):
    #     self.fail()
    #
    # def test_cancelPendingCommands(self):
    #     self.fail()
    #
    # def test_sendInitialValues(self):
    #     self.fail()