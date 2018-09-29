'''
This file contains the conversation functions this program use
'''

from Functions.Ethernet import get_ethernet_interfaces, get_arp_table

from KameneCustom.Interfaces import get_my_default_iface
from KameneCustom.Arp import start_arp_poison

def Conv_main_menu(globalVars):
    chose = 99
    while(chose != '0'):
        print('Welcome to MitmB - Man in the middle Browser')
        print('Select the option number :')
        print('1. Set targets')
        print('2. Confirm services')
        print('3. Set attack')
        print('0. Exit')

        chose = input("Option number ?\n")
        if(chose == '1'):
            Conv_set_targets(globalVars)
        elif(chose == '2'):
            Conv_confirm_services(globalVars)
        elif(chose == '3'):
            Conv_set_attack(globalVars)
    exit()

def Conv_set_targets(globalVars):
    chose = 99
    while(chose != '0'):
        print('Set targets :')
        print('1. Change eth interface')
        print('2. Select victim ARP')
        print('3. Select gateway ARP')
        print('4. Select Man in the middle ARP')
        print('0. Back')

        chose = input("Option number ?\n")
        if(chose == '1'):
            print('Current : ' + globalVars.ethInterFace)
            globalVars.ethInterFace = Conv_generic_select_from_list(get_ethernet_interfaces(), "Please select eth interface")
        elif(chose == '2'):
            print('Current target : ' + globalVars.victimArp.IPAddress + " | " + globalVars.victimArp.MACAddress)
            arpString: str = Conv_generic_select_from_list(get_arp_table(globalVars.ethInterFace), "Please select target ip address")
            globalVars.victimArp.IPAddress = arpString.split(' - ')[0]
            globalVars.victimArp.MACAddress = arpString.split(' - ')[1]
        elif(chose == '3'):
            print('Current gateway : ' + globalVars.gatewayArp.IPAddress + " | " + globalVars.gatewayArp.MACAddress)
            arpString: str = Conv_generic_select_from_list(get_arp_table(globalVars.ethInterFace), "Please select target ip address")
            globalVars.gatewayArp.IPAddress = arpString.split(' - ')[0]
            globalVars.gatewayArp.MACAddress = arpString.split(' - ')[1]
        elif(chose == '4'):
            '''#lab
            if(globalVars.arpPosion == False):
                globalVars.set_lab_thread()
                globalVars.lab_thread.start()
            else:
                globalVars.arpPosion = False'''
            
            print('Current middle : ' + globalVars.middleArp.IPAddress + " | " + globalVars.middleArp.MACAddress)
            while not(chose in range(1,4)):
                print('1. Keep current')
                print('2. Get default')
                print('3. Set custom')
                chose = input("Option number ?\n")

                if(chose == '2'):
                    globalVars.middleArp = get_my_default_iface()
                elif(chose == '3'):
                    globalVars.middleArp.MACAddress = input('MAC Address:\n')
                    globalVars.middleArp.IPAddress = input('IP Address:\n')
                if(chose.isdigit()):
                    chose = int(chose)

def Conv_confirm_services(globalVars):
    chose = 99
    while(chose != '0'):
        print('Confirm services :')
        if(globalVars.Service_portForward.serviceStatus == False):
            print('1. Start port forwarding service')
        else:
            print('1. Stop port forwarding service')
        if(globalVars.Service_preRouting.serviceStatus == False):
            print('2. Start prerouting service')
        else:
            print('2. Stop prerouting service')
        print('0. Back')

        chose = input("Option number ?\n")
        if(chose == '1'):
            globalVars.Service_portForward.change_service_status()
            

def Conv_set_attack(globalVars):
    chose = 99
    while(chose != '0'):
        print('Set attack :')
        print('1. Set string to inject')
        if(globalVars.arpPosion == False):
            print('2. Start ARP poisioning')
        else:
            print('2. Stop ARP poisioning')
            print('3. Show poisioning status')
        print('0. Back')

        chose = input("Option number ?\n")
        
        '''elif(chose == '1'):
            #lab
            if(globalVars.arpPosion == False):
                globalVars.set_lab_thread()
                globalVars.lab_thread.start()
            else:
                globalVars.arpPosion = False'''
            
        if(chose == '2'):
            if(globalVars.arpPosion == False):
                start_arp_poison(globalVars)
            else:
                globalVars.arpPosion = False

        elif(chose == '3' and globalVars.arpPosion == True):
            print('Poision Status:')
            print('Packets recieved from target : ' + str(len(globalVars.packets_TargetToGatway)))
            print('Packets recieved from gateway : ' + str(len(globalVars.packets_GatwayToTarget)))


def Conv_generic_select_from_list(List: list, phrase):
    chose = 0
    while not(chose in range(1, len(List)+1)):
        print(phrase)
        for i in range(0, len(List)):
            print(str(i+1) + ". " + List[i])
        chose = input("Option number ?\n")
        if(chose.isdigit()):
            chose = int(chose)
        else:
            chose = 0

    return List[chose-1]