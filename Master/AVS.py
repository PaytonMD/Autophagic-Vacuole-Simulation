# -*- coding: utf-8 -*-

import inputAdjustment
import SphereGen_M
import SliceStats_M

############################################################################################################
#   Eastern Michigan University
#   Backues Lab  
#   Author: Payton Dunning
#   Last Date Modified: October 13th, 2020
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


def main():
    while(True):
        print("Please select from the following options by entering the corresponding number:")
        print("[1]: inputAdjustment + SphereGen")
        print("[2]: SliceStats")
        print("[3]: inputAdjustment")
        print("[4]: SphereGen")
        print("[5] readme (coming soon)")
        print("[0] Exit AVS")
        
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
        else:
            print("Invalid Input, please select from options 0~5")

def optionOne():
    print("Option One Selected")
    inputAdjustment.main()
    SphereGen_M.main(False)
    
def optionTwo():
    print("Option Two Selected")
    SliceStats_M.main()
    
def optionThree():
    print("Option Three Selected")
    inputAdjustment.main()
    
def optionFour():
    print("Option Four Selected")
    SphereGen_M.main(True)
    
def optionFive():
    print("Option Five Selected")
    print("README is not yet available.")

main()