#!/usr/bin/env python3

from Classes import GlobalVars

from HMGeneric.terminal import check_admin_rights
from Menu import start_main_branch

check_admin_rights(True)
globalVars = GlobalVars()
start_main_branch(globalVars)