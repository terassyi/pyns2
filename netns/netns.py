import netaddr
from enum import Enum
from siml.error import SimlCreateException
from pyroute2 import IPRoute
from pyroute2 import NetNS
from pyroute2 import netns
import logging

log = logging.getLogger(__name__)

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
        # log.info("Created Network Namespace %s" % self.name)
        print("[info] Created Network Namespace %s" % self.name)
        for iface in self.interfaces:
            iface.create()
            self.set_interface(iface)
    
    def remove(self):
        netns.remove(self.name)

    def set_interface(self, iface):
        ipr = IPRoute()
        index = ipr.link_lookup(ifname=iface.name)[0]
        ipr.link('set', index=index, net_ns_fd=self.name)

class Interface():
    def __init__(self, name: str, address: str = None, typ: str = None):
        self.type = interface_type_from_string(typ)
        self.name = name
        self.ip = netaddr.IPNetwork(address)

    def create(self):
        ipr = IPRoute()
        if len(ipr.link_lookup(ifname=self.name)) != 0:
            print("[info] Already created name=%s" % self.name)
            return
        ipr.link('add', ifname=self.name, kind=self.type.to_string())

        self.set_addr()
        print("[info] Created Network Interface name=%s address=%s " % (self.name, str(self.ip)))

    def delete(self):
        ipr = IPRoute()
        if len(ipr.link_lookup(ifname=self.name)) == 0:
            return
        ipr.link('del', ifname=self.name)

    def set_addr(self, addr: str = None):
        ipr = IPRoute()
        prefix = 0
        if addr is None:
            addr = str(self.ip.ip)
            prefix = self.ip.prefixlen
        else:
            ip = netaddr.ip_network(addr)
            addr = str(ip.ip)
            prefix = ip.prefixlen

        index = ipr.link_lookup(ifname=self.name)[0]
        ipr.addr('add', index=index, address=addr, prefixlen=prefix)
class InterfaceType(Enum):
    veth = 0

    def to_string(self):
        if self is InterfaceType.veth:
            return 'veth'
        else:
            ''

def interface_type_from_string(typ: str):
    if typ == "veth":
        return InterfaceType.veth
