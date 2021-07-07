# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 12:16:17 2021

@author: Steven Backues
"""
import numpy as np
import pandas as pd


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

wallRadius = 125

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

bodyAreas = []
bodyPixels = []
bodyImages = []
recogLimit = 1
        
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
ArDim = 2*(wallRadius+1) # Dimension of the array will be just slightly larger than of the simulation, to make sure that no pixels are right on the edge (needed later)

for array in lineCollection:
    index2 = 0
    currentArea = 0
    currentPixels = []
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
        index3 = 0
        found = 0
        print ("length of projection data")
        print (len(projectionData))
        while index3 < len(projectionData) and found <1:
            if lineData[4] == projectionData[index3][4] and lineData[6] == projectionData[index3][6]:   #checks if both x and y match
                found += 1
                index3 += 1
            elif index3 < len(projectionData):    
                 index3 += 1 
        if found <1:
            projectionData.append(lineData)
            Pixels = [int(lineData[4]), int(lineData[6])]
            Shift = 1
            shiftedPixels = [x + Shift for x in Pixels]   #So that no pixels are right on the edge, later
            currentPixels.append(shiftedPixels)                  
            print ("not there - adding line")
        print ("projectionData")
        print (projectionData)
        print ("current Pixels")
        print (currentPixels)
        print ("current Body")
        print (currentBody)
        index2 += 1

    currentArea = len(projectionData)
    if(currentArea >= recogLimit):
        bodyAreas.append([currentBody, currentArea])
        #Now to make the imageArray for each body - a Numpy array the size of the simulation, with "1's" at every pixel location, and "0's" 
#everywhere there isn't a pixel'''
        imageArray = np.zeros ((ArDim, ArDim), dtype=int)
        for pix in currentPixels:
            imageArray[pix[0],pix[1]] = 1
            #To view the output
            #imageArraydf = pd.DataFrame(imageArray)
            #imageArraydf.to_csv('imageArray.csv')  
        bodyImages = bodyImages.append([imageArray])
        
        
    else:
        print ("below recognition limit - discarded")
    index1 += 1
    

  

