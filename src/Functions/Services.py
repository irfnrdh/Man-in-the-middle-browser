'''
This file contains the services functions this program use
'''
import os

class IPForwardingService:
    def __init__(self):
        self.serviceStatus:bool = self.check_service_status()
        
    def check_service_status(self):
        if(os.name == "nt"): #windows
            import win32serviceutil
            s = win32serviceutil.QueryServiceStatus('RemoteAccess')
            if(s[1] == 4):
                self.serviceStatus = True
                return True
            else:
                self.serviceStatus = False
                return False
        elif(os.name == "posix"): #linux
            try:       
                file = open("/proc/sys/net/ipv4/ip_forward", 'r')
                line = file.readline()
                file.close()
            finally:
                if(line == "1"):
                    self.serviceStatus = True
                    return True
                else:
                    self.serviceStatus = False
                    return False

    def change_service_status(self):
        if(os.name == "nt"): #windows
            import win32serviceutil
            if(self.serviceStatus == True):
                if(input('Do you want to disable the service ? (y|n) [y]\n' != "n")):
                    os.system("sc config RemoteAccess start=disabled")
                win32serviceutil.StopService('RemoteAccess')
                self.serviceStatus = False
                return False
            else:
                while True:
                    try:
                        win32serviceutil.StartService('RemoteAccess')
                    except:
                        os.system("sc config RemoteAccess start=auto")
                        continue
                    break
                self.serviceStatus = True
                return True
        elif(os.name == "posix"): #linux
            file = open("/proc/sys/net/ipv4/ip_forward", 'w')
            if(self.serviceStatus == True):
                file.write("0")
                self.serviceStatus = False
            else:
                file.write("1")
                self.serviceStatus = True
            file.close()

class PreRoutingService:
    def __init__(self):
        self.serviceStatus:bool = self.check_service_status()
        
    def check_service_status(self):
        if(os.name == "nt"): #windows
            #probably something with netsh
            print('not work yet')
        elif(os.name == "posix"): #linux
            print(1)
        ##################
        return False

    def change_service_status(self):
        if(os.name == "nt"): #windows
            #probably something with netsh
            print('not work yet')
        elif(os.name == "posix"): #linux
            print(1)