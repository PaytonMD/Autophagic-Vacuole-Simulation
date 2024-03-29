# -*- coding: utf-8 -*-
import subprocess
import time

import inputAdjustment
import SphereGen_M
import SliceStats_M
import AVSStats
import Condenser_M

from tkinter import Tk
from tkinter.filedialog import askopenfilename

############################################################################################################
#   Eastern Michigan University
#   Backues Lab  
#   Author: Payton Dunning
#   Last Date Modified: July 20th, 2021
#
#   Master script for the Autophagic Vacuole Simulation project software pipeline. This script is used as the initial interface with
#   users and is responsible for calling the other scripts in the pipeline and generally controlling the flow of information and
#   functionality.
#
#   Important Note: AVS software was developed and tested primarily on Windows OS. AVS has not (yet) been
#       tested on Mac or Linux Operating Systems.
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

def main():
    
    print("Welcome to the Autophagic Vacuole Simulation (AVS) Project")
    print("Would you like to run this program with File Explorer selection enabled? [y/n]")
    explorerEnabled = False
    
    optionSelection = input()
    if(optionSelection == "y" or optionSelection == "Y"):
        explorerEnabled = True
    
    while(True):
        print(">>Please select from the following options by entering the corresponding number:")
        print("\t[1]: Single AVS Pipeline Run (COMING SOON)")
        print("\t[2]: Mass AVS Pipeline Runs")
        print("\t[3]: Run GenBalls Alone (COMING SOON)")
        print("\t[4]: Run inputAdjustment Alone")
        print("\t[5]: Run SphereGen Alone")
        print("\t[6]: Run CC3D Simulation Alone (GUI-Less mode)")
        print("\t[7]: Run SliceStats Alone")
        print("\t[8]: Run AVSStats Alone")
        print("\t[9]: Run inputAdjustment + SphereGen")
        print("\t[10]: Run Condenser Utility Script")
        print("\t[11]: Update your Model_Parameters file with new parameters.")
        print("\t[12]: Read the readme file (COMING SOON)")
        print("\t[0]: Exit AVS")
        
        scriptChoice = input()
        
        if(scriptChoice == "0"):
            print("---Now exiting AVS---")
            #This simply exits the program. Equivalent to using sys.exit
            raise SystemExit
        elif(scriptChoice == "1"):
            optionOne(explorerEnabled)
        elif(scriptChoice == "2"):
            optionTwo(explorerEnabled)
        elif(scriptChoice == "3"):
            optionThree(explorerEnabled)
        elif(scriptChoice == "4"):
            optionFour(explorerEnabled)
        elif(scriptChoice == "5"):
            optionFive(explorerEnabled)
        elif(scriptChoice == "6"):
            optionSix(explorerEnabled)
        elif(scriptChoice == "7"):
            optionSeven(explorerEnabled)
        elif(scriptChoice == "8"):
            optionEight(explorerEnabled)
        elif(scriptChoice == "9"):
            optionNine(explorerEnabled)
        elif(scriptChoice == "10"):
            optionTen(explorerEnabled)
        elif(scriptChoice == "11"):
            optionEleven()
        elif(scriptChoice == "12"):
            optionEleven()
        else:
            print("---Invalid Input, please select from options 0~11---")

#[1] Single AVS Pipeline Run (COMING SOON)
def optionOne(fileSelectOpt):
    print("---Option One Selected---")
    print("\tCOMING SOON! Please choose another option.")
    print("---Option One Complete---")
    
