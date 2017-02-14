# -*- encoding: utf-8 -*-
from PyQt4 import QtGui


CHANNEL_COLORS = list()
CHANNEL_COLORS.append((190, 0, 0))
CHANNEL_COLORS.append((0, 150, 0))
CHANNEL_COLORS.append((0, 153, 255))
CHANNEL_COLORS.append((255, 165, 0))
CHANNEL_COLORS.append((222, 184, 135))
CHANNEL_COLORS.append((0, 139, 139))
CHANNEL_COLORS.append((143, 188, 143))
CHANNEL_COLORS.append((255, 215, 0))

CHECK_BOX_FONT = QtGui.QFont()
CHECK_BOX_FONT.setPointSize(8)

USER_INPUT_WARNING_COLOR = QtGui.QColor(255, 165, 0)
CONFIRMATION_WARNING_COLOR = QtGui.QColor(210, 0, 0)

HOVER_COLOR = QtGui.QColor(200, 200, 200)
MOUSE_DOWN_COLOR = QtGui.QColor(150, 150, 150)

# TODO unused
CABLE_PEN = QtGui.QPen()
CABLE_PEN.setColor(QtGui.QColor(0, 0, 0))
CABLE_PEN.setCosmetic(True)
CABLE_PEN.setWidth(2)