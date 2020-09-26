import netaddr
from enum import Enum
from siml.error import SimlCreateException
from netns.exec import start_process
from netns.interface import Interface
from pyroute2 import IPRoute
from pyroute2 import IPDB
from pyroute2 import NetNS
from pyroute2 import netns
from pyroute2 import NSPopen
import subprocess
import logging

log = logging.getLogger(__name__)

class NetNs():
    def __init__(self, name: str, ifaces):
        self.name = name
        interfaces = []
        for iface in ifaces:
            name = list(iface.keys())[0]
            i = Interface(name, address=iface[name]["address"], typ=iface[name]["type"], ns_name=self.name)
            interfaces.append(i)
        self.interfaces = interfaces

    def create(self):
        self.ns = NetNS(self.name)
        # log.info("Created Network Namespace %s" % self.name)
        print("[info] Created Network Namespace %s" % self.name)

        # up loopback interface
        ipdb = IPDB(nl=self.ns)
        with ipdb.interfaces["lo"] as lo:
            lo.add_ip("127.0.0.1/8")
            lo.up()

    def run(self):
        self.ns = NetNS(self.name)
        print("[info] Created Network Namespace %s" % self.name)
        # up loopback interface
        ipdb = IPDB(nl=self.ns)
        with ipdb.interfaces["lo"] as lo:
            lo.add_ip("127.0.0.1/8")
            lo.up()
    
    def remove(self):
        netns.remove(self.name)

    def set_interface(self, iface):
        ipr = IPRoute()
        index = ipr.link_lookup(ifname=iface.name)[0]
        ipr.link('set', index=index, net_ns_fd=self.name)

    def is_exist_interface(self, ifname: str):
        for iface in self.interfaces:
            if iface.name == ifname:
                return True
        return False
