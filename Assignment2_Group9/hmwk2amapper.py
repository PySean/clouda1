#!/usr/bin env python
import sys
#f=open('/usr/local/hadoop-1.2.1/apd08.csv', 'r')
#will use line below for actual map
#for line in sys.stdin:
listOfCrimes = [] #only use for testing
for line in sys.stdin:
     line=line.strip()
     words=line.split(",") #it's a csv
     print(words[5] + "," + words[1]) #we need collumn 3 & 6
     #listOfCrimes.append(words[5] + "," + words[1]) #only use for testing
#testAddress=sorted(listOfCrimes)[0][0]
'''for testSort in sorted(listOfCrimes):
     if testSort==testAddress:
          print(testSort)
     else:
          testAddress = testSort'''
#reducer(sorted(listOfCrimes))
