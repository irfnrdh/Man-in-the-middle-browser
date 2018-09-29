#!/usr/bin/env python3

from Classes import GlobalVars

from Functions.Ethernet import get_ethernet_interfaces
from Functions.Terminal import check_admin_rights
from Functions.Conversations import Conv_generic_select_from_list, Conv_main_menu

check_admin_rights(True)

globalVars = GlobalVars()
globalVars.ethInterFace = Conv_generic_select_from_list(get_ethernet_interfaces(), "Please select eth interface")

Conv_main_menu(globalVars)