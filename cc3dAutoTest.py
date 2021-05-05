# -*- coding: utf-8 -*-
#from os.path import dirname, join, expanduser
#from cc3d import CompuCellSetup
#from cc3d.CompuCellSetup.CC3DCaller import CC3DCaller
import subprocess
import time

#C:\Users\Temp\Desktop\AVS\Master\AVS_Model\AVS_Model.cc3d
def main():
    print("cc3d Auto Test Start\n")
    startTime = (time.time()*1000) # in milliseconds
    
    #For testing purposes on Payton D' Computer:
    batFile = r"C:\\CompuCell3D-py3-64bit\\runScript.bat"
    cc3dModel = r"C:\\Users\\Temp\\Desktop\\AVS\\Master\\AVS_Model\\AVS_Model.cc3d"
    
    #...\runScript.bat is meant to run CC3D in GUI-less mode, which we should be faster running
    #than GUI mode. ...\compucell3d.bat is used to run CC3D with the player (GUI).
    #subprocess.run([r"C:\\CompuCell3D-py3-64bit\\runScript.bat", "-i", r"C:\\Users\\Temp\\Desktop\\AVS\\Master\\AVS_Model\\AVS_Model.cc3d"])
    
    subprocess.run([batFile, "-i", cc3dModel])
    
    
    endTime = (time.time()*1000) # in milliseconds
    totalTime = (endTime - startTime)/1000 #In seconds
    print("Time to complete: ~ %d seconds" %(totalTime))
    print("DONE!")
#Help

main()


   

#print("Hello")
#simulation_fname = r"C:\Users\Temp\Desktop\AVS\Master\AVS_Model\AVS_Model.cc3d"
#root_output_folder = join(expanduser('~'), 'CC3DCallerOutput')
    
#sim_fnames= [simulation_fname] * 1

#cc3d_caller = CC3DCaller(cc3d_sim_fname=sim_fnames,result_identifier_tag=1)
#ret_values = []
#ret_value = cc3d_caller.run()
#ret_values.append(ret_value)'''