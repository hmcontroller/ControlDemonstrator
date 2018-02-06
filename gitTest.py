# -*- encoding: utf-8 -*-

import os
import winreg

# import git

def run():


    os.environ['GIT_PYTHON_REFRESH'] = "quiet"
    from git import Repo # Ugly place to have the import...

    repo = Repo("D:\\00 eigene Daten\\000 FH\\S 4\\Regelungstechnik\\Regelungsversuch\\microRay")
    branch = repo.active_branch
    print branch.name
    # repo.git.checkout('devel')
    ding = repo.iter_commits('saveChecker..saveChecker@{u}')

    for dinddong in ding:
        print dinddong

if __name__ == "__main__":
    run()