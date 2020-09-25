import netaddr
from enum import Enum
from siml.error import SimlCreateException
from netns.exec import start_process
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
        for iface in self.interfaces:
            iface.create()
            # self.set_interface(iface)

    def run(self):
        self.ns = NetNS(self.name)
        print("[info] Created Network Namespace %s" % self.name)
        for iface in self.interfaces:
            iface.create()
            iface.up()
    
    def remove(self):
        netns.remove(self.name)

    def set_interface(self, iface):
        ipr = IPRoute()
        index = ipr.link_lookup(ifname=iface.name)[0]
        ipr.link('set', index=index, net_ns_fd=self.name)

class Interface():
    def __init__(self, name: str, address: str = None, typ: str = None, ns_name: str = None):
        self.type = interface_type_from_string(typ)
        self.name = name
        self.ip = netaddr.IPNetwork(address)
        self.ns_name = ns_name
        self.status = InterfaceStatus.not_created

    def create(self):
        ns = NetNS(self.ns_name)
        ipdb = IPDB(nl=ns)
        ipdb.create(kind=str(self.type), ifname=self.name).commit()
        self.set_addr()
        self.status = InterfaceStatus.down
        print("[info] Created Network Interface name=%s address=%s in netns=%s" % (self.name, str(self.ip), self.ns_name))

    def delete(self):
        ipdb = IPDB(nl=NetNS(self.ns_name))
        with ipdb.interfaces[self.name] as iface:
            iface.detach().commit()

    def up(self):
        ipdb = IPDB(nl=NetNS(self.ns_name))
        with ipdb.interfaces[self.name] as iface:
            iface.up()
            print("[info] Network Interface(%s) is Up" % self.name)

    def down(self):
        ipdb = IPDB(nl=NetNS(self.ns_name))
        with ipdb.interfaces[self.name] as iface:
            iface.down()
            print("[info] Network Interface(%s) is Down" % self.name)

    def set_addr(self, addr: str = None):
        ipdb = IPDB(nl=NetNS(self.ns_name))
        with ipdb.interfaces[self.name] as iface:
            iface.add_ip(str(self.ip))
class InterfaceType(Enum):
    veth = 0

    def __str__(self):
        if self == InterfaceType.veth:
            return 'veth'
        else:
            return ''

def exec_command(ns: str, command):
    if type(command) is not list:
        command  = [command]
    # nsprocess = NSPopen(ns, command, encoding='UTF-8', stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    # nsprocess.wait()
    # output = nsprocess.stdout.read()
    # print(output)
    # nsprocess.stdout.close()
    start_process(ns, command)

def interface_type_from_string(typ: str):
    if typ == "veth":
        return InterfaceType.veth


class InterfaceStatus(Enum):
    not_created = 0
    down = 1
    up = 2

    def __init__(self, status: int):
        self = status
    
    def __str__(self):
        if self == not_created:
            return "NOT_CREATED"
        elif self == down:
            return "DOWN"
        elif self == up:
            return "UP"
        else:
            return "UNKNOWN"
