from HMGeneric import ServiceManager, ServiceTypes

class IPForwardingService(ServiceManager):
    def __init__(self):
        super().__init__()
        self.add_service('nt', 'RemoteAccess', ServiceTypes.windowsService)
        self.add_service('posix', '/proc/sys/net/ipv4/ip_forward', ServiceTypes.LinuxBoolFile)

class PreRoutingService(ServiceManager):
    def __init__(self):
        super().__init__()
        self.add_service('nt', 'PreRouting', ServiceTypes.NotWorking)
        self.add_service('posix', 'PreRouting', ServiceTypes.NotWorking)