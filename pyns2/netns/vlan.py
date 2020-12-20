from pyns2.netns.interface import Interface, InterfaceType, InterfaceStatus
import netaddr
from pyroute2 import IPDB

class Vlan(Interface):
    def __init__(self, ifname: str, address: str = None, ns_name: str = None):
        self.name = ifname
        self.type = InterfaceType.vlan
        self.ip = netaddr.IPAddress(address)
        self.status = InterfaceStatus.not_created
        self.ns_name = ns_name

    def create(self):
        ipdb = IPDB()
        ipdb.create(kind=str(self.type), ifname=self.name).commit()
        print("[info] create vlan interface name=%s" % self.name)
        self.status = InterfaceStatus.down
