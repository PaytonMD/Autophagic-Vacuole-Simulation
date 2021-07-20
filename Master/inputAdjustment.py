# -*- coding: utf-8 -*-
from tkinter import Tk
from tkinter.filedialog import askopenfilename

############################################################################################################
#   Author: Payton Dunning
#   Last Date Modified: July 20th, 2021
#
#   Complimentary code for SphereGen.py. Takes in spherical data and makes 2 types of adjustments in order
#   for the data to be compatible with SphereGen.py, CompuCell 3D, and other AVS project programs.
#   First, the script shifts all spheres equally along any or all of the XYZ planes in order to produce spheres that only
#   reside in quadrant 1. This is done because CompuCell 3D uses a lattice of purely positive integers (0 to whatever limit the 
#   lattice is set to). CompuCell 3D's default conditions are not compliant with negative coordinates.
#
#   The second adjustment is an optional scaling of the spherical data. If the data is deemed too large the user can specify some
#   scale to shrink the spheres down by. For instance, a given scale down of 2 would divide all of the radii and sphere center
#   coordinates by 2. Other adjustments to the data may be added in time.
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
fileInput = "" #Name of input file.
fileOutput = "sphereData.txt" #Name of output file.

#paramsFile is used to keep track of several variables used by multiple scipts.
paramsFile = "attributes/Model_Parameters.txt"

def main(fileSelectOpt, massRunCheck, massRunData, scaleFactor):
    print("Now running Master\inputAdjustment.py")
    ogData = [] #og as in original
    
    '''A new input format for text files was configured by Dr. Backues. During mass runs only
        the new format will be used, but otherwise users will select between using the old format
        or the new format. Eventually the old format option will be removed entirely.'''
    newInputFormat = True
    
    if(massRunCheck == True):
        print("MASSRUN")
        for line in massRunData:
            ogDataEntry = [line[4], line[5], line[6], line[7]]
            ogData.append(ogDataEntry)
    else:    
        print(">>Would you like to use the OLD input format?[y/n] (Select n if unsure).")
        formatCheck = input()
        
        if(formatCheck == 'y' or formatCheck == 'Y'):
            newInputFormat = False
        
        fileInput = ""
        if(fileSelectOpt == True):
            print(">>Select the sphere data file you'd like to use:")
            print("(The file selection screen may appear BEHIND your current application)")
            Tk().withdraw()
            fileInput = askopenfilename()
        else:
            print("\n>>Enter INPUT file path and name:", end='')
            fileInput = input()
        
        print("\n---All output will be written to 'sphereData.txt'---")
        
        #Read in all data from input file and store in ogData
        
        
        inStream = open(fileInput, "r")
        #List of all lines from the given input file.
        inStreamLines = inStream.readlines()
        
        if(newInputFormat):
            for line in inStreamLines:
                ogDataEntry = [line[4], line[5], line[6], line[7]]
                ogData.append(ogDataEntry)
        
        else:
            #Grabs sphere data from input file and stores in ogData.
            for line in inStreamLines:
                ogSphere = line.split()
                ogData.append(ogSphere)
                
        inStream.close()
    
    print("Original Coordinates:")
    print("(Coordinates here are the sphere's radius, X-center, Y-center, and Z-center.)")
    for sphere in ogData:
        print(sphere)
    
    #An array of the x, y, and z coordinate shifts needed to be made to the scaled spheres.
    maxChanges = [0, 0, 0]
    scaledData = []
    #If -1 is passed into inputAdjustment for scaleFactor, then ask user what factor they'd like to use.
    #If the scaleFactor passed in was not -1, use that scaleFactor for scaling
    if(scaleFactor == -1):
        print("\n>>>Would you like to scale down the coordinates [y/n]:")
        
        toScale = input()
        scaledData = ogData
        
        if(toScale == "y" or toScale =="Y"):
            print("\n>>>Enter Scaling Factor:")
            #scaleFactor here being an integer that will be used to divide the values of all the spheres.
            #A scaleFactor of 2 would cut the size of the spheres, and model, in half.
            scaleFactor = int(input())            
            scaledData = scaleDown(ogData, scaleFactor)
        else:
            scaleFactor = 1 #No scale factor was used.
    else:
        scaledData = scaleDown(ogData, scaleFactor)
    print("\nScaled Coordinates:")
    
    for sphere in scaledData:
        print(sphere)
        #The diagnose function determines how much the sphere data should be shifted based on an individual sphere's position and size.
        potentialChanges = diagnose(sphere)
        
        if(potentialChanges[0] > maxChanges[0]):
            maxChanges[0] = potentialChanges[0]
            
        if(potentialChanges[1] > maxChanges[1]):
            maxChanges[1] = potentialChanges[1]

        if(potentialChanges[2] > maxChanges[2]):
            maxChanges[2] = potentialChanges[2]
    
    #The shift function shifts the sphere data as needed so that all spheres remain in the all positive coordinate quadrant 1.
    shiftedData = shift(scaledData, maxChanges)
    
    #The largest predicated x, y, and z values among the sphere data. Used to predict the minimum size a CC3D simulation lattice
    #needs to be in order to fit this spherical data.
    maxX = 0
    maxY = 0
    maxZ = 0
    
    print("\nFinal Coordinates:")
    outStream = open(fileOutput, "w")
    
    #Prints the newly modified sphere data and determines actual values for maxX, maxY, and maxZ.
    for sphere in shiftedData:
        print(sphere)
        outLine = str(sphere[0]) + " " + str(sphere[1]) + " " + str(sphere[2]) + " " + str(sphere[3]) + "\n"
        outStream.write(outLine)
        
        #The temp values use the sphere's radius, sphere[0].
        tempX = sphere[1] + sphere[0]
        tempY = sphere[2] + sphere[0]
        tempZ = sphere[3] + sphere[0]
        
        if(tempX > maxX):
            maxX = tempX
        
        if(tempY > maxY):
            maxY = tempY
    
        if(tempZ > maxZ):
            maxZ = tempZ      
        
    print("\nThe Lattice will need to be at least %d x %d x %d (X x Y x Z) in size." %(maxX, maxY, maxZ))
    wallRadius = int(shiftedData[0][0])
    wallXCoord = int(shiftedData[0][1])
    print("Final Wall radius = %d" %(wallRadius))
    print("Final Wall central X-coordinate = %d" %(wallXCoord))
        
        
    outStream.close()
    print("\n\n---inputAdjustment is DONE.---")
    
    #Model Parameters Update:
    updateParams(scaleFactor, wallRadius, wallXCoord)

