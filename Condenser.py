

print("Hello!")

#Enter the input and output file paths+names below inside the quotations. 
inputName = r"G:\Shared drives\Backues Research Team\Notebooks\Backues\Testing programs\Spheregen testing\20200527\generated4.piff"
outputName = r"C:\Users\Temp\Desktop\gen4Condense.piff"

inStream = open(inputName, "r")
inStreamLines = inStream.readlines()
inStream.close()
condensedCoords = []

currentX = 0
currentY = 0
currentZ = 0
minZ = 0
maxZ = -1

firstLine = True
length = (len(inStreamLines))
lastElement = inStreamLines[length-1]

for line in inStreamLines:
    if(firstLine):
        data = line.split()
        cellType = data[1]
        currentBody = data[0]
        currentX = data[2]
        currentY = data[4]
        currentZ = data[6]
        minZ = currentZ
        maxZ = currentZ
        firstLine = False
    else:
        data = line.split()
        nextBody = data[0]
        nextX = data[2]
        nextY = data[4]
        nextZ = data[6]
        
        if((nextX == currentX) and (nextY == currentY)):
            currentBody = nextBody
            maxZ = nextZ
            
            #Used for when the last line in the file is reached.
            if(line == lastElement):
                currentBody = nextBody
                currentX = nextX
                currentY = nextY
                newLine = ("%s %s %s %s %s %s %s %s \n" % (currentBody, cellType, currentX, currentX, currentY, currentY, minZ, maxZ))
                condensedCoords.append(newLine)
        else:
            
            newLine = ("%s %s %s %s %s %s %s %s \n" % (currentBody, cellType, currentX, currentX, currentY, currentY, minZ, maxZ))
            condensedCoords.append(newLine)
            currentBody = nextBody
            currentX = nextX
            currentY = nextY
            minZ = nextZ
            maxZ = nextZ
            cellType = data[1]
            #outStream.write("%d Body %d %d %d %d %d %d \n" % (currentBody, currentX, currentX, currentY, currentY, minZ, maxZ))
            
outStream = open(outputName, "w")

for line in condensedCoords:
    outStream.write(line)
outStream.close()