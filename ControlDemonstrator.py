# -*- encoding: utf-8 -*-
import sys
import traceback

from PyQt4 import QtGui

from gui.mainWindow import ControlDemonstratorMainWindow


class Framerack(QtGui.QApplication):
    def __init__(self, args):
        QtGui.QApplication.__init__(self, args)
        self.mainW = ControlDemonstratorMainWindow()
        self.mainW.show()

    def notify(self, object, event):
        isex = False
        try:
            return QtGui.QApplication.notify(self, object, event)
        except Exception:
            isex = True
            print "Unexpected Error"
            print traceback.format_exception(*sys.exc_info())
            return False
        finally:
            if isex:
                self.quit()

    # def my_excepthook(selftype, value, tback):
    #     do stuff...
    #     sys.__excepthook__(type, value, tback)


def run():
    app = Framerack(sys.argv)
    sys.exit(app.exec_())

if __name__ == "__main__": run()
