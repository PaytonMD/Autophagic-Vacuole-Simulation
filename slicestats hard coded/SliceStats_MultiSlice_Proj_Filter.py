# -*- coding: utf-8 -*-
import sys
import random
import math
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
from skimage import measure 
############################################################################################################
#   Eastern Michigan University
#   Backues Lab  
#   Author: Payton Dunning, Andrew Ross and Steven Backues
#   Last Date Modified: July15th, 2021
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
        bodyImages = []
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
        
        ArDim = 2*(wallRadius+1) # Dimension of the array will be just slightly larger than of the simulation, to make sure that no pixels are right on the edge (needed later)


        overalldfsk = pd.DataFrame()
        if len(lineCollection) > 0:
            for array in lineCollection:
                index2 = 0
                currentArea = 0
                currentPixels = []
                #print ("body array")
                #print (array)
                projectionData = []
                projectionData.append(array[index2].split())  #gets ProjectionData started by adding the very first line
                lineData = array[index2].split()
                Pixels = [int(lineData[4]), int(lineData[6])] #list of the just the yz pixels, for making the binary image later
                Shift = 1
                shiftedPixels = [x + Shift for x in Pixels]   #So that no pixels are right on the edge, later
                currentPixels.append(shiftedPixels) 
                #print ("initial projection data")
                #print (projectionData)
                #lineData = lineCollection[index1][index2].split()
                for line in array:
                    lineData = array[index2].split()
                    currentBody = int(lineData[0])
                    #print ("Current Body")
                    #print (currentBody)
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
                        #else: 
                            #print ("done looking - not there")
                    if found <1:
                        projectionData.append(lineData)
                        Pixels = [int(lineData[4]), int(lineData[6])]  #list of the just the yz pixels, for making the binary image later
                        shiftedPixels = [x + Shift for x in Pixels]   #So that no pixels are right on the edge, later
                        currentPixels.append(shiftedPixels)    
                        #print ("not there - adding line")
                  #  else:
                  #      print ("not adding a line because it is a duplicate")
                    #print ("projectionData")
                    #print (projectionData)
                    index2 += 1
                #print("final projectionData")
                #print (projectionData)
                currentArea = len(projectionData)
                if(currentArea >= recogLimit):
                    bodyAreas.append([currentBody, currentArea])
                    '''Now to make the imageArray for each body - a Numpy array the size of the simulation, with "1's" at every pixel location, and "0's" 
                everywhere there isn't a pixel'''
                    imageArray = np.zeros ((ArDim, ArDim), dtype=int)
                    for pix in currentPixels:
                        imageArray[pix[0],pix[1]] = 1
                    bodyImages.append(imageArray)
                    all_labels = measure.label(imageArray)
                    propertylist=['label', 'bbox', 'area', 'centroid', 'convex_area','eccentricity','euler_number','filled_area','major_axis_length','minor_axis_length','perimeter']
                    '''this will add all regions that it finds to the dataframe, even those with areas below the recognition limit. We will filter those out later.
                    It’s nice to have all of them recorded for filtering out later, so we can also do stats all at once on what gets filtered out.
                    Area and perimeter units are pixels, not nanometers (nm); we’ll translate numbers in the dataframe to nm all at once later.'''
                    if( np.sum(all_labels) > 0):
                        props2 = measure.regionprops_table(all_labels,properties=propertylist)
                        df_skimage = pd.DataFrame(props2)  
                        df_skimage['imgnum'] = currentBody
                        overalldfsk = overalldfsk.append(df_skimage,ignore_index=True)
                index1 += 1
                
            print(overalldfsk) 
            """ Filtering out tiny regions."""
            big_enough = overalldfsk['area'] >= recogLimit
            too_small = np.invert(big_enough)
            print(big_enough)
            print(too_small)
            # do the filtering:
            overalldfsk_big_enough = overalldfsk[big_enough]
            ''' Now that we've filtered out the too-small regions, let's look for APBs that had more than 1 big-enough region.
            We'll do what's called a "pivot table" in Excel. To quantify how spread-out the areas are for any bodynumber,
            we'll use the statistical range (max-minus-min), which Python calls 'ptp'=peak-to-peak,
            We'll also take the StdDev, though that gives NaN when there's only 1 region for a bodynumber. 
            Any imagenum with count_area >= 2 has multiple regions in it (and they are not just tiny ones, since we filtered those out already)
            Then we'll rename those bodies with greater than one area with new numbers - a new body number for each area'''
            pvt_df=overalldfsk_big_enough.pivot_table(values='area',index='imgnum',aggfunc=["count",np.mean,np.std,np.amax,np.ptp])
            pvt_df.columns = list(map("_".join, pvt_df.columns)) #renames the columns with simpler names
            print(pvt_df.columns)
            print (pvt_df)  #this is a pandas dataframe
            pvt_df_split = pvt_df[pvt_df['count_area'] >= 2] #subsetting just those bodies that are split in two
            if (len(pvt_df_split) >= 1):
                pvt_df_single =pvt_df[pvt_df['count_area'] < 2] #subsetting just those bodies that are whole
                singles = pvt_df_single.index
                splits = pvt_df_split.index
                print (splits)
                print (singles)
                #now to rename the bodies that are split in parts, giving each part a new body number
                new_bod_nums_req = len(pvt_df_split) # how many new body numbers we need
                new_bod_nums = range(1000, 1001+new_bod_nums_req, 1)
                #print (new_bod_nums)
                overalldfsk_single = overalldfsk_big_enough[overalldfsk_big_enough["imgnum"].isin(singles)] # filters the original list by just the single bodies
                #print (overalldfsk_single)
                overalldfsk_splits = overalldfsk_big_enough[overalldfsk_big_enough["imgnum"].isin(splits)] # filters the original list by just the split bodies
                #print (overalldfsk_splits)
                overalldfsk_splits.loc[:,"imgnum"] = new_bod_nums  #giving the splits data frame the new body numbers
                #print (overalldfsk_splits)
                overalldfsk_new = overalldfsk_single.append(overalldfsk_splits) #this has the data on all of the bodies, with unique body numbers
                print (overalldfsk_new)
            else:
                overalldfsk_new = overalldfsk_big_enough
            
            # I need to adjust the area and perimeter by the scale factor
            overalldfsk_new["area_scaled"] = scaleFactor**2*overalldfsk_new["area"]
            overalldfsk_new["perimeter_scaled"] = scaleFactor*overalldfsk_new["perimeter"]
            # Now to do some more calculations to get exactly the data I want, Aspect Ratio (AR) and Circularity 
            overalldfsk_new["AR"]=overalldfsk_new["major_axis_length"] / overalldfsk_new["minor_axis_length"]  #Adds Aspect ratio column
            overalldfsk_new["circularity"]= 4*math.pi*overalldfsk_new["area_scaled"] / (overalldfsk_new["perimeter_scaled"]**2)  #Adds circularity column
            overalldfsk_new["time"] = initialTime
            overalldfsk_new.rename(columns = {"imgnum":"body_number"}, inplace=True)
            # Now need to export just what we want, in a nice format
            finalOutput = overalldfsk_new[["time", "body_number", "area_scaled", "perimeter_scaled", "circularity", "AR"]]
            print (finalOutput)
            finalOutput.to_csv ("sliceData/sliceMeasurements.csv", mode='a')  
        else:
            print ("no bodies captured in slice" + " " + str(SX) + ". Inserting blank line (time stamp only) into output")
            Blankdf = pd.DataFrame({"time":[initialTime]})
            print(Blankdf)
            Blankdf.to_csv ("sliceData/sliceMeasurements.csv", mode='a')
# Calls main to run the program
main(1)