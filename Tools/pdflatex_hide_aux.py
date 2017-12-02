# Hide LaTex auxiliaries 
# Windows 

import glob
import subprocess

## Add extensions if needed
auxiliary = ["aux", "bbl", "bcf", "blg", "log", "run.xml", "gz","out"]

def hide_auxi(extension):
    file_name = glob.glob("*."+extension) #get the file name
    if file_name:	#if not empty 
        [subprocess.run(['attrib',"+h",x]) for x in file_name] 	#set the system attrib to hidden


list(map(hide_auxi,auxiliary))