#[2] Mass AVS Pipeline Runs (COMING SOON)
def optionTwo(fileSelectOpt):
    print("---Option Two Selected---")
    
    print("\n---Running CC3D requires the CC3D batch file 'runScript.bat',---")
    print("---(The default installation site on Windows is 'C:\CompuCell3D-py3-64bit\'),---")
    print("---As well as a .cc3d file and a .piff file to be selected.---")
    
    #[batFile, cc3dModelFile, piffFile, massRunScaleFactor]
    userData = grabFilesFromUser(fileSelectOpt)
    
    batFile = userData[0]
    cc3dModelFile = userData[1]
    piffFile = userData[2]
    massRunScaleFactor = int(userData[3])
    
        
    massInStream = open("spheregen_input_example.txt","r")
    
    #allData will contain all lines from the input file.
    allData = massInStream.readlines()
    dataByRun = []
    dataListIndex = 0
    
    #Keeps track of how many bodies were originally in each run.
    numBodiesPerRun = []
    lastRun = 0
    
    '''This for loop will iterate over all of the read in lines in allData
     and split them up into a series of sub-lists within dataByRun.
    Each sub-list in dataByRun is a list of lists containing the split up lines
     organized together by run number.
    To clarify, dataByRun is organized as such:
    dataByRun = [[run1Lines], [run2Lines], etc...]
    [run1Lines] = [[split_up_line_1_data], [split_up_line_2_data], etc...]'''
    for line in allData:
        splitLine = line.split()
        
        if(len(splitLine) == 8):
            runNum = splitLine[0]
            
            if(lastRun == 0):
                lastRun = runNum
                bodiesInRun = int(splitLine[1])
                numBodiesPerRun.append(bodiesInRun)
                #Adds an initial sub-list to the dataByRun list.
                dataByRun.append([])
                dataByRun[dataListIndex].append(splitLine)
                
            elif(lastRun != runNum):
                lastRun = runNum
                bodiesInRun = int(splitLine[1])
                numBodiesPerRun.append(bodiesInRun)
                dataByRun.append([])
                dataListIndex += 1
                dataByRun[dataListIndex].append(splitLine)
            else:
                dataByRun[dataListIndex].append(splitLine)
           
    massInStream.close()
    
    
    #Takes each set of lines (runs) and calls inputAdjustment, then SphereGen, then CC3D, then SliceStats
    # with a set of lines (spheredata) at a time.
    for runSet in dataByRun:
        #print("\nRun Set Length: %d" %(len(runSet)))
        #Line coresponding to the first (zeroith) line of a run representing the vacuole wall.
        wallLine = runSet[0]

        inputAdjustment.main(fileSelectOpt, True, runSet, massRunScaleFactor)

        SphereGen_M.main(fileSelectOpt, True)
        
        print("\n\t---Compucell3D Simulation Start (Can take seconds to hours depending on model used.)---")
        startTime = (time.time()*1000.0) # in milliseconds
    
        subprocess.run([batFile, "-i", cc3dModelFile])
    
        endTime = (time.time()*1000.0) # in milliseconds
        print("\n\t---Compucell3D Simulation Finished---")
    
        totalTime = (endTime - startTime)/1000.0 #In seconds
        print("\t---CC3D Model Runtime: ~ %d seconds---" %(totalTime))
    
        SliceStats_M.main(fileSelectOpt, True, piffFile)
        
    print("---Option Two Complete---")

def grabFilesFromUser(fileSelectOpt):
    if(fileSelectOpt == True):
        print(">>Select your 'runScript.bat' file:")
        print("(The file selection screen may appear BEHIND your current application)")
        Tk().withdraw()
        batFile = askopenfilename()
        
        print(">>Select your 'Model.cc3d' file:")
        print("(The file selection screen may appear BEHIND your current application)")
        Tk().withdraw()
        cc3dModelFile = askopenfilename()
        
        print(">>Select your 'Model.piff' file:")
        print("(The file selection screen may appear BEHIND your current application)")
        Tk().withdraw()
        piffFile = askopenfilename()
        
    else:
        print(">>Enter file path+name for your CC3D runScript.bat file:")
        batFile = input()
    
        print(">>Enter file path+name for your CC3D Model's .cc3d file:")
        cc3dModelFile = input()
        
        print("Enter file +ath+name for your CC3D .piff file:")
        piffFile = input()
        
    print("What scale factor would you like to use for this mass run? (Please use whole numbers)")
    massRunScaleFactor = int(input())
    
    return [batFile, cc3dModelFile, piffFile, massRunScaleFactor]
###END OF grabFilesFromUser###
    
    
#[3] Run GenBalls Alone (COMING SOON)
def optionThree(fileSelectOpt):
    print("---Option Three Selected---")
    
    r_path = ""
    script_path = ""
    
    #For testing purposes on Payton D's Computer:
    #r_path = "C:\\Users\\Temp\\.conda\\envs\\rstudio\\lib\\R\\bin\\Rscript.exe"
    #script_path = "C:\\Users\\Temp\\Desktop\\AVS\\Master\\genBalls.r"
    #If errors related to 'dll' files not being found occurs, the easiest solution is usually
    #to just go and download those missing files (not so surprising).
    if(fileSelectOpt==True):
        print(">>Select your 'bin\Rscript.exe' file:")
        print("(The file selection screen may appear BEHIND your current application)")
        Tk().withdraw()
        r_path = askopenfilename()
        
        print(">>Select your 'Master\genBalls.r' file:")
        print("(The file selection screen may appear BEHIND your current application)")
        Tk().withdraw()
        script_path = askopenfilename()
        
    else:
        print("Enter the full path and file name of your 'Rscript.exe' file.")
        r_path = input()
        
        print("Enter the fulle path and file name of your 'genBalls.r' script.")
        script_path = input()
    args = [r_path,"--vanilla", script_path]
    #cmd = [r_path, script_path] + args
    #result = subprocess.check_output(cmd, universal_newlines=True)
    #subprocess.run(cmd, universal_newlines=True)
    fileOut = "rData.txt"
    #subprocess.call(args, shell=True)
    subprocess.run([r_path, script_path])
    #subprocess.run(r_path, script_path, "--vanilla")
    
    print("---Option Three Complete---")

