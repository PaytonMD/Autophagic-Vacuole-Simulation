# -*- coding: utf-8 -*-
from tkinter import Tk
from tkinter.filedialog import askopenfilename

#Author: Payton Dunning

print("Welcome to File Fixer, this utility script will contain functions for editing and fixing files in the AVS ecosystem.")

print("\nThe only option for now is removing duplicate body numbers from piff files.")

print("For example, if a piff file had the following piff coordinate format: ")
print("\t4 4 Body 45 45 160 160 12 12")

print("\nThis script could correct any lines like that to: ")
print("\t4 Body 45 45 160 160 12 12")

print("(Notice the extra 4 in the first example has been removed)")

print("Would you like to fix a file with this issue? [y/n]")
fixerCheck = input()

if(fixerCheck == "y" or fixerCheck == "Y"):
    print("Please select the PIFF file you would like to correct: ")
    print("(The file selection screen may appear BEHIND the application you are running this script on)")
    
    Tk().withdraw()
    filename = askopenfilename()
    inputName = filename
    print("Given File Name: %s" %(filename))
    
    print("Now fixing file, please hold...")
    
    piffLines = []
    
    inStream = open(inputName, "r")
    #Fills wallText and bodyText with relevent data from the input file.
    for line in inStream:
        #data = line.split()
        piffLines.append(line)

    inStream.close()
    
    outStream = open(inputName, "w")
    
    for piffCoord in piffLines:
        data = piffCoord.split()
        #Normal coordinates will have Body/Wall in index 1, abnormal coordinates will have them in index 2.
        if( (len(data) > 8 ) and (data[2] == "Body" or data[2] == "Wall")):
            fixedLine = "%s %s %s %s %s %s %s %s \n" %(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
            outStream.write(fixedLine)
    outStream.close()            
    

print("End Script...")