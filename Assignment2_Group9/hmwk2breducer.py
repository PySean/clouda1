#!/usr/bin/env python
import sys
currentType = "" # String for current crime type
# array of 13 ints. don't use position 0. This will prevent a
#  subtraction in every itteration of the loop below
currentTypeCounts=[0]*13
#allDates = []
lineTester = 0
#for line in listOfCrimes:
for line in sys.stdin:
    #lineTester+=1
    fields = line.split(",") #it's a csv
    #int(fields[1-12]) # convert these to ints
    if fields[0] == currentType:
        for i in range(1,13):
            #print("line " + str(lineTester) + line)
            currentTypeCounts[i]+=int(fields[i])
            #allDates.append(currentTypeCounts)
    else: 
        if currentType != "": #only works if no blanks in csv
            #currentTypeCounts = [sum(x) for x in zip(*allDates)]
            sys.stdout.write(currentType) # no newline!!!
            for typeCounts in currentTypeCounts[1:]:
                sys.stdout.write(','+str(typeCounts))
            #sys.stdout.write(str(currentTypeCounts[1:])) #seperated by commas
            sys.stdout.write('\n')
            #bi.write(currentType)
            #bi.write(str(currentTypeCounts[1:]))
            #bi.write('\n')
            for i in range(1, 13):
                currentTypeCounts[i] = int(fields[i])
            #allDates = []
            #allDates.append(currentTypeCounts)
            currentType=fields[0]
        else: # this should happen on 1st iteration only
            for i in range(1, 13):
                currentTypeCounts[i] = int(fields[i])
            #allDates.append(currentTypeCounts)
            currentType=fields[0]
#bi.close()
