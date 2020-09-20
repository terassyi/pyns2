import netaddr
from enum import Enum
from siml.error import SimlCreateException

class NetNs():
    def __init__(self, name: str, ifaces):
        self.name = name
        interfaces = []
        for iface in ifaces:
            name = list(iface.keys())[0]
            print(iface)
            i = Interface(name, address=iface[name]["address"], typ=iface[name]["type"])
            interfaces.append(i)
        self.interfaces = interfaces



class Interface():
    def __init__(self, name: str, address: str = None, typ: str = None):
        self.type = interface_type_from_string(typ)
        self.name = name
        self.ip_address = netaddr.IPNetwork(address)

class InterfaceType(Enum):
    veth = 0

def interface_type_from_string(typ: str):
    if typ == "veth":
        return InterfaceType.veth
