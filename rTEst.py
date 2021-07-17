# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 11:01:06 2020
https://www.r-bloggers.com/2015/10/integrating-python-and-r-part-ii-executing-r-from-python-and-vice-versa/
@author: Temp
"""
#Test file for calling R script in python.

import subprocess
command = 'Rscript'

path2script = r"C:/Users/Temp/Desktop/AVS/genBalls_for_spheregen.R"
cmd = [command, path2script]

x = subprocess.check_output(cmd, universal_newlines=True)

print(x)