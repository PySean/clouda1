#!/usr/bin/env python
import sys   
#listOfCrimes = [] #used for testing only
badTypes = 0
headers = 0
makeLine = ""
for line in sys.stdin: #used for testing only
    line=line.strip()
    fields = line.split(",") #it's a csv
    mytype = fields[1] # type of crime
    if str(mytype) != '':
        month = fields[2].split("/")[0] #month listed 1st in date is stripped of leading zeroes
        try:
            month = int(month)
            makeLine += mytype
            #sys.stdout.write(mytype+",") # do not print new line!!!!
            for i in range(1, 13):        
                if i == int(month):
                    makeLine+=",1"
                    #sys.stdout.write(",1") #no newline
                else:
                    makeLine+=",0"    
                    #sys.stdout.write(",0") # no newline
            #makeLine+='\n'
            #listOfCrimes.append(makeLine)
            print(makeLine)
            makeLine=""
            #print('\n')
        except ValueError:
            ValueError
            headers += 1
    else:
        badTypes += 1
   #bi.write(makeLine)
   #listOfCrimes.append(makeLine)
#makeLine=""
#print(listOfCrimes)
#bi.close()
#sys.stdout.write(str(headers) + " HEADERS, "+ str(badTypes) +" EMPTY TYPES" )
    #bi.write("BLANKCOUNT FOR TYPE: " + str(blankCounter))
    #bi.close()
    
