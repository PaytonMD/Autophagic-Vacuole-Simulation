# -*- coding: utf-8 -*-
import sys
import math
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
############################################################################################################
#   Eastern Michigan University
#   Backues Lab  
#   Author: Payton Dunning and Steven Backues
#   Last Date Modified: May 3rd, 2021
#
#   A script for analyzing the contents of an Autophagic Vacuole Simulation (AVS) project formatted 
#   Compucell 3D (CC3D) simulation. The script takes in a PIF file (.piff), that must contain "Body" and
#   "Wall" cells, and takes a slice through the simulation comparable to a TEM image of a cell. The bodies
#   within this slice are then analyzed to determine their relative areas. This area data is the recorded
#   and reported for later compilation and statistical analysis.
# This version has various variables hard-coded instead of being user-input, in order to speed the analysis 
# of multiple identical files.  
############################################################################################################
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################################################
def main(fileSelectOpt):
        #For a given run of SliceStats_M, all body measurment output lines to the output
    #file will have the same date and time stamp.
    initialTime = time.asctime(time.localtime(time.time()))
    
    print("Now running SliceStats.py with your hard-coded options")
    
    if(fileSelectOpt):
        print("Please Select file...")
        #inputName = r""
        Tk().withdraw()
        filename = askopenfilename()
        inputName = filename
        print("Given File Name: %s" %(filename))
    else: 
        print(">>Enter INPUT PIF file path+name:")
        inputName = input()
   


    outputName = "sliceData/sliceCoords.txt"
 


    scaleFactor = 4
    #wallD = modelParams[1]
    wallRadius = 125
    centerX = 125
    
    
    print("Current Model Parameters:\n")
    print("\tScale_Factor: %d\n" %(scaleFactor))
    print("\tWall_Radius: %d\n" %(wallRadius))
    print("\tWall_Diameter: %d\n" %(wallRadius*2))
    print("\tWall_X_Coordinate: %d\n" %(centerX))
    
    
    #The minimum vacuole diameter needed to perform the slice and analyze the body areas.
    #Used to define the usable range of coordinates a slice can be taken at.
    #Essentially used as a threshold within to take slices.
    #Unscalled default is a 300nm minimum radius (600nm minimum diameter).
    #Used to be called recognition limit, but that is meant to be used for minimum body size.
    unScalledVacMin = 300
    vacMin = (unScalledVacMin / scaleFactor)
    print("Default slice recognition limit = %dunits" %(vacMin))
    
   
    #Useable range of x-coordinates for the main slice.
    #diamRangeVar = int((wallD - minDiam) / 2)
    wallRecDiff = (wallRadius**2)-(vacMin**2)
    diamRangeVar = 0
    
    #(wallRadius**2)-(recogLimit**2) must be checked to be non-negative before attempted to find its square root.
    if(wallRecDiff > 0):
        diamRangeVar = math.sqrt(wallRecDiff)
        
    if(diamRangeVar <= 0):
        sys.exit("\n!!!This model does not support a vacuole slice threshold of %s" %(vacMin))
        
    #The starting and ending X-coordinates viable for a slice to be taken at.
    minX = centerX - diamRangeVar
    maxX = centerX + diamRangeVar
   
    # This is everything except the file input so that I can loop over it.  
            
    slices = [28, 78, 128, 178, 228]
    for SX in slices:    
        sliceCoord = SX
    
    
        #Stores all lines in input PIFF file that contain Wall data.
        wallText = []
        #Stores all lines in input PIFF file that contain Body data.
        bodyText = []
            
        #Keeps track of the entire volume of every body in the piff file, not just ones that make it into a slice.
        bodyWholeVol = []
        bodyTotalVolumeNums = []
            
        inStream = open(inputName, "r")
        #Fills wallText and bodyText with relevent data from the input file.
        for line in inStream:
            data = line.split()
    
            bodyID = int(data[0])
            
            idCheck = bodyID in bodyTotalVolumeNums
            
            if(len(bodyTotalVolumeNums) > 0 and (idCheck == True)):
                #print("check")
                index = bodyTotalVolumeNums.index(bodyID)
                bodyWholeVol[index] += 1
                
            else:
                bodyTotalVolumeNums.append(bodyID)
                bodyWholeVol.append(1)
                                    
                #print("check2")
    
            if(data[1] == "Wall"):
                wallText.append(line)
                
            if(data[1] == "Body"):
                bodyText.append(line)
                
        inStream.close()
        
   
        print("\n\n\t minX = %d || maxX = %d \n" %(minX, maxX))
            
        #Randomly select a x value within our minX~maxX range, that is the center point of our slice.
        '''The slice can then be (BLANK) units thick, with blank being the difference between the inputted diameter of the wall
                and the minimum diameter size. For sphereCoords xRange would be 5, so 2 higher and 2 lower than the chosen x Value.
                The funcitionality of the main slice being taken at a randomly selected X value within the valid range will '''
            
        '''A list of the bodies that make it into the slice. So if only bodies #1, #3, and #4 make it into the slice,
                bodyNum will have "1", "3", and "4", as elements. '''
        bodySliceNums = []
            
        '''A list that keeps a count of the number of points for each body that fall within the slice. So if bodies 1,3, and 4,
                make it into the slice, and #1 has 55 points within the slice, #3 has 70 points, and #4 has 102 points, 
                bodyVolCounts should be [55, 70, 102]. This effectively keeps track of the volumes of each body's slice.'''
        bodySliceVolCounts = []
            
        #A list of lists. Each sub-list contains all of the lines associated with a body.
        lineCollection = []
        index = 0
        
        print("\nPIFF coordinates of the slice will be written to sliceData\sliceCoords.txt")
        print("\nSlice measurment data will be written to sliceData\sliceDefault.txt")
        
        '''The lines within bodyText are parsed through and sorted into the list of lists, lineCollection.
            As the lines within the given piff file can be out of order, as in all the lines for the bodies and wall
            can be mixed around and in a non-linear order, all the lines for each body, that fall within
            the slice range, are collected into the sub-lists of listCollection. Each sub-list contains all the lines 
            associated with a single body that made it into the main slice. Just to be clear, this is where the MAIN slice occurs.'''
        outStream = open(outputName, "w")
            
        for bodyEntry in bodyText:
            bodyLine = bodyEntry.split()
            xValue = int(bodyLine[2])
            
            if(xValue <= (sliceCoord+2) and xValue >= (sliceCoord-2)):
                bodyID = bodyLine[0]
                
                try:
                    index = bodySliceNums.index(bodyID)
                    bodySliceVolCounts[index] += 1
                    #print(lineCollection)
                    
                except:
                    bodySliceNums.append(bodyID)
                    lineCollection.append([])
                    bodySliceVolCounts.append(1)
                    
                posi = bodySliceNums.index(bodyID)
                lineCollection[posi].append(bodyEntry)
                
        index1 = 0
        bodyAreas = []
        #The minimum recognition limit for the sub-slices of the bodies. This is based on a 50nm limit
        #for body radius givin by Dr.Backues. This translates to a minimum area of ~7854 (prescaling).
        #Area of circle = pi * r^2

        minBodyRadius = (50.0 / scaleFactor)
        recogLimit = math.pi * (minBodyRadius**2)
        print("Current minimum recognized body radius (scaled) = %d" %(minBodyRadius))
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
            print ("body array")
            print (array)
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
                #print ("lineData")
                #print (lineData)
                index3 = 0
                found = 0
                while index3 < len(projectionData) and found <1:
               
        
                    if lineData[4] == projectionData[index3][4] and lineData[6] == projectionData[index3][6]:   #checks if both x and y match
                        #print ("Found it the real way!")
                        found += 1
                        index3 += 1
                    elif index3 < len(projectionData):    
                         #print ("keep looking!")
                         index3 += 1 
                    else: 
                        print ("done looking - not there")
                if found <1:
                    projectionData.append(lineData)                
                    #print ("not there - adding line")
                else:
                    print ("not adding a line because it is a duplicate")
                #print ("projectionData")
                #print (projectionData)
                index2 += 1
            print("final projectionData")
            print (projectionData)
            currentArea = len(projectionData)
            if(currentArea >= recogLimit):
                bodyAreas.append([currentBody, currentArea])
            else:
                print ("below recognition limit - discarded")
            index1 += 1
        
        outStream2 = open("sliceData/sliceDefault.txt", "a+")
        
        print("[\"Body Number\", \"Max Area\"]:")
    
        # For easier data parsing I'll change body output to just the measured body area seperated by commas.
        #Each data set will be seperated by a dashed line.
        reScaledAreas = []
    
        
        #Check Initial Area Data and print:
        for result in bodyAreas:
            print("\nUnmodified Body Data:")
            stringPrintResult = "[%d, %d]" %(int(result[0]), result[1])
            print(stringPrintResult)
        
        if(scaleFactor!=1):
                #TO-DO: Merge the following two for loops, no point in having them seperate.
                for result in bodyAreas:
                    #stringPrintResult = "[%d, %d]" %(int(result[0]), result[1])
                    scaledResult = result[1] * scaleFactor
                    reScaledAreas.append([result[0], scaledResult])
                
                for result in reScaledAreas:
                    print("\nModified Body Data:")
                    stringPrintResult = "[%d, %d]" %(int(result[0]), result[1])
                    print(stringPrintResult)

                    
                    #date | time | bodyNum | area | perimeter | volume | model wall's radius
                    #Perimeter Will be added later.
                    tableEntry = "%s , %d , %d , %d \n" %(initialTime, sliceCoord, int(result[0]), result[1])
                    outStream2.write(tableEntry) # Outputs each area value in the result array seperated by commas.
        
        else:
            for result in bodyAreas:
                stringPrintResult = "[%d, %d]" %(result[0], result[1])
                print(stringPrintResult)
                outStream2.write("%d," %(result[1])) # Outputs each area value in the result array seperated by commas.
            
        outStream2.write("---")
        outStream2.close()
        print("\none slice is done.")

# Calls main to run the program
main(1)