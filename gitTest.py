# -*- encoding: utf-8 -*-

import os
import winreg

import sys
print sys.path

for aPath in os.environ["PATH"].split(";"):
    print aPath
# import git

def run():


    os.environ['GIT_PYTHON_REFRESH'] = "quiet"
    from git import Repo

    repo = Repo("D:\\00 eigene Daten\\000 FH\\S 4\\Regelungstechnik\\Regelungsversuch\\microRay")
    branch = repo.active_branch
    print branch.name
    # repo.git.checkout('devel') # funktioniert nur, wenn git im Path drinsteht

    # Länge ist, wieviele commits der erste hinter dem zweiten her ist (@{u} heißt remote)
    ding = list(repo.iter_commits('saveChecker@{u}..saveChecker'))
    print len(ding)
    for dingDong in ding:
        # dingDong ist die Revisionsnummer der Commits, die im Vergleich zu anderen in der Zukunft liegen
        print dingDong


if __name__ == "__main__":
    run()