#!/usr/bin/python3

"""
    "assign1.py", by Sean Soderman, Lee Boyd, and Corey Crosser.
    Automates all experiments within the first assignment.
    This is all going to be done in the same directory.
"""

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os
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
        reddots, = plt.plot(list(map(lambda x: x[0], results)), 
                             list(map(lambda x: x[1], results)), 'ro')
        #1-4 vms on the x axis, 0 to 2 seconds on the y...(it's fast, at least for
        #byslot scheduling.)
        plt.axis([0,5, 0, 2])
        plt.xlabel('Nodes')
        #It's in seconds by default, might convert to ms somewhere down the line.
        plt.ylabel('Runtime (s)')
        plt.title('Tachyon Results: {}'.format(schedType))
        #plt.legend()
        plt.savefig('tachyonresults.pdf')
    ###HPCC component
    elif benchType == 'hpcc':
        #Unfortunately, we have to read in the hpccinf file, modify then spit
        #it out repeatedly because of how the hpcc benchmark works.
        #We also have to read in the output file, delete it, then read it in again
        #after the next program execution...

        #For the hpl benchmark
        hplReg = re.compile('WR11C2R4.*(\d+\.\d+e(\+|-)\d+)')
        #For the ptrans benchmark: Introducing the most beautiful regex of all time.
        #ptransReg = re.compile('WALL.*(\d+\.\d+).*')
        ptransReg = re.compile(('WALL\s*\S*\s*\S*\s*\S*\s*\S*\s*\S*'
                                '\s*\S*\s*\S*\s*\S*\s*(\d+\.\d+)'))
        template = mpiCmd.format(tachyonOrHpcc='./hpcc')
        hpccinfTemplate = ''
        #Read in the hpccinf file, turn the Q part into a format string for
        #easy replacement.
        with open('hpccinf.txt', 'r') as infile:
            for line in infile:
                #Here's the line we were looking for! Replace the number with brackets.
                if line.endswith('Qs\n'):
                    #Strings in python are immutable, which is really dumb but oh well.
                    listLine = list(line)
                    listLine[0:2] = '{}'
                    hpccinfTemplate += ''.join(listLine)
                else:
                    hpccinfTemplate += line
        #These will both store tuples of the form (vm,time) for both benchmarks.
        hplResults = []
        ptransResults = []
        for vms in range(1, 5):
            #Just going to set the "Q" value in the input file to whatever np is.
            procs = vms * 2
            Q=vms
            #print("Q="+str(Q))
            host = hostTemplate.format(vms)
            theCmd = template.format(byslotOrBynode=schedType, procs=procs, host=host)
            curHpc = hpccinfTemplate.format(Q)
            #Remove the current output file before each iteration if it exists.
            if os.path.exists('hpccoutf.txt'):
                os.unlink('hpccoutf.txt')
            try:
                #Spit out the appropriate input file with according Q value.
                with open('hpccinf.txt', 'w') as infile:
                    infile.write(curHpc)
                subprocess.check_output(theCmd.split(), stderr=STDOUT)
                #Iterate through output file, gather relevant info.
                with open('hpccoutf.txt', 'r') as resfile:
                    #Need these to average the WALL values for the PTRANS benchmark.
                    wallCounter = 0
                    ptransTotal = 0
                    for line in resfile:
                        hplMatch = hplReg.search(line)
                        ptransMatch = ptransReg.search(line)
                        #If we hit the line with the gflops result...
                        if hplMatch is not None:
                            hplFlops = float(hplMatch.group(1))
                            #This is safe to do, as it only happens once in the entire file.
                            hplResults.append( (vms, hplFlops) )
                        #If we hit a WALL line, accumulate the time, inc the counter.
                        elif ptransMatch is not None:
                            ptransTotal += float(ptransMatch.group(1))
                            wallCounter += 1
                    ptransAvg = ptransTotal / wallCounter
                    ptransResults.append((vms,  ptransAvg))
            except subprocess.CalledProcessError as cpe:
                sys.stderr.write('Uh oh: ' + str(cpe))
            #Ensure we did everything correctly...
            print("HPL data: {}".format(str(hplResults)))
            print("PTRANS data: {}".format(str(ptransResults)))
            #Now plot a graph for HPL and PTRANS, respectively.
            hplDots, = plt.plot(list(map(lambda x: x[0], hplResults)), 
                                 list(map(lambda x: x[1], hplResults)), 'ro')
            #0-5 vms on the x axis, 0 to 7 gflops on the y.
            plt.axis([0,5, 0, 7])
            plt.xlabel('Nodes')
            #It's in seconds by default, might convert to ms somewhere down the line.
            plt.ylabel('Gflops')
            plt.title('HPL Results: {}'.format(schedType))
            #plt.legend()
            plt.savefig('hpl{}.pdf'.format(schedType))
            #Clear the figure on the next plot command.
            plt.hold(False)
            ptransDots, = plt.plot(list(map(lambda x: x[0], ptransResults)), 
                                 list(map(lambda x: x[1], ptransResults)), 'ro')
            #0-5 vms on the x axis, 0 to 1.5 GB/s on the y.
            plt.axis([0,5, 0, 1.5])
            plt.xlabel('Nodes')
            #It's in seconds by default, might convert to ms somewhere down the line.
            plt.ylabel('GB/s')
            plt.title('PTRANS Results: {}'.format(schedType))
            #plt.legend()
            plt.savefig('ptrans{}.pdf'.format(schedType))
