# -*- coding: utf-8 -*-
import sys
import random
import math
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
############################################################################################################
#   Eastern Michigan University
#   Backues Lab  
#   Author: Payton Dunning
#   Last Date Modified: June10th, 2021
#
#   A script for analyzing the contents of an Autophagic Vacuole Simulation (AVS) project formatted 
#   Compucell 3D (CC3D) simulation. The script takes in a PIF file (.piff), that must contain "Body" and
#   "Wall" cells, and takes a slice through the simulation comparable to a TEM image of a cell. The bodies
#   within this slice are then analyzed to determine their relative areas. This area data is the recorded
#   and reported for later compilation and statistical analysis.
############################################################################################################
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################################################

#paramsFile is used to keep track of several variables used by multiple scipts.
paramsFile = "attributes/Model_Parameters.txt"

#cycleRun is a boolean variable. It is false when SliceStats is run alone, and true when run as part of the AVS cycle.
def main(fileSelectOpt):
    
    #For a given run of SliceStats_M, all body measurment output lines to the output
    #file will have the same date and time stamp.
    initialTime = time.asctime(time.localtime(time.time()))
    
    print("Now running Master\SliceStats_M.py")
    outputName = ""
    inputName = ""
    
    if(fileSelectOpt):
        print("Please Select file...")
        print("(The file selection screen may appear BEHIND your current application)")
        Tk().withdraw()
        filename = askopenfilename()
        inputName = filename
        print("Given File Name: %s" %(filename))
    else: 
        print(">>Enter INPUT PIF file path+name:")
        inputName = input()

    #The master version of SliceStats will just use this predefined output file for easier use of this script.
    outputName = "sliceData/sliceCoords.txt"
    
    print("Grabbing AVS Model Parameters...\n")
    modelParams = grabParams()
    scaleFactor = modelParams[0]
    #wallD = modelParams[1]
    wallRadius = modelParams[1]
    centerX = modelParams[2]
    
    
    print("Current Model Parameters:\n")
    print("\tScale_Factor: %d\n" %(scaleFactor))
    print("\tWall_Radius: %d\n" %(wallRadius))
    print("\tWall_Diameter: %d\n" %(wallRadius*2))
    print("\tWall_X_Coordinate: %d\n" %(centerX))
    
    print(">>Would you like to use these parameters?[y/n]")
    paramSelect = input()
    
    if(paramSelect == "n"):
        print(">>Please enter new values for parameters:\n")
        print("(The Wall radius parameter value should be a post-scaling value)")
        
        print("\n>>Enter new scaling factor: ")
        scaleFactor = int(input())
        
        #The known Diameter of the simulation's Wall sphere.
        print("\n>>Enter the given wall's radius", end='')
        wallRadius = int(input())
        
        #The X value representing the X-coordinate of the Wall sphere's center.
        print("\n>>Enter the given wall's central x-coordinate:", end='')
        centerX = int(input()) 
    
    wallD = (wallRadius*2)
    
    #The minimum vacuole radius needed to perform the slice and analyze the body areas.
    #Used to define the usable range of coordinates a slice can be taken at.
    #Essentially used as a threshold within to take slices.
    #Unscalled default is a 300nm minimum radius (600nm minimum diameter).
    #Used to be called recognition limit, but that is meant to be used for minimum body size.
    unScalledVacMin = 300.0
    vacMin = (unScalledVacMin / scaleFactor)
    print("Default slice recognition limit (radius) = %dunits" %(vacMin))
    
    print(">>Would you like to use this default minimum vacuole slice threshold?[y/n]")
    minDInput = input()
    
    if(minDInput == "n" or minDInput == "N"):
        print("\n>>Enter new minimum vacuole threshold (scaled): ")
        vacMin = int(input())
    
    #Useable range of x-coordinates for the main slice.
    #diamRangeVar = int((wallD - minDiam) / 2)
    wallRecDiff = (wallRadius**2)-(vacMin**2)
    diamRangeVar = 0
    
    #(wallRadius**2)-(vacMin**2) must be checked to be non-negative before attempted to find its square root.
    if(wallRecDiff > 0):
        diamRangeVar = math.sqrt(wallRecDiff)
        
    if(diamRangeVar <= 0):
        sys.exit("\n!!!This model does not support a vacuole slice threshold of %s" %(vacMin))
        
    #The starting and ending X-coordinates viable for a slice to be taken at.
    minX = centerX - diamRangeVar
    maxX = centerX + diamRangeVar
    
    
    print(">>Finally, select an option for determining where a slice will be taken:")
    print("\t[0 for slice to be taken at centerX coordinate]")
    print("\t[1 for slice to be taken at a randomly selected coordinate]")
    print("\t[2 for slice to be taken at a user specified coordinate]")
        
    sliceChoice = int(input())
    sliceCoord = 0
    
    if(sliceChoice == 0):
        sliceCoord = centerX
        
    elif(sliceChoice == 1):
        sliceCoord = random.randint(minX, maxX)
        
    elif(sliceChoice == 2):
        print("\n>>Enter the x coordinate you'd like the slice to be taken at:")
        sliceCoord = int(input())
    else:
        sys.ext("\nInput was found to be invalid. Please enter in 0, 1, or 2 for your choice of slice selection method.")
    
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
    
    print("\nPIFF coordinates of the slice will be written to Master\sliceData\sliceCoords.txt")
    print("\nSlice measurment data will be written to Master\sliceData\sliceDefault.txt")
    
    # Changes the thickness of the slice depending on the scale.  The unscaled thickness of the slice should be 70nm,  typical thickness for a TEM section
    sliceThickness = 70 / scaleFactor
    HalfSliceThickness = round((sliceThickness - 1)/2)
    '''The lines within bodyText are parsed through and sorted into the list of lists, lineCollection.
        As the lines within the given piff file can be out of order, as in all the lines for the bodies and wall
        can be mixed around and in a non-linear order, all the lines for each body, that fall within
        the slice range, are collected into the sub-lists of listCollection. Each sub-list contains all the lines 
        associated with a single body that made it into the main slice. Just to be clear, this is where the MAIN slice occurs.'''
    outStream = open(outputName, "w")
        
    for bodyEntry in bodyText:
        bodyLine = bodyEntry.split()
        xValue = int(bodyLine[2])
        
        if(xValue <= (sliceCoord+HalfSliceThickness) and xValue >= (sliceCoord-HalfSliceThickness)):
            bodyID = int(bodyLine[0])
            
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
    
    #The lines that made it into lineCollection are recordered to the primary output file.
    for array in lineCollection:
        index2 = 0
        for line in lineCollection[index1]:
            #print(lineCollection[index1][index2])
            outStream.write(lineCollection[index1][index2])
            index2 += 1
        index1 += 1
    outStream.close()
    
    '''The following loops iterate through the main slice, contained in lineCollection. Each body, contained in
        each sub-list, is individually analyzed to determine the largest single unit thick sub-slice for that body.
        As the main slice may be several units thick, some bodies may contain several of these sub-slices. The
        largest sub-slice for each body, that meet the minimum area threshold, are recorded and outputted. Each body's
        max area slice may be from different X-coordinate slices. All of these sub-slices will still fall within the
        previously determined range of valid x-value ranges.'''
    
    #An array of arrays. Each sub array contains 2 things: "Body Num", "Max Area" for that body.
    bodyAreas = []
    #The minimum recognition limit for the sub-slices of the bodies. This is based on a 50nm limit
    #for body radius givin by Dr.Backues. This translates to a minimum area of ~7854 (prescaling).
    #Area of circle = pi * r^2

    minBodyRadius = (50.0 / scaleFactor)
    print("Current minimum recognized body radius (scaled) = %d" %(minBodyRadius))
    print(">>Would you like to use this default body recognition limit? [y/n]")
    bodyCheck = input()
    
    if(bodyCheck == "n" or bodyCheck == "N"):
        print(">>Please enter a new minimum recognized body radius with scaling factored in: ")
        minBodyRadius = int(input())
    recogLimit = math.pi * (minBodyRadius**2)
           
    index1 = 0
    #The outer for loop iterates through each body.
    for array in lineCollection:
        maxArea = -1
        index2 = 0
        currentArea = 0
        lineData = lineCollection[index1][index2].split()
        currentBody = int(lineData[0])
        currentX = lineData[2]
        
        #This inner loop iterates through the lines for the current body.
        for line in lineCollection[index1]:
            lineData = lineCollection[index1][index2].split()
            nextBody = int(lineData[0])
            nextX = lineData[2]
            index2 += 1

            if( (currentBody == nextBody) and (currentX == nextX)):
                currentArea += 1
                
                '''At the end of a sub-slice, determined by reaching a new set of lines with
                a different x-value, check if the current slice should count as the largest
                slice (maxArea) of the current body.'''
            elif( (currentBody == nextBody) and (currentX != nextX)):
                if(currentArea > maxArea):
                    #print("New X Check")
                    maxArea = currentArea
                    currentArea = 1
                    currentX = nextX
                    
            '''End of the sublist has been reached. Check if any of the slices for the
            current body meet the minimum area requirement. If so, record the body and it's area.'''
            if(index2 >= (len(lineCollection[index1]))):
                #print("End of Body Check")
                if(currentArea > maxArea):
                    maxArea = currentArea

                if(maxArea >= recogLimit):
                    bodyAreas.append([currentBody, maxArea])
        index1 += 1
    
    outStream2 = open("sliceData/sliceDefault.txt", "a+")
    
    print("[\"Body Number\", \"Max Area\"]:")
    
    #Check Initial Area Data and print:
    for result in bodyAreas:
        print("\nUNmodified Body Data:")
        stringPrintResult = "[%d, %d]" %(result[0], result[1])
        print(stringPrintResult)
    
    if(scaleFactor!=1):
        #TO-DO: Merge the following two for loops, no point in having them seperate.
        for result in bodyAreas:
            scaledResult = result[1] * scaleFactor
            stringPrintResult = "[%d, %d]" %(result[0], scaledResult)
            
            print("\nModified Body Data:")
            print(stringPrintResult)
            
            volIndex = bodyTotalVolumeNums.index(result[0])
            currentVolume = bodyWholeVol[volIndex]
            
            #date&time , bodyNum , area , perimeter , volume , model wall's radius
            #Perimeter Will be added later.
            tableEntry = "%s , %d , %d , %d , %d \n" %(initialTime, result[0], scaledResult, currentVolume, wallRadius)
            outStream2.write(tableEntry) # Outputs each area value in the result array seperated by commas.

    else:
        for result in bodyAreas:
            stringPrintResult = "[%d, %d]" %(result[0], result[1])
            print(stringPrintResult)
            outStream2.write("%d," %(result[1])) # Outputs each area value in the result array seperated by commas.
        
    outStream2.write("---")
    outStream2.close()
    print("\n\nSliceStats_M is DONE.")
#Calls the function main to initate program.

def grabParams():
    params = []
    paramsInStream = open(paramsFile, "r")
    inStreamLines = paramsInStream.readlines()
    paramsInStream.close()
    
    for line in inStreamLines:
        splitLine = line.split()
        params.append(int(splitLine[1].strip()))
        
    return params
#This will automatically run this file if imported:
#main()