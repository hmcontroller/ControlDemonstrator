# -*- encoding: utf-8 -*-

import os
import distutils.dir_util
import subprocess
import sys
import traceback
import time
import shutil

ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))

def run():
    pathToExtractedFolder = os.path.join(ROOT_FOLDER, "microRay")

    pathToInstallerExe = os.path.join(pathToExtractedFolder, "ucomplete.exe")
    os.remove(pathToInstallerExe)

    distutils.dir_util.copy_tree(pathToExtractedFolder, ROOT_FOLDER)

    exePath = os.path.join(ROOT_FOLDER, "microRay.exe")
    subprocess.Popen(exePath)



if __name__ == "__main__":
    time.sleep(3)
    try:
        run()
        pathToExtractedFolder = os.path.join(ROOT_FOLDER, "microRay")
        shutil.rmtree(pathToExtractedFolder)
    except:
        errorFilePath = os.path.join(ROOT_FOLDER, "updateError.txt")
        with open(errorFilePath, "w") as f:
            f.write(traceback.format_exc())
