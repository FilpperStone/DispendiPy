import os
import signal
import psutil

def close_parent_process():
    PROCNAME = "Dispendi.exe"

    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()
def open_new_executable():
    os.system(workingdir)

print("working")
workingdir = os.path.join(os.getcwd, "..\Dispendi.exe")
print(workingdir)
s=input()
close_parent_process()
open_new_executable()
