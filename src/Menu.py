'''
This file contains the menu classes and functions this program use
'''

from HMGeneric.menu import MenuRoot, select_from_list
from HMGeneric.ethernet import get_ethernet_interfaces, get_arp_table, get_my_interface

def get_branch_targets(menuRoot: MenuRoot):
    def select_victim_arp():
        print('Current target : ' + menuRoot.globalVars.victimArp.IPAddress + " | " + menuRoot.globalVars.victimArp.MACAddress)
        arpString: str = select_from_list(get_arp_table(menuRoot.globalVars.myInterface['ip']), "Please select target ip address")
        menuRoot.globalVars.victimArp.IPAddress = arpString.split(' - ')[0]
        menuRoot.globalVars.victimArp.MACAddress = arpString.split(' - ')[1]
    
    def select_gateway_arp():
        print('Current gateway : ' + menuRoot.globalVars.gatewayArp.IPAddress + " | " + menuRoot.globalVars.gatewayArp.MACAddress)
        arpString: str = select_from_list(get_arp_table(menuRoot.globalVars.myInterface['ip']), "Please select target ip address")
        menuRoot.globalVars.gatewayArp.IPAddress = arpString.split(' - ')[0]
        menuRoot.globalVars.gatewayArp.MACAddress = arpString.split(' - ')[1]
    
    def select_mitm_arp():
        print('Current middle : ' + menuRoot.globalVars.middleArp.IPAddress + " | " + menuRoot.globalVars.middleArp.MACAddress)
        options = ['Keep current', 'Get default', 'Set custom']
        chose = options.index(select_from_list(options, ''))+1
        if(chose == 2):
            menuRoot.globalVars.middleArp.MACAddress = menuRoot.globalVars.myInterface['mac']
            menuRoot.globalVars.middleArp.IPAddress = menuRoot.globalVars.myInterface['ip']
        elif(chose == 3):
            menuRoot.globalVars.middleArp.MACAddress = input('MAC Address:\n')
            menuRoot.globalVars.middleArp.IPAddress = input('IP Address:\n')

    if not (menuRoot.get_branch(name='targets')):
        menuRoot.add_branch(name='targets', title='Set targets :')
        menuRoot.get_branch(name='targets').parentBranch = 'main'
    menuRoot.get_branch(name='targets').options.clear()
    menuRoot.get_branch(name='targets').add_menu_option('targets', select_victim_arp, 'Select victim ARP')
    menuRoot.get_branch(name='targets').add_menu_option('targets', select_gateway_arp, 'Select gateway ARP')
    menuRoot.get_branch(name='targets').add_menu_option('targets', select_mitm_arp, 'Select Man in the middle ARP')

def get_branch_services(menuRoot: MenuRoot):
    if not (menuRoot.get_branch(name='services')):
        menuRoot.add_branch(name='services', title='Confirm services :')
        menuRoot.get_branch(name='services').parentBranch = 'main'
    menuRoot.get_branch(name='services').options.clear()
    if(menuRoot.globalVars.Service_portForward.check_service_status() == False):
        menuRoot.get_branch(name='services').add_menu_option('main', menuRoot.globalVars.Service_portForward.change_service_status, 'Start port forwarding service')
    else:
        menuRoot.get_branch(name='services').add_menu_option('main', menuRoot.globalVars.Service_portForward.change_service_status, 'Stop port forwarding service')
    if(menuRoot.globalVars.Service_preRouting.check_service_status() == False):
        menuRoot.get_branch(name='services').add_menu_option('main', menuRoot.globalVars.Service_preRouting.change_service_status, 'Start prerouting service')
    else:
        menuRoot.get_branch(name='services').add_menu_option('main', menuRoot.globalVars.Service_preRouting.change_service_status, 'Stop prerouting service')

def get_branch_attacks(menuRoot: MenuRoot):
    if not (menuRoot.get_branch(name='attacks')):
        menuRoot.add_branch(name='attacks', title='Set attacks :')
        menuRoot.get_branch(name='attacks').parentBranch = 'main'
    menuRoot.get_branch(name='attacks').options.clear()
    menuRoot.get_branch(name='attacks').add_menu_option('attacks', 'targets', 'Set string to inject')
    if(menuRoot.globalVars.arpPosion.status == False):
        menuRoot.get_branch(name='attacks').add_menu_option('main', menuRoot.globalVars.arpPosion.start, 'Start ARP poisioning')
    else:
        menuRoot.get_branch(name='attacks').add_menu_option('main', menuRoot.globalVars.arpPosion.stop_posion, 'Stop ARP poisioning')

def start_main_branch(globalVars):
    globalVars.menu.add_branch(name='main', title='Welcome to MitmB - Man in the middle Browser')
    globalVars.menu.get_branch(name='main').add_menu_option('targets', get_branch_targets, 'Set targets', True)
    globalVars.menu.get_branch(name='main').add_menu_option('services', get_branch_services, 'Confirm services', True)
    globalVars.menu.get_branch(name='main').add_menu_option('attacks', get_branch_attacks, 'Set attacks', True)
    globalVars.menu.set_current_branch(name='main')