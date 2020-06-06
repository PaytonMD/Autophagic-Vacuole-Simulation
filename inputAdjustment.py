# -*- coding: utf-8 -*-
#   Author: Payton Dunning
#   Last Date Modified: June 5th, 2020
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

fileInput = "" #Name of input file.
#fileOutput = "" #Name of output file.
#Script does not currently output to any file, though this will be added in a future version.

def main():    
    
    print("\n>>Enter INPUT file path and name:", end='')
    fileInput = input()
    
    #print("\n>>Enter OUTPUT file path and name:", end='')
    #fileOutput = input()
    
    #Read in all data from input file and store in Data
    ogData = [] #og as in original
    
    inStream = open(fileInput, "r")
    #List of all lines from the given input file.
    inStreamLines = inStream.readlines()
    
    #Grabs sphere data from input file and stores in ogData.
    for line in inStreamLines:
        ogSphere = line.split()
        ogData.append(ogSphere)
    inStream.close()
    
    print("Original Coordinates:")
    for sphere in ogData:
        print(sphere)
    
    #An array of the x,y, and z coordinate shifts needed to be made to the ogData spheres.
    maxChanges = [0, 0, 0]
    
    for y in ogData:
        potentialChanges = diagnose(y)
        if(potentialChanges[0] > maxChanges[0]):
            maxChanges[0] = potentialChanges[0]
            
        if(potentialChanges[1] > maxChanges[1]):
            maxChanges[1] = potentialChanges[1]

        if(potentialChanges[2] > maxChanges[2]):
            maxChanges[2] = potentialChanges[2]
            
    shiftedData = shift(ogData, maxChanges)
    
    #The largest predicated x, y, and z values among the sphere data. Used to predict the minimum size a CC3D simulation lattice
    #needs to be in order to fit this spherical data.
    maxX = 0
    maxY = 0
    maxZ = 0
    
    print("\nModified Coordinates:")
    #Prints the newly modified sphere data and determines actual values for maxX, maxY, and maxZ.
    for sphere in shiftedData:
        print(sphere)
        tempX = sphere[1] + sphere[0]
        tempY = sphere[2] + sphere[0]
        tempZ = sphere[3] + sphere[0]
        
        if(tempX > maxX):
            maxX = tempX
        
        if(tempY > maxY):
            maxY = tempY
    
        if(tempZ > maxZ):
            maxZ = tempZ
    
    print("\nThe Lattice will likely need to be at least %d x %d x %d (X x Y x Z) in size." %(maxX, maxY, maxZ))
        
    print("\nWould you like to scale down the coordinates [y/n]:")
    
    toScale = input()
    scaledData = []
    
    if(toScale == "y" or toScale =="Y"):
        print("\nBy what factor?")
        scaleFactor = int(input())
        
        scaledData = scaleDown(shiftedData, scaleFactor)
        
        print("\nScaled Coordinates")
        
        newMaxX = 0
        newMaxY = 0
        newMaxZ = 0
        #Redetermines the maximum dimensions of the future CC3D lattice based on the largest XYZ values found among the spheres.
        for sphere in scaledData:
            print(sphere)
            tempX = sphere[1] + sphere[0]
            tempY = sphere[2] + sphere[0]
            tempZ = sphere[3] + sphere[0]
        
            if(tempX > newMaxX):
                newMaxX = tempX
        
            if(tempY > newMaxY):
                newMaxY = tempY
    
            if(tempZ > newMaxZ):
                newMaxZ = tempZ
            
        print("\nThe NEW Lattice will likely need to be at least %d x %d x %d (X x Y x Z) in size." %(newMaxX, newMaxY, newMaxZ))
    print("\n\nDONE!!!")
###END OF main###

#For a given line of sphere data passed into diagnose, function determines the coordinate shifts needed for the sphere in order
#to produce the sphere entirely in the 1st quandrant (no negative coordinates in any dimension).
def diagnose(lineData):
    xChange = ((int(lineData[1]) - int(lineData[0])) * -1) + 5
    yChange = ((int(lineData[2]) - int(lineData[0])) * -1) + 5
    zChange = ((int(lineData[3]) - int(lineData[0])) * -1) + 5
    changes = [xChange, yChange, zChange]
    return(changes)
###END OF diagnose###

#Shifts all spheres in the data set by the independently determined X, Y and Z values determined in diagnose.
def shift(Spheres, Changes):
    #print("Fix Check")
    FinalData = []
    
    for sphere in Spheres:
        tempX = int(sphere[1]) + Changes[0]
        tempY = int(sphere[2]) + Changes[1]
        tempZ = int(sphere[3]) + Changes[2]

        tempLine = [int(sphere[0]), tempX, tempY, tempZ]
        FinalData.append(tempLine)
    return(FinalData)
###END OF shift###

#Scales down all spheres in the data set by the given user factor. The factor is always an integer value.
def scaleDown(moreData, factor):
    newData = []

    for line in moreData:
        newRadius = int(line[0]/factor)
        newX = int(line[1]/factor)
        newY = int(line[2]/factor)
        newZ = int(line[3]/factor)
        
        newLine = [newRadius, newX, newY, newZ]
        newData.append(newLine)

    return(newData)
###END OF scaleDown###
main()