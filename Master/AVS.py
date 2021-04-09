# -*- coding: utf-8 -*-

import subprocess
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
#   Last Date Modified: MArch 31st, 2021
#
#   DESCRIPTION
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

#paramsFile is used to keep track of several variables used throughout the pipeline.
paramsFile = "attributes/Model_Parameters.txt"

def main():
    while(True):
        print(">>Please select from the following options by entering the corresponding number:")
        print("[1]: Single AVS Pipeline Run (COMING SOON)")
        print("[2]: Mass AVS Pipeline Runs (COMING SOON)")
        print("[3]: Run GenBalls Alone (COMING SOON)")
        print("[4]: Run inputAdjustment Alone")
        print("[5]: Run SphereGen Alone")
        print("[6]: Run CC3D Simulation Alone (NON-GUI mode)")
        print("[7]: Run SliceStats Alone")
        print("[8]: Run AVSStats Alone")
        print("[9]: Run inputAdjustment + SphereGen")
        print("[10]: Run Condenser Utility Script")
        print("[11]: Read the readme file (COMING SOON)")
        print("[0]: Exit AVS")
        
        scriptChoice = input()
        
        if(scriptChoice == "0"):
            print("Now exiting AVS.")
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
            print("Invalid Input, please select from options 0~11")

#[1] Single AVS Pipeline Run (COMING SOON)
def optionOne():
    print("Option One Selected")
    print("\tCOMING SOON! Please choose another option.")
    
#[2] Mass AVS Pipeline Runs (COMING SOON)
def optionTwo():
    print("Option Two Selected")
    print("\tCOMING SOON! Please choose another option.")

#[3] Run GenBalls Alone (COMING SOON)
def optionThree():
    print("Option Three Selected")
    print("\tCOMING SOON! Please choose another option.")

#[4]: Run inputAdjustment Alone
def optionFour():
    print("Option Four Selected")
    inputAdjustment.main()
    
    
#[5]: Run SphereGen Alone
def optionFive():
    print("Option Five Selected")
    SphereGen_M.main(True)
    
#[6]: Run CC3D Simulation Alone (COMING SOON)
def optionSix():
    print("Option Six Selected")
    
    subprocess.run([r"C:\\CompuCell3D-py3-64bit\\runScript.bat", "-i", r"Master\\AVS_Model\\AVS_Model.cc3d"])
    print("DONE!")
    #print("\tCOMING SOON! Please choose another option.")
    
#[7]: Run SliceStats Alone
def optionSeven():
    print("Option Seven Selected")
    SliceStats_M.main()
    
#[8] Run AVSStats Alone
def optionEight():
    print("Option Eight Selected")
    AVSStats.main()
 
#[9]: Run inputAdjustment + SphereGen
def optionNine():
    print("Option Nine Selected")
    inputAdjustment.main()
    SphereGen_M.main(False)

#[10] Run Condenser Utility Script
def optionTen():
    print("Option Ten Selected")
    Condenser_M.main()

#[11] Read the readme file (COMING SOON)
def optionEleven():
    print("Option Eleven Selected")
    print("README is not yet available. Sorry :( ")

main()