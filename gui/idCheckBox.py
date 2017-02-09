# -*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class IdCheckbox(QtGui.QCheckBox):

    changed = QtCore.pyqtSignal(int, int, int)

    def __init__(self, parent=None, id=None, channelType=None):
        QtGui.QCheckBox.__init__(self, parent)
        self.id = id
        self.channelType = channelType
        self.stateChanged.connect(self.statiChanged)

    def statiChanged(self, state):
        self.changed.emit(self.id, state, self.channelType)

