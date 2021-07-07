# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 12:16:17 2021

@author: Steven Backues
"""
#from tkinter import Tk
#from tkinter.filedialog import askopenfilename
## Opens file.  I've been using LineCollectionTest.txt as a small test
#print("Please Select file...")
#print("(The file selection screen may appear BEHIND your current application)")
#Tk().withdraw()
#filename = askopenfilename()
#inputName = filename
#print("Given File Name: %s" %(filename))

#print(">>Enter INPUT PIF file path+name:")
#inputName = input()
#print ("Enter output name for projection data")
#outputName = input()
#Reads in the file, putting it into the object bodyText. 

inStream = open("LineCollectionTest.txt", "r")
bodyText = []
print(inStream)
for line in inStream:
    data = line.split()
    bodyID = int(data[0])
    bodyText.append(line)
inStream.close()
#print ("bodyText")
#print(bodyText)
#Collects the lines that are in the slice.  Here the slice is 123-124.  Prints it
lineCollection = []
bodySliceNums = []
index = 0 

for bodyEntry in bodyText:
    bodyLine = bodyEntry.split()
    xValue = int(bodyLine[2])
    
    if(xValue <= (124) and xValue >= (123)):
        bodyID = int(bodyLine[0])
        
        try:
            index = bodySliceNums.index(bodyID)

            #print(lineCollection)
            
        except:
            bodySliceNums.append(bodyID)
            lineCollection.append([])

            
        posi = bodySliceNums.index(bodyID)
        lineCollection[posi].append(bodyEntry)
print ("lineCollection")        
print (lineCollection)
#now to get the slice for each body        
index1 = 1  
#print ("lineCollection[index1]")
#print (lineCollection[index1])

'''We build up the projection by going through each line in the lineCollection, checking if it is already in the projection, and, 
if not, adding it.  The outer loop is for each line in lineCollection.
The inner loop goes through each line currently in the projectionData string and compares it to the current line from the lineCollection
If it finds a match with identical Y and Z coordiantes it sets "found" to 1 and stops looking.  
If it goes through the entire projectionData without finding a match, it also stops looking.
Then it checks why it stopped looking, and if it wasn because it didn't find it (found = 0), at adds that line to the projectionData 
Then it moves on to the next line from the lineCollection'''    

# I will get rid of all the extraneous print statements on a later cleanup once this is for sure working

for array in lineCollection:
    index2 = 0
    currentArea = 0
    #print ("body array")
    #print (array)
    projectionData = []
    projectionData.append(array[index2].split())
    #print ("initial projection data")
    #print (projectionData)
    #lineData = lineCollection[index1][index2].split()
    for line in array:
        lineData = array[index2].split()
        currentBody = int(lineData[0])
        print ("Current Body")
        print (currentBody)
        print ("lineData")
        print (lineData)
        index3 = 0
        found = 0
        print ("length of projection data")
        print (len(projectionData))
        while index3 < len(projectionData) and found <1:
#            print ("index3")
#            print (index3)
#            print ("found?")
#            print (found)
#            print ("projection Data")
#            print (projectionData)
#            print ("current projection line")
#            print (projectionData[index3])
#            print ("current projection xy")
#            projectionxy=(projectionData[index3][4], projectionData[index3][6])
#            print (projectionxy)
#            print ("current line xy")
#            linexy = (lineData[4], lineData[6])
#            print (linexy)
#            if linexy == projectionxy:
#                print ("Match!")
#            else:
#                print ("No match")           

            if lineData[4] == projectionData[index3][4] and lineData[6] == projectionData[index3][6]:   #checks if both x and y match
                print ("Found it the real way!")
                found += 1
                index3 += 1
            elif index3 < len(projectionData):    
                 print ("keep looking!")
                 index3 += 1 
            else: 
                print ("done looking - not there")
        if found <1:
            projectionData.append(lineData)                
            print ("not there - adding line")
        else:
            print ("not adding a line because it is a duplicate")
        print ("projectionData")
        print (projectionData)
        index2 += 1

   

    

