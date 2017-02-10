#!/usr/bin/python3

"""
    "assign1.py", by Sean Soderman, Lee Boyd, and Corey Crosser.
    Automates all experiments within the first assignment.
    This is all going to be done in the same directory.
"""

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import re
import sys
import subprocess
from subprocess import STDOUT
#testFromLee
#testFromSean(amazing=True, ego='YES')
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
    #The command that will be formatted based on the command line arguments,
    #then executed...the double brackets are a trick to reuse this template,
    #essentially.
    mpiCmd = 'mpirun -np {{procs}} --{{byslotOrBynode}} --hostfile {{host}} {tachyonOrHpcc}'
    #Each host file we're using begins with a number and ends with the word
    #"hosts".
    hostTemplate = '{}hosts'
    ####Tachyon component
    if benchType == 'tachyon':
        #Used for grabbing the elapsed time in seconds from the ray tracer
        #output.
        timeReg = re.compile('Ray Tracing Time:\s*(\d*\.\d*)')
        #Stores (vms, time) information as tuples
        results = []
        template = mpiCmd.format(tachyonOrHpcc='./tachyon teapot.dat')
        #Execute this for 1 - 4 vms...
        for vms in range(1, 5):
            #2 slots per VM
            procs = vms * 2
            host = hostTemplate.format(vms)
            theCmd = template.format(byslotOrBynode=schedType, procs=procs, host=host)
            #Now run the command and grep for the bit that talks about
            #the number of seconds it took to run the command.
            try:
                output = str(subprocess.check_output(theCmd.split(), stderr=STDOUT),
                             encoding='UTF-8')
                #Debug print
                print(output)
                rayTime = timeReg.search(output).group(1)
                results.append( (vms, rayTime))
            except subprocess.CalledProcessError as cpe:
                sys.stderr.write("Uh oh: " + str(cpe))
        print(results)
        #Now plot the results as a line...will end up a graph of bynode or byslot, depending
        #on cmd line option. Unfortunately that means we will have two different graphs
        #to compare instead of having both lines on one graph.
        #Must unpack the results list tuples.
        redline,_ = plt.plot(list(map(lambda x: x[0], results)), 
                             list(map(lambda x: x[1], results)))
        #1-4 vms on the x axis, 0 to 2 seconds on the y...(it's fast, at least for
        #byslot scheduling.)
        plt.axis([1,4, 0, 2])
        plt.xlabel('Nodes')
        #It's in seconds by default, might convert to ms somewhere down the line.
        plt.ylabel('Runtime (s)')
        plt.title('Tachyon Results: {}'.format(schedType))
        #plt.legend()
        plt.savefig('tachyonresults.pdf')
