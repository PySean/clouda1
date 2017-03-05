def mapper:
     for line in stdin:
          words=line.split(",") #it's a csv
          print(words[5] + "," + words[1]) #we need collumn 3 & 6



#note because we are finding the single most dangerous address
#we can only use one reducer when we submit our job
def reducer:
     currentAddr = "" #string holds addr we're processing
     addrCrimeCount = 0 #count of crimes at current addr
     addrCrimesList = "" #list of crimes at current addr
     mostDangerousAddr = "" #you don't want to live here
     maxCrimeCount = 0 #max crimes to beat
     longestCrimeList = "" #list of crimes at worst place
    
     for line in stdin:
          words = line.split(",") #split mapper output
          addr = words[0]
          type = words[1] #type of crime commited
          if addr == currentAddr: #we're still at this addr
               addrCrimeCount+=1 #increment crime count here
               #add to list of crimes commited at this addr
               addrCrimesList.append(type + ", ")
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
          addrCrimesList = type + ", "
     #done reading mapper output, but still need to check if the
     #very last addr just happend to have the highest count
     if addrCrimeCount > maxCrimeCount:
          maxCrimeCount = addrCrimeCount
          mostDangerousAddr = currentAddr
          longestCrimeList = addrCrimesList
     #reducer output. Answers question 4
     print(mostDangerousAddr + ": " + longestCrimeList)
     #note that this may output the same crime multiple times
     #so we may want to store the crimes in a unique list instead
     #of a string
