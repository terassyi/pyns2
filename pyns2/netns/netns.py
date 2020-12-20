import netaddr
import os
import time
from enum import Enum
from pyns2.siml.error import SimlCreateException
from pyns2.siml.util import get_netns_id
from pyns2.netns.exec import start_process
from pyns2.netns.interface import Interface
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
        self.netns_id = 0
        interfaces = []
        for ifname, iface in ifaces.items():
            i = Interface(ifname, address=iface["address"], typ=iface["type"], ns_name=self.name)
            interfaces.append(i)
        self.interfaces = interfaces

    def create(self):
        self.ns = NetNS(self.name)
        # log.info("Created Network Namespace %s" % self.name)
        print("[info] Created Network Namespace %s" % self.name)
        self.register_netns_id()
        self.netns_id = int(get_netns_id(self.name))
        # up loopback interface
        ipdb = IPDB(nl=self.ns)
        with ipdb.interfaces["lo"] as lo:
            lo.add_ip("127.0.0.1/8")
            lo.up()

    def run(self):
        self.ns = NetNS(self.name)
        print("[info] Created Network Namespace %s" % self.name)
        # up loopback interface
        # ipdb = IPDB(nl=self.ns)
        # with ipdb.interfaces["lo"] as lo:
        #     lo.add_ip("127.0.0.1/8")
        #     lo.up()
    
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


    def register_netns_id(self):
        # command = ['python3', 'main.py', 'register_netns_id', self.name]
        command = ['bin/pyns2', 'register_netns_id', self.name]
        p = NSPopen(self.name, command,
            preexec_fn=os.setsid,
            universal_newlines=True)
        time.sleep(0.1)
        p.release()
