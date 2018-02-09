# -*- encoding: utf-8 -*-

import os, pip, subprocess

import sys


def run():

    # sys.path.append("C:\\Program Files\\Git\\bin")

    os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = "C:\\Program Files\\Git\\bin\\git.exe"

    print("syspath")
    for aPath in sys.path:
        print aPath

    pythonFound = False
    print("\n\npath\n")
    for aPath in os.environ["PATH"].split(";"):
        print aPath
        if "Python27" in aPath:
            pythonFound = True

    git_url = "https://github.com/hmcontroller/microRay.git"
    repo_dir = "D:\\mRayTestClonerRepo"

    from git import Repo
    if not os.path.isdir(repo_dir):
        Repo.clone_from(git_url, repo_dir)

    qtWhlPath = os.path.join(repo_dir, "PyQt4-4.11.4-cp27-cp27m-win32.whl")
    if pythonFound is True:

        try:
            subprocess.check_call("pip2.7 install -U pyserial", shell=True)
        except:
            print "failed to install pyserial"

        try:
            subprocess.check_call("pip2.7 install -U pyserial".format(qtWhlPath), shell=True)
        except:
            print "failed to install pyqt4"



if __name__ == "__main__":
    run()