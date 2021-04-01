# -*- coding: utf-8 -*-
import math
import numpy as np
from copy import deepcopy

############################################################################################################
#   Eastern Michigan University
#   Backues Lab  
#   Author: Payton Dunning
#   Last Date Modified: March 31st, 2021
#
#   Reads in numerical data representing spheres and outputs a CC3D compatible PIF file representing the
#   various spheres. Sphere data is read in as lines from either a text file or typped into the console.
#   Each line of input represents one sphere and consists of the radii of that sphere and the x, y and z
#   coordinates of its center point. These spheres are meant to represent autophagic bodies within the
#   vacuole of a cell undergoing the cellular process of autophagy. The wall of the vacuole itself
#   can also be modeled here along with the autophagic bodies as a hollow sphere.
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
fileOutput = "" #Name of output file.

'''Takes in console input to determine method of sphere data input (file vs console).
    alone is a boolean variable that is False when selecting the inputAdjustment + SphereGen
    option in the master AVS script.'''
def main(alone):
    print("Now running Master\SphereGen_M.py")
    
    #Connects the following fileOutput to the global fileOutput variable.
    global fileOutput
    
    print("\n>>Enter OUTPUT PIF file path and name:", end='')
    fileOutput = input()
    
    if(not alone):
        useFile(alone)
    else:
        #Asks if input will be from console or from file:
        print ("\n>>Input method selection: \n\t[0 for file input]\n\t[1 for console input]", end='')
        inputType = int(input())     
        
        #Takes in file as input. Can be used for multiple spheres.
        if(inputType == 0):
            useFile(alone)
        #Takes in manual input from console. Spheres are read in line by line.
        elif(inputType == 1):
            useConsole()
   
###END OF main FUNCTION###
        
'''Handles reading sphere data from text file and converts it to CC3D PIFF coordinates.'''
def useFile(alone):
    #If the inputAdjustment + SphereGen_M option was selected in Master (alone == False),
    #use the default input file sphereData.
    if(not alone):
        fileInput = "sphereData.txt"
    else:
        print("\n>>Enter INPUT file path and name:", end='')
        fileInput = input()
    
    inStream = open(fileInput, "r")
    #List of all lines from the given input file.
    inStreamLines = inStream.readlines()
    
    print("\n>Build an encapsulating membrane wall? [y/n]")
    wallCheck = False
    if(input() == 'y'):
        wallCheck = True
    
    #wallData will be used if a wall is built. Stores the first line from input file while other bodies are being built.
    wallData = "x"
        
    #Keeps track of what cell body the current coordinates are being written for.
    bodyNum = 1
    
    for line in inStreamLines:
        #Option for creating wall out of first line of file.
        if(wallCheck == True):
            #Stores the first line from input file as the Wall sphere data.
            wallData = line
            wallCheck = False
            
        else:
            sphereData = line.split()
            print("Body #%d: %s %s %s %s" %(bodyNum, sphereData[0], sphereData[1], sphereData[2], sphereData[3]))
            #tVolume = float(sphereData[0]) #Target Volume
            dim = int(sphereData[0]) + 1 # The +1 might not be necessary. Other diameter variables may not have the +1.
            radii = (int(sphereData[0]) / 2)
            centerPoint = [float(sphereData[1]), float(sphereData[2]), float(sphereData[3])]
            
            #numpy arrays are a specialized array type.
            starterGrid = np.zeros((dim, dim, dim)) # Builds the 3D numpy array.
            sphereGrid = deepcopy(starterGrid) #Copy of the starterGrid.
            
            
            sphereGrid = setUpGrid(sphereGrid, radii) #Fills the grid with 1 to make a "sphere" of given radius.
            sphereToPif(sphereGrid, centerPoint, radii, bodyNum) #Writes out all 1s in the grid as a PIFF coordinate.
            #print(sphereGrid)
            bodyNum += 1
    
    #Begins the vacuole wall creation as a semi-hollowed out sphere.
    if(wallData!="x"):
        buildWall(wallData, bodyNum)
        
    inStream.close()
    print("\n\nDONE")
###END OF fileSphere FUNCTION###
    
'''Handles reading sphere data from console and converts it to CC3D PIFF coordinates.'''
def useConsole():
    print("Would you like a membrane wall built around bodies? [y/n]")
    wallCheck = False
    if(input() == 'y'):
        wallCheck = True
            
    #wallData will be used if a wall is built. Stores the first line from input file while other bodies are being built.
    wallData = "x"
    
    
    
    #If a wall is to be built, take first sphere entry to use for wall.
    if(wallCheck):
        print("Enter in sphere data to be used for a vacuole wall: ")
        wallData = input()

    print("\nNow enter in all bodies in the format 'Radii X-Coord Y-Coord Z-Coord'. Type STOP when done.")
    print("(Each body should be entered on seperate lines)")
    
    print("\nEnter in the first Body's sphere data: ")
    sphereInput = input()
    bodyNum = 1
    sphereList = []
    
    while(sphereInput!="STOP"):
        sphereList.append(sphereInput)       
        
        print("\nEnter the next Body's sphere data, or STOP:")
        sphereInput = input()
    
    for sphere in sphereList:
        sphereData = sphere.split()
        print("Body #%d: %s %s %s %s" %(bodyNum, sphereData[0], sphereData[1], sphereData[2], sphereData[3]))
        centerPoint = [float(sphereData[1]), float(sphereData[2]), float(sphereData[3])]
        #radius = int(sphereData[0])
        dim = int(sphereData[0])
        radius = dim / 2
        #dim = (radius*2)+1
        
        starterGrid = np.zeros((dim, dim, dim)) # Builds the numpy array.
        sphereGrid = deepcopy(starterGrid) #Copy of the starterGrid.
            
            
        sphereGrid = setUpGrid(sphereGrid, radius) #Fills the grid with 1 to make a "sphere" of given radius.
        sphereToPif(sphereGrid, centerPoint, radius, bodyNum) #Writes out all 1s in the grid as a PIFF coordinate.
        
        bodyNum += 1
    
    #Begins the vacuole wall creation as a semi-hollowed out sphere.    
    if(wallData!="x"):
        buildWall(wallData, bodyNum)
    print("\n\nSphereGen_M is DONE.")
