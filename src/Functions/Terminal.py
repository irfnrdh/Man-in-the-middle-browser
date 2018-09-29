'''
This file contains the terimal functions this program use
'''

import subprocess, os

from Functions.Arrays import count_layers
from Functions.Parse import get_object_unbyte

def get_terminal_lines(CMD, phrase='', startLine=0):
    '''Run terminal command and get its output'''
    if(count_layers(CMD)>1):
        procs = []
        for i in range(0,len(CMD)):
            if(i==0):
                proc = subprocess.Popen(CMD[i], stdout=subprocess.PIPE)
                procs.append(proc)
            else:
                proc = subprocess.Popen(CMD[i], stdin=procs[i-1].stdout,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                procs.append(proc)

        for i in range(0,len(procs)-1):
            procs[i].stdout.close()

        out, err = procs[-1].communicate()
        return(bytes(out).decode())
    else:
        CMDOutLines = []
        with subprocess.Popen(CMD, stdout=subprocess.PIPE, bufsize=1,
                            universal_newlines=True) as p:
            for line in p.stdout:
                CMDOutLines.append((get_object_unbyte(line)))
        return CMDOutLines[startLine:len(CMDOutLines)]


def check_admin_rights(exitIfNot = False):
    import ctypes
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    
    if(exitIfNot == True):
        if(is_admin == False):
            print("Please start this code with admin rights")
            exit()
    return is_admin