###END OF main###

#For a given line of sphere data passed into diagnose, function determines the coordinate shifts needed for the sphere in order
#to produce the sphere entirely in the 1st quandrant (no negative coordinates in any dimension).
def diagnose(lineData):
    xChange = ((int(float(lineData[1])) - int(float(lineData[0]))) * -1) + 5
    yChange = ((int(float(lineData[2])) - int(float(lineData[0]))) * -1) + 5
    zChange = ((int(float(lineData[3])) - int(float(lineData[0]))) * -1) + 5
    changes = [xChange, yChange, zChange]
    return(changes)
###END OF diagnose###

#Shifts all spheres in the data set by the independently determined X, Y and Z values determined in diagnose.
def shift(Spheres, Changes):
    #print("Fix Check")
    FinalData = []
    
    for sphere in Spheres:
        tempX = int(float(sphere[1])) + Changes[0]
        tempY = int(float(sphere[2])) + Changes[1]
        tempZ = int(float(sphere[3])) + Changes[2]

        tempLine = [int(float(sphere[0])), tempX, tempY, tempZ]
        FinalData.append(tempLine)
    return(FinalData)
###END OF shift###

#Scales down all spheres in the data set by the given user factor. The factor is always an integer value.
def scaleDown(moreData, factor):
    newData = []

    for line in moreData:
        #print("moreData line: %s" %(line))
        newRadius = (int(float(line[0]))) / factor
        newX = int(float(line[1])) / factor
        newY = int(float(line[2])) / factor
        newZ = int(float(line[3])) / factor
        
        newLine = [newRadius, newX, newY, newZ]
        newData.append(newLine)

    return(newData)
###END OF scaleDown###

def updateParams(factor, wallRadius, wallX):
    print("\nUpdating AVS Model Parameters...\n")
    paramsStream = open(paramsFile, "w")
    paramsStream.write("Scale_Factor: %d\n" %(factor))
    paramsStream.write("Wall_Radius: %d\n" %(wallRadius))
    paramsStream.write("Wall_X_Coordinate: %d\n" %(wallX))
    
    paramsStream.close()