###END OF consoleSphere FUNCTION###
        
'''Builds a hollow sphere around the set of regular spheres that represents a vacuole membrane wall.
    WallData contains the first line of user input (file or console) to be used in the wall building process.'''
def buildWall(wallData, bodyCount):
    #Build default wall
    #print("\nWall Data: %s" %(wallData))
    sphereData = wallData.split()
    print("Wall: %s %s %s %s" %(sphereData[0], sphereData[1], sphereData[2], sphereData[3]))
    radii = (int(sphereData[0]) / 2)
    xCenter = int(sphereData[1])
    yCenter = int(sphereData[2])
    zCenter = int(sphereData[3])
        
    #wallRadius = findRadii(volume)
    
    outStream = open(fileOutput, "a")

    '''The -1s and +3s here extend the range of pixels that count as being on the surface of the wall sphere.
        Without this extension, the wall may be exceedingly thin in certain spots, and depending on its
        overall size, there may be holes or gaps. This extension and the exact numbers used may not be
        optimal and may be adjusted in the future.'''
    for x in range( int((xCenter-radii)-1), int(xCenter+radii+3) ):
        for y in range( int((yCenter-radii)-1), int(yCenter+radii+3) ):
            for z in range( int((zCenter-radii)-1), int(zCenter+radii+3) ):
                dValue = ((x-xCenter)**2) + ((y-yCenter)**2) + ((z-zCenter)**2)
                if(dValue >= (radii**2) and dValue <= ((radii+4)**2)):
                    outStream.write("%d Wall %d %d %d %d %d %d \n" % (bodyCount, x, x, y, y, z, z))
    outStream.close()
###END OF buildWall FUNCTION###
    

'''Fills the given numpy array "grid" with 1s in such a configuration that
    it makes up the image of a sphere with the given radius.'''
def setUpGrid(grid, radius):
    x0, y0, z0 = int(np.floor(grid.shape[0]/2)), \
            int(np.floor(grid.shape[1]/2)), int(np.floor(grid.shape[2]/2))
        
    spherePow = 2
    for x in range(int(x0-radius), int(x0+radius+1)):
        for y in range(int(y0-radius), int(y0+radius+1)):
            for z in range(int(z0-radius), int(z0+radius+1)):
                ''' point: measures how far a coordinate in grid is far from the center. 
                        point >= 0: inside or on the surface of the sphere.
                        point < 0: outside the sphere.'''   
                point = int((radius**spherePow) - (abs(x0-x)**spherePow) - (abs(y0-y)**spherePow) - (abs(z0-z)**spherePow))
                if (point)>=0: 
                    grid[x,y,z] = 1
    return grid
###END OF setUpGrid FUNCTION###

'''Given the volume of a sphere, finds the radii of the smallest sphere
    larger than the given sphere that uses an integer radii. Integers are
    used for radii and volumes because CC3D doesn't deal with decimals or
    partial pixels. Currently unused in version 1.2'''
def findRadii(givenVolume):
    calcRadii = math.pow( ((givenVolume/(math.pi))*(3.0/4.0)), (1/3))
    #^calcRadii is the actual, double value of the given sphere's radii. (I.E. it can be 12.163371 etc.)
    return calcRadii        
###END OF findRadii FUNCTION###

'''Traverses through the given numpy array (grid), and writes the coordinates
    of any found 1s to the given output file, fileOutput, in PIF format for use in CC3D.'''
def sphereToPif(grid, centerArray, radius, bodyCount):
    '''This check just determines if the script overwrites the output file or just appends to it.
        If bodyCount is 1, then it overwrites what was previously in the output file and then
        just appends to it after the initially overwritting.'''
    if(bodyCount==1):
        outStream = open(fileOutput, "w")
    else:
        outStream = open(fileOutput, "a")
    
    #x0,y0,z0 are the grid based center.
    x0, y0, z0 = int(np.floor(grid.shape[0]/2)), \
    int(np.floor(grid.shape[1]/2)), int(np.floor(grid.shape[2]/2))
    
    '''These nested for loops traverse through the given grid 
        writting any 1's found as PIF coordinates to the output file.'''
    for x in range(int(x0-radius), int(x0+radius+1)):
        for y in range(int(y0-radius), int(y0+radius+1)):
            for z in range(int(z0-radius), int(z0+radius+1)):
                if(grid[x][y][z]==1):
                    xPif = (x-x0) + centerArray[0]
                    
                    yPif = (y-y0) + centerArray[1]
                    
                    zPif = (z-z0) + centerArray[2]
                    
                    outStream.write("%d Body %d %d %d %d %d %d \n" % (bodyCount, xPif, xPif, yPif, yPif, zPif, zPif))
    outStream.close()
###END OF sphereToPif FUNCTION###

#This will automatically run this file if imported:
#main()