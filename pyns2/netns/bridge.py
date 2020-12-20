from pyns2.netns.interface import Interface, InterfaceType, InterfaceStatus
import netaddr
from pyroute2 import IPDB, NetNS

class Bridge(Interface):
    def __init__(self, ifname: str, iflist, addr: str = None, ns_name: str = None):
        self.name = ifname
        self.type = InterfaceType.bridge
        self.iflist = iflist
        self.ns_name = ns_name
        self.ip = None
        if addr is not None:
            self.ip = netaddr.IPNetwork(addr)
        self.status = InterfaceStatus.not_created

    def create(self):
        ipdb = IPDB()
        if self.ns_name is not None:
            ipdb = IPDB(nl=NetNS(self.ns_name))
        if self.name in ipdb.interfaces.keys():
            print("[info] %s is already created" % self.name)
            return
        ipdb.create(kind=str(self.type), ifname=self.name).commit()
        print("[info] create bridge interface name=%s" % self.name)

        self.status = InterfaceStatus.down

    def set_if(self):
        if self.ns_name is not None:
            ipdb = IPDB()
            for slv_name in self.iflist:
                with ipdb.interfaces[slv_name] as slv:
                    slv.net_ns_fd = self.ns_name
            ipdb = IPDB(nl=NetNS(self.ns_name))
            with ipdb.interfaces[self.name] as br:
                for slv_name in self.iflist:
                    with ipdb.interfaces[slv_name] as slv:
                        br.add_port(slv)
            return

        ipdb = IPDB()
        with ipdb.interfaces[self.name] as br:
            for i in self.iflist:
                with ipdb.interfaces[i] as iface:
                    br.add_port(iface)

    def up(self):
        ipdb = IPDB()
        if self.ns_name is not None:
            ipdb = IPDB(nl=NetNS(self.ns_name))
        with ipdb.interfaces[self.name] as br:
            br.up()
            self.status = InterfaceStatus.up

            for i in self.iflist:
                with ipdb.interfaces[i] as iface:
                    iface.up()


