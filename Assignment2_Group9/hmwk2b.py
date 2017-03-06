#!/usr/bin env python
import sys
def mapper():
    #use below for mapreduce
    #for line in sys.stdin:
    f=open('/usr/local/hadoop-1.2.1/apd08.csv', 'r') #used for testing only
    #bi=open('badinput.txt', 'w')   
    listOfCrimes = [] #used for testing only
    badTypes = 0
    headers = 0
    makeLine = ""
    for line in f: #used for testing only
        line=line.strip()
        fields = line.split(",") #it's a csv
        mytype = fields[1] # type of crime
	if str(mytype) != '':
	    month = fields[2].split("/")[0] #month listed 1st in date is stripped of leading zeroes
            try:
                month = int(month)
                makeLine += mytype+","
                #sys.stdout.write(mytype+",") # do not print new line!!!!
                for i in range(1, 13):        
                    if i == int(month):
                        makeLine+=",1"
                        #sys.stdout.write(",1") #no newline
                    else:
                        makeLine+=",0"    
                        #sys.stdout.write(",0") # no newline
                makeLine+='\n'
                #print('\n')
            except ValueError:
                ValueError
                headers += 1
        else:
            badTypes += 1
        listOfCrimes.append(makeLine)
	makeLine=""
    #print(listOfCrimes)
    reducer(sorted(listOfCrimes))
    sys.stdout.write(str(headers) + " HEADERS, "+ str(badTypes) +" EMPTY TYPES" )
    #bi.write("BLANKCOUNT FOR TYPE: " + str(blankCounter))
    #bi.close()
def reducer(listOfLines):
    currentType = "" # String for current crime type
    # array of 13 ints. don't use position 0. This will prevent a
    #  subtraction in every itteration of the loop below
    currentTypeCounts[13] = 0
    allDates = []
    #for line in sys.stdin:
    for line in listOfCrimes:
        fields = line.split(",") #it's a csv
        #int(fields[1-12]) # convert these to ints
        if fields[0] == currentType:
            allDates.append(fields.GetRange(1,12))
        else: 
            if listOfCrimescurrentType != "": #only works if no blanks in csv
                currentTypeCounts = [sum(x) for x in zip(*allDates)]
                sys.stdout.write(currentType) # no newline!!!
                sys.stdout.write(currentTypeCounts) #seperated by commas
                sys.stdout.write('\n')
                for i in range(1, 13):
                    currentTypeCounts[i] = int(fields[i]);
                currentType=fields[0]
            else: # this should happen on 1st iteration only
                for i in range(1, 13):
                    currentTypeCounts[i] = int(fields[i]);
                allDates.append(currentTypeCounts)
                currentType=fields[0]
mapper()
