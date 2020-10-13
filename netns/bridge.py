from netns.interface import Interface, InterfaceType, InterfaceStatus
import netaddr
from pyroute2 import IPDB, NetNS

class Bridge(Interface):
    def __init__(self, ifname: str, iflist, ns_name: str = None):
        self.name = ifname
        self.type = InterfaceType.bridge
        self.iflist = iflist
        self.ns_name = ns_name
        self.ip = None
        self.status = InterfaceStatus.not_created

    def create(self):
        ipdb = IPDB()
        if self.name in ipdb.interfaces.keys():
            print("[info] %s is already created" % self.name)
            return
        ipdb.create(kind=str(self.type), ifname=self.name).commit()
        print("[info] create bridge interface name=%s" % self.name)

        self.status = InterfaceStatus.down

    def set_if(self):
        ipdb = IPDB()
        if self.ns_name is not None:
            ipdb = IPDB(ns=NetNS(self.ns_name))
        with ipdb.interfaces[self.name] as br:
            for i in self.iflist:
                with ipdb.interfaces[i] as iface:
                    br.add_port(iface)

    def up(self):
        ipdb = IPDB()
        if self.ns_name is not None:
            ipdb = IPDB(ns=NetNS(self.ns_name))
        with ipdb.interfaces[self.name] as br:
            br.up()
            self.status = InterfaceStatus.up

            for i in self.iflist:
                with ipdb.interfaces[i] as iface:
                    iface.up()


