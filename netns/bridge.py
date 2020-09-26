from netns.interface import Interface, InterfaceType
import netaddr

class Bridge(Interface):
    def __init__(self, ifname: str, address: str = None, ns_name: str = None):
        self.name = ifname
        self.type = InterfaceType.bridge
        self.address = netaddr.IPNetwork(address)
        self.ns_name = ns_name