#[4]: Run inputAdjustment Alone
def optionFour(fileSelectOpt):
    print("---Option Four Selected---")
    inputAdjustment.main(fileSelectOpt, False, [], -1)
    print("---Option Four Complete---")
    
#[5]: Run SphereGen Alone
def optionFive(fileSelectOpt):
    print("---Option Five Selected---")
    SphereGen_M.main(fileSelectOpt, False)
    print("---Option Five Complete---")
    
#[6]: Run CC3D Simulation Alone
def optionSix(fileSelectOpt):
    print("---Option Six Selected---")
    print("\n---Running CC3D requires the CC3D batch file 'runScript.bat'.---")
    print("---(The default installation site on Windows is 'C:\CompuCell3D-py3-64bit\')---")
    print("---For both the CC3D batch and model files, please enter their FULL file paths!---\n")
    
    userData = grabFilesFromUser(fileSelectOpt)

    batFile = userData[0]
    cc3dModelFile = userData[1]
    
    #Running CC3D this way require FULL FILE PATHS to the location of "runScript.bat" and the
    #   CC3D model you'd like to use.
    
    #For testing purposes on Payton D' Computer:
    #CC3D Bat File Path+Name: batFile = r"C:\\CompuCell3D-py3-64bit\\runScript.bat"
    #CC3D Model File Path+Name: cc3dModel = r"C:\\Users\\Temp\\Desktop\\AVS\\Master\\AVS_Model\\AVS_Model.cc3d"
    
    print("\n\t---Compucell3D Simulation Start (Can take seconds to hours depending on model used.)---")
    startTime = (time.time()*1000.0) # in milliseconds
    
    subprocess.run([batFile, "-i", cc3dModelFile])
    
    endTime = (time.time()*1000.0) # in milliseconds
    print("\n\t---Compucell3D Simulation Finished---")
    
    
    totalTime = (endTime - startTime)/1000.0 #In seconds
    print("\t---CC3D Model Runtime: ~ %d seconds---" %(totalTime))
    
    print("---Option Six Complete---")
    
#[7]: Run SliceStats Alone
def optionSeven(fileSelectOpt):
    print("---Option Seven Selected---")
    SliceStats_M.main(fileSelectOpt, False, "")
    print("---Option Seven Complete---")
    
#[8] Run AVSStats Alone
def optionEight(fileSelectOpt):
    print("---Option Eight Selected---")
    AVSStats.main(fileSelectOpt)
    print("---Option Eight Complete---")
 
#[9]: Run inputAdjustment + SphereGen
def optionNine(fileSelectOpt):
    print("---Option Nine Selected---")
    inputAdjustment.main(fileSelectOpt, False, [], -1)
    SphereGen_M.main(fileSelectOpt, False)
    print("---Option Nine Complete---")

#[10] Run Condenser Utility Script
def optionTen(fileSelectOpt):
    print("---Option Ten Selected---")
    Condenser_M.main(fileSelectOpt)
    print("---Option Ten Complete---")

#[11] Update model parameters in 'Model_Parameters.txt'
def optionEleven():
    print(">>Please enter new values for parameters:\n")
    print("(The Wall radius parameter value should be a post-scaling value)")
        
    print("\n>>Enter new scaling factor: ")
    scaleFactor = int(input())
        
    #The known Radius of the simulation's Wall sphere.
    print("\n>>Enter the given wall's radius", end='')
    wallRadius = int(input())
        
    #The X value representing the X-coordinate of the Wall sphere's center.
    print("\n>>Enter the given wall's central x-coordinate:", end='')
    centerX = int(input()) 
    
    print("\nUpdating AVS Model Parameters...\n")
    paramsStream = open(paramsFile, "w")
    paramsStream.write("Scale_Factor: %d\n" %(scaleFactor))
    paramsStream.write("Wall_Radius: %d\n" %(wallRadius))
    paramsStream.write("Wall_X_Coordinate: %d\n" %(centerX))
    
    paramsStream.close()
    
#[12] Read the readme file (COMING SOON)
def optionTwelve():
    print("---Option Twelve Selected---")
    print("README is not yet available. Sorry :( ")
    print("---Option Twelve Complete---")
main()