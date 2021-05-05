# -*- coding: utf-8 -*-

import subprocess
import time

import inputAdjustment
import SphereGen_M
import SliceStats_M
import AVSStats
import Condenser_M
#from rpy2.robjects import r

############################################################################################################
#   Eastern Michigan University
#   Backues Lab  
#   Author: Payton Dunning
#   Last Date Modified: May 3rd, 2021
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
    while(True):
        print(">>Please select from the following options by entering the corresponding number:")
        print("\t[1]: Single AVS Pipeline Run (COMING SOON)")
        print("\t[2]: Mass AVS Pipeline Runs (COMING SOON)")
        print("\t[3]: Run GenBalls Alone (COMING SOON)")
        print("\t[4]: Run inputAdjustment Alone")
        print("\t[5]: Run SphereGen Alone")
        print("\t[6]: Run CC3D Simulation Alone (NON-GUI mode)")
        print("\t[7]: Run SliceStats Alone")
        print("\t[8]: Run AVSStats Alone")
        print("\t[9]: Run inputAdjustment + SphereGen")
        print("\t[10]: Run Condenser Utility Script")
        print("\t[11]: Read the readme file (COMING SOON)")
        print("\t[0]: Exit AVS")
        
        scriptChoice = input()
        
        if(scriptChoice == "0"):
            print("---Now exiting AVS---")
            #This simply exits the program. Equivalent to using sys.exit
            raise SystemExit
        elif(scriptChoice == "1"):
            optionOne()
        elif(scriptChoice == "2"):
            optionTwo()
        elif(scriptChoice == "3"):
            optionThree()
        elif(scriptChoice == "4"):
            optionFour()
        elif(scriptChoice == "5"):
            optionFive()
        elif(scriptChoice == "6"):
            optionSix()
        elif(scriptChoice == "7"):
            optionSeven()
        elif(scriptChoice == "8"):
            optionEight()
        elif(scriptChoice == "9"):
            optionNine()
        elif(scriptChoice == "10"):
            optionTen()
        elif(scriptChoice == "11"):
            optionEleven()
        else:
            print("---Invalid Input, please select from options 0~11---")

#[1] Single AVS Pipeline Run (COMING SOON)
def optionOne():
    print("---Option One Selected---")
    print("\tCOMING SOON! Please choose another option.")
    
#[2] Mass AVS Pipeline Runs (COMING SOON)
def optionTwo():
    print("---Option Two Selected---")
    print("\tCOMING SOON! Please choose another option.")

#[3] Run GenBalls Alone (COMING SOON)
def optionThree():
    print("---Option Three Selected---")
    r_path = "C:\\Users\\Temp\\.conda\\envs\\rstudio\\lib\\R\\bin\\Rscript.exe"
    script_path = "C:\\Users\\Temp\\Desktop\\AVS\\Master\\genBalls.r"
    args = [r_path,"--vanilla", script_path]
    #cmd = [r_path, script_path] + args
    #result = subprocess.check_output(cmd, universal_newlines=True)
    #subprocess.run(cmd, universal_newlines=True)
    fileOut = "rData.txt"
    subprocess.call(args, shell=True)
    
    print("Option 3 Done!")
    

#[4]: Run inputAdjustment Alone
def optionFour():
    print("---Option Four Selected---")
    inputAdjustment.main()
    
    
#[5]: Run SphereGen Alone
def optionFive():
    print("---Option Five Selected---")
    SphereGen_M.main(True)
    
#[6]: Run CC3D Simulation Alone
def optionSix():
    print("---Option Six Selected---")
    print("\n---Running CC3D requires the CC3D batch file 'runScript.bat'.---")
    print("---(The default installation site on Windows is 'C:\CompuCell3D-py3-64bit\')---")
    print("---For both the CC3D batch and model files, please enter their FULL file paths!---\n")
    
    print(">>Enter file path+name for your CC3D runScript.bat file:")
    batFile = input()
    
    print(">>Enter file path+name for your CC3D Model's .cc3d file:")
    cc3dModelFile = input()
    
    #Running CC3D this way require FULL FILE PATHS to the location of "runScript.bat" and the
    #   CC3D model you'd like to use.
    
    #For testing purposes on Payton D' Computer:
    #CC3D Bat File Path+Name: batFile = r"C:\\CompuCell3D-py3-64bit\\runScript.bat"
    #CC3D Model File Path+Name: cc3dModel = r"C:\\Users\\Temp\\Desktop\\AVS\\Master\\AVS_Model\\AVS_Model.cc3d"
    
    print("\n\t---Compucell3D Simulation Start (Can take seconds to hours depending on model used.)---")
    startTime = (time.time()*1000) # in milliseconds
    
    subprocess.run([batFile, "-i", cc3dModelFile])
    
    endTime = (time.time()*1000) # in milliseconds
    print("\n\t---Compucell3D Simulation Finished---")
    
    
    totalTime = (endTime - startTime)/1000 #In seconds
    print("\t---CC3D Model Runtime: ~ %d seconds---" %(totalTime))
    
    print("---Option Six Complete---")
    #print("\tCOMING SOON! Please choose another option.")
    
#[7]: Run SliceStats Alone
def optionSeven():
    print("---Option Seven Selected---")
    SliceStats_M.main(True)
    
#[8] Run AVSStats Alone
def optionEight():
    print("---Option Eight Selected---")
    AVSStats.main()
 
#[9]: Run inputAdjustment + SphereGen
def optionNine():
    print("---Option Nine Selected---")
    inputAdjustment.main()
    SphereGen_M.main(False)

#[10] Run Condenser Utility Script
def optionTen():
    print("---Option Ten Selected---")
    Condenser_M.main()

#[11] Read the readme file (COMING SOON)
def optionEleven():
    print("---Option Eleven Selected---")
    print("README is not yet available. Sorry :( ")

main()