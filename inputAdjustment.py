# -*- coding: utf-8 -*-

#Test code foradjusting SphereGen input. Basically this code is meant to increase x, y, and/or z coordinate values for all
# spheres entered if certain spheres were detected to produce negative coordinate values in any way.

fileInput = "" #Name of input file.
fileOutput = "" #Name of output file.

def main():
    print("stuff")
    
    
    print("\n>>Enter INPUT file path and name:", end='')
    fileInput = input()
    
    #print("\n>>Enter OUTPUT file path and name:", end='')
    #fileOutput = input()
    
    #Read in all data from input file and store in Data
    Data = []
    
    inStream = open(fileInput, "r")
    #List of all lines from the given input file.
    inStreamLines = inStream.readlines()
    
    for line in inStreamLines:
        stuff = line.split()
        Data.append(stuff)
    inStream.close()
    
    print("Original Coordinates:")
    for x in Data:
        #print("Sphere Radius: " + x[0])
        print(x)
    
    maxChanges = [0, 0, 0]
    
    for y in Data:
        tempChange = diagnose(y)
        if(tempChange[0] > maxChanges[0]):
            maxChanges[0] = tempChange[0]
            
        if(tempChange[1] > maxChanges[1]):
            maxChanges[1] = tempChange[1]
        #The following were all [0] before.
        if(tempChange[2] > maxChanges[2]):
            maxChanges[2] = tempChange[2]
            
    FinalData = fix(Data, maxChanges)
    
    maxX = 0
    maxY = 0
    maxZ = 0
    
    print("\nModified Coordinates:")
    for stuff in FinalData:
        print(stuff)
        tempX = stuff[1] + stuff[0]
        tempY = stuff[2] + stuff[0]
        tempZ = stuff[3] + stuff[0]
        
        if(tempX > maxX):
            maxX = tempX
        
        if(tempY > maxY):
            maxY = tempY
    
        if(tempZ > maxZ):
            maxZ = tempZ
    
    print("\nThe Lattice will probably need to be at least %d x %d x %d in size (X x Y x Z)" %(maxX, maxY, maxZ))
        
    print("\nWould you like to scale down the coordinates [y/n]:")
    
    toScale = input()
    ScaledData = []
    if(toScale == "y"):
        print("\nBy what factor?")
        scaleFactor = int(input())
        
        ScaledData = scaleDown(FinalData, scaleFactor)
        
        print("\nScaled Coordinates")
        
        newMaxX = 0
        newMaxY = 0
        newMaxZ = 0
        for line in ScaledData:
            print(line)
            tempX2 = line[1] + line[0]
            tempY2 = line[2] + line[0]
            tempZ2 = line[3] + line[0]
        
            if(tempX2 > newMaxX):
                newMaxX = tempX2
        
            if(tempY2 > newMaxY):
                newMaxY = tempY2
    
            if(tempZ2 > newMaxZ):
                newMaxZ = tempZ2
            
        print("\nThe NEW Lattice will probably need to be at least %d x %d x %d in size (X x Y x Z)" %(newMaxX, newMaxY, newMaxZ))
    print("\n\nDONE!!!")

def diagnose(lineData):
    #print("Diagnose Check")
    
    #temp = [0, 0, 0]
    xChange = ((int(lineData[1]) - int(lineData[0])) * -1) + 5
    yChange = ((int(lineData[2]) - int(lineData[0])) * -1) + 5
    zChange = ((int(lineData[3]) - int(lineData[0])) * -1) + 5
    temp = [xChange, yChange, zChange]
    return(temp)


def fix(Spheres, Changes):
    #print("Fix Check")
    FinalData = []
    
    for sphere in Spheres:
        #These lines were all Changes[0] before
        tempX = int(sphere[1]) + Changes[0]
        tempY = int(sphere[2]) + Changes[1]
        tempZ = int(sphere[3]) + Changes[2]
        #tempLine = sphere[0] + " " + str(tempX) + " " + str(tempY) + " " + str(tempZ)
        #tempLine = sphere[0] + " " + tempX + " " + tempY + " " + tempZ
        tempLine = [int(sphere[0]), tempX, tempY, tempZ]
        FinalData.append(tempLine)
    return(FinalData)

def scaleDown(moreData, factor):
    
    newData = []
    index = 0
    for line in moreData:
        newRadius = int(line[0]/factor)
        newX = int(line[1]/factor)
        newY = int(line[2]/factor)
        newZ = int(line[3]/factor)
        newLine = [newRadius, newX, newY, newZ]
        newData.append(newLine)
        index += 1
    return(newData)

main()