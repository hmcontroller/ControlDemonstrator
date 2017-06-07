# -*- encoding: utf-8 -*-

import os
import ctypes
import traceback

def run():
    programRootFolder = u'C:\\Program Files (x86)\\microRay'

    exePath = u'"{}"'.format(os.path.join(programRootFolder, u"ucomplete.exe"))


    pathToExtractedUpdateFolder = u'"{}"'.format(u"D:\\TEMP\\microRay\\extractedUpdate\\microRay")
    targetDirectory = u'"{}"'.format(programRootFolder)

    exeArgs = pathToExtractedUpdateFolder + u" " + targetDirectory

    print exePath, exeArgs

    try:
        # print ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), u"", None, 1)
        print ctypes.windll.shell32.ShellExecuteW(None, u"runas", exePath, exeArgs, None, 1)

        # subprocess.Popen([exePath, pathToMicroRayTempFolder, targetDirectory])

        # QtGui.QApplication.quit()

        # das nicht nehmen
        # sys.exit(0)
    except:
        print traceback.format_exc()

if __name__ == "__main__":
    run()