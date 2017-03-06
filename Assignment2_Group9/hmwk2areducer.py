#!/usr/bin/python2
import sys
#note because we are finding the single most dangerous address
#we can only use one reducer when we submit our jobdef reducer():
currentAddr = "" #string holds addr we're processing
addrCrimeCount = 0 #count of crimes at current addr
addrCrimesList = [] #list of crimes at current addr
mostDangerousAddr = ""  #you don't want to live here
maxCrimeCount = 0 #max crimes to beat
longestCrimeList = [] #list of crimes at worst place
#will use line below for mapreduce
#for line in stdin:
for line in sys.stdin:
     line=line.strip()
     words = line.split(",") #split mapper output
     
     addr = words[0]
     mytype = words[1] #type of crime commited
     if addr == currentAddr: #we're still at this addr
          addrCrimeCount+=1 #increment crime count here
          #add to list of crimes commited at this addr
          addrCrimesList.append(mytype)
     else: #we're to the next address
       #first check if we have a new max
          if addrCrimeCount > maxCrimeCount:
          #update max values
               maxCrimeCount = addrCrimeCount
               mostDangerousAddr = currentAddr
               longestCrimeList = addrCrimesList
       #initialize values for this new address
          currentAddr = addr
          addrCrimeCount = 1
          addrCrimesList = []
          addrCrimesList.append(mytype)
#done reading mapper output, but still need to check if the
#very last addr just happened to have the highest count
if addrCrimeCount > maxCrimeCount:
     maxCrimeCount = addrCrimeCount
     mostDangerousAddr = currentAddr
     longestCrimeList = addrCrimesList
#reducer output. Answers question 4
print(mostDangerousAddr + ": " + str(set(longestCrimeList)))
