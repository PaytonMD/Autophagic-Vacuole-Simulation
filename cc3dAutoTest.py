# -*- coding: utf-8 -*-
#from os.path import dirname, join, expanduser
#from cc3d import CompuCellSetup
#from cc3d.CompuCellSetup.CC3DCaller import CC3DCaller
import subprocess

#C:\Users\Temp\Desktop\AVS\Master\AVS_Model\AVS_Model.cc3d
def main():
    subprocess.run([r"C:\\CompuCell3D-py3-64bit\\runScript.bat", "-i", r"Master\\AVS_Model\\AVS_Model.cc3d"])
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