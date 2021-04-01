# -*- coding: utf-8 -*-
#   Author: Payton Dunning
#   Last Date Modified: March 31st, 2021
#
#   Complimentary code for SphereGen.py. Takes in spherical data and makes 2 types of adjustments in order
#   for the data to be compatible with SphereGen.py, CompuCell 3D, and other AVS project programs.
#   First, the script shifts all spheres equally along any or all of the XYZ planes in order to produce spheres that only
#   reside in quadrant 1. This is done because CompuCell 3D uses a lattice of purely positive integers (0 to whatever limit the 
#   lattice is set to). CompuCell 3D's default conditions are not compliant with negative coordinates.
#
#   The second adjustment is an optional scaling of the spherical data. If the data is deemed too large the user can specify some
#   scale to shrink the spheres down by. For instance, a given scale down of 2 would divide all of the diameters and sphere center
#   coordinates by 2. Other adjustments to the data may be added in time.

fileInput = "" #Name of input file.
fileOutput = "sphereData.txt" #Name of output file.

#paramsFile is used to keep track of several variables used throughout the pipeline.
paramsFile = "attributes/Model_Parameters.txt"

def main():    
    print("Now running Master\inputAdjustment.py")
    
    print("\n>>Enter INPUT file path and name:", end='')
    fileInput = input()
    
    print("\nAll output will be written to 'sphereData.txt'")
    
    #Read in all data from input file and store in ogData
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
    
    #An array of the x, y, and z coordinate shifts needed to be made to the scaled spheres.
    maxChanges = [0, 0, 0]
    
    print("\nWould you like to scale down the coordinates [y/n]:")
    
    toScale = input()
    scaledData = ogData
    
    if(toScale == "y" or toScale =="Y"):
        print("\nBy what factor?")
        #scaleFactor here being an integer that will be used to divide the values of all the spheres.
        #A scaleFactor of 2 would cut the size of the spheres, and model, in half.
        scaleFactor = int(input())
        lastScaleFactor = scaleFactor
        
        scaledData = scaleDown(ogData, scaleFactor)
    else:
        lastScaleFactor = 1 #No scale factor was used.
    for sphere in scaledData:
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
    
    print("\nModified Coordinates:")
    #Prints the newly modified sphere data and determines actual values for maxX, maxY, and maxZ.
    for sphere in shiftedData:
        print(sphere)
        #The temp values use the sphere's radius, so the diameter, sphere[0] must be halved.
        tempX = sphere[1] + (sphere[0] / 2)
        tempY = sphere[2] + (sphere[0] / 2)
        tempZ = sphere[3] + (sphere[0] / 2)
        
        if(tempX > maxX):
            maxX = tempX
        
        if(tempY > maxY):
            maxY = tempY
    
        if(tempZ > maxZ):
            maxZ = tempZ
        
            
    print("\nFinal Coordinate data:")

    #Output to default file for now:
    outStream = open(fileOutput, "w")
    for sphere in shiftedData:
        print(sphere)
        outLine = str(sphere[0]) + " " + str(sphere[1]) + " " + str(sphere[2]) + " " + str(sphere[3]) + "\n"
        outStream.write(outLine)
        
    print("\nThe Lattice will likely need to be at least %d x %d x %d (X x Y x Z) in size." %(maxX, maxY, maxZ))
    wallDiameter = int(shiftedData[0][0])
    wallXCoord = int(shiftedData[0][1])
    print("Final Wall diameter = %d" %(wallDiameter))
    print("Final Wall central X-coordinate = %d" %(wallXCoord))
        
        
    outStream.close()
    print("\n\ninputAdjustment is DONE.")
    
    #Model Parameters Update:
    updateParams(scaleFactor, wallDiameter, wallXCoord)

###END OF main###

#For a given line of sphere data passed into diagnose, function determines the coordinate shifts needed for the sphere in order
#to produce the sphere entirely in the 1st quandrant (no negative coordinates in any dimension).
def diagnose(lineData):
    xChange = ((int(float(lineData[1])) - (int(float(lineData[0]))) / 2) * -1) + 5
    yChange = ((int(float(lineData[2])) - (int(float(lineData[0]))) / 2) * -1) + 5
    zChange = ((int(float(lineData[3])) - (int(float(lineData[0]))) / 2) * -1) + 5
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
        newDiameter = (int(float(line[0]))) / factor
        newX = int(float(line[1])) / factor
        newY = int(float(line[2])) / factor
        newZ = int(float(line[3])) / factor
        
        newLine = [newDiameter, newX, newY, newZ]
        newData.append(newLine)

    return(newData)
###END OF scaleDown###

def updateParams(factor, wallDiam, wallX):
    print("\nUpdating AVS Model Parameters...\n")
    paramsStream = open(paramsFile, "w")
    paramsStream.write("Scale_Factor: %d\n" %(factor))
    paramsStream.write("Wall_Diameter: %d\n" %(wallDiam))
    paramsStream.write("Wall_X_Coordinate: %d\n" %(wallX))
    
    paramsStream.close()
    
#This will automatically run this file if imported:
#main()