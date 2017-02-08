#!/usr/bin/python3

"""
    "assign1.py", by Sean Soderman, Lee Boyd, and Corey Crosser.
    Automates all experiments within the first assignment.
    This is all going to be done in the same directory.
"""

import re
import sys
import subprocess

"""
    Set up arguments for parsing...
"""
if __name__ == '__main__':
    usage = ('Usage: assign1.py -benchmark=[tachyon|hpcc]'
                     ' -sched=[byslot|bynode]\n')
    if len(sys.argv) < 3:
        sys.stderr.write(usage)
        sys.exit(1)
    _, benchmark, scheduling = sys.argv
    argReg = re.compile('.*=(.*)')
    benchType = argReg.search(benchmark).group(1)
    schedType = argReg.search(scheduling).group(1)
    if benchType is None or (benchType != 'tachyon' and benchType != 'hpcc'):
        sys.stderr.write(usage)
        sys.exit(1)
    if schedType is None or (schedType != 'byslot' and schedType != 'bynode'):
        sys.stderr.write(usage)
        sys.exit(1)

    ####Tachyon component
