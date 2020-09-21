import netaddr
from enum import Enum
from siml.error import SimlCreateException
from pyroute2 import IPRoute
from pyroute2 import NetNS

class NetNs():
    def __init__(self, name: str, ifaces):
        self.name = name
        interfaces = []
        for iface in ifaces:
            name = list(iface.keys())[0]
            i = Interface(name, address=iface[name]["address"], typ=iface[name]["type"])
            interfaces.append(i)
        self.interfaces = interfaces

    def create(self):
        self.ns = NetNS(self.name)

    def set_interface(self, iface):
        index = iface.ipr.lookup(ifname=iface.name)[0]
        iface.ipr.link('set', index=index, net_ns_fd=self.name)

class Interface():
    def __init__(self, name: str, address: str = None, typ: str = None):
        self.type = interface_type_from_string(typ)
        self.name = name
        self.ip_address = netaddr.IPNetwork(address)

    def create(self):
        self.ipr = IPRoute()
        self.ipr.link('add', ifname=self.name, kind=self.type)

        
class InterfaceType(Enum):
    veth = "veth"

def interface_type_from_string(typ: str):
    if typ == "veth":
        return InterfaceType.veth
