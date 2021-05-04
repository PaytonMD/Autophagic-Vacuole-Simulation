# -*- coding: utf-8 -*-

############################################################################################################
#   Eastern Michigan University
#   Backues Lab  
#   Author: Payton Dunning
#   Last Date Modified: May 3rd, 2021
#
#   Utility script that is not used by default within the AVS pipeline. PIF files used by CompuCell 3D (CC3D)
#   can become quite large and take up an inconvieant amount of file space. This scripts condenses the number
#   of PIF coordinate lines needed to represent a CC3D model. PIF coordinates define two opposite corners of
#   a rectangular or square box to be plotted in CC3D. The SphereGen script generates PIF coordinates that model
#   single voxels (1 x 1 x 1 unit cubes) by default. Condenser can scan through a PIF file and condense sets of
#   single voxel PIF coordinates into 1 x 1 x Z lines, reducing the number of lines in the PIF file
#   and the overall file size.
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

#This script condenses PIF files into fewer lines, minimizing the file size.
def main():
    inputName = ""
    outputName = ""
    
    print(">>Enter input PIF file, including file path.")
    inputName = input()
    
    print(">>Use same file for output?[y/n]")
    userSelect = input()
    
    if(userSelect == "n" or userSelect == "N"):
        print(">>Enter new output PIF file.")
        outputName = input()
    else:
        outputName = inputName
    
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
    
    '''Scan through every line in the PIF file and group sets of voxels from the same cell body
        with the same x and y coordinates. This should group together lines of each body
        along the Z axis, converting the all voxel PIF coordinates into voxel + line PIF coordinates.'''
    for line in inStreamLines:
        
        #The first line of the file is singled out to set the inital min and max Z values.
        if(firstLine):
            # PIF coordinates are written as such: [Cell#] [CellType] [X-Low] [X-High] [Y-Low] [Y-High] [Z-Low] [Z-High]
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
            
            #If the current and next line have the same X and Y coordinates, begin grouping together PIF file lines.
            if((nextX == currentX) and (nextY == currentY)):
                currentBody = nextBody
                maxZ = nextZ
                
                #Used for when the last line in the file is reached.
                if(line == lastElement):
                    currentBody = nextBody
                    currentX = nextX
                    currentY = nextY
                    newLine = ("%s %s %s %s %s %s %s %s \n" % (currentBody, cellType, currentX, currentX, currentY, currentY, minZ, maxZ))
                    #Append the new model line to the coordinate array.
                    condensedCoords.append(newLine)
                    
            #When the end of the current model line is reached, detected by a changed X or Y coordinate value, append the current PIF
            # line to the coordinate array and set up the beginning of a new model line.
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
    
    #Once condensing of all input PIF file lines is complete, output the resulting coordinates to the output file.
    for line in condensedCoords:
        outStream.write(line)
    outStream.close()
    
    print("---Condensing Finished---")
#ENDOFMAIN