from pyns2.netns.interface import Interface, InterfaceType, InterfaceStatus
import netaddr
from pyroute2 import IPDB

class Veth(Interface):
    def __init__(self, ifname: str, address: str = None, peer: str = None, ns_name: str = None):
        self.name = ifname
        self.type = InterfaceType.veth
        if address is not None:
            self.ip = netaddr.IPNetwork(address)
        self.peer = peer
        self.status = InterfaceStatus.not_created
        self.ns_name = ns_name

    def create(self):
        ipdb = IPDB()
        if self.name in ipdb.interfaces.keys():
            print("[info] %s is already created" % self.name)
            return
        ipdb.create(kind=str(self.type), ifname=self.name, peer=self.peer).commit()
        print("[info] create veth interface name=%s" % self.name) 
        self.status = InterfaceStatus.down

