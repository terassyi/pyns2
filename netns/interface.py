import netaddr
from pyroute2 import IPDB, NetNS, NSPopen
from enum import Enum

class Interface():
    def __init__(self, name: str, address: str = None, typ: str = None, peer: str = None, ns_name: str = None):
        self.type = interface_type_from_string(typ)
        if self.type == InterfaceType.veth:
            self.peer_name = peer
        self.name = name
        self.ip = netaddr.IPNetwork(address)
        self.ns_name = ns_name
        self.status = InterfaceStatus.not_created

    def create_in_ns(self):
        ns = NetNS(self.ns_name)
        ipdb = IPDB(nl=ns)
        ipdb.create(kind=str(self.type), ifname=self.name, peer=self.peer_name).commit()
        self.set_addr()
        self.status = InterfaceStatus.down
        print("[info] Created Network Interface name=%s address=%s in netns=%s" % (self.name, str(self.ip), self.ns_name))

    def create_veth(self):
        if is_exist_interface(self.name):
            return
        
        ipdb = IPDB()
        ipdb.create(kind=str(self.type), ifname=self.name, peer=self.peer_name).commit()

    def set_netns(self):
        ipdb = IPDB()
        with ipdb.interfaces[self.name] as iface:
            iface.net_ns_fd = self.ns_name
            print("[info] %s is set netns=%s" % (self.name, self.ns_name))

    def delete(self):
        ipdb = IPDB(nl=NetNS(self.ns_name))
        with ipdb.interfaces[self.name] as iface:
            iface.detach().commit()

    def up(self):
        ipdb = IPDB(nl=NetNS(self.ns_name))
        with ipdb.interfaces[self.name] as iface:
            iface.up()
            self.status = InterfaceStatus.up
            print("[info] Network Interface(%s) is Up" % self.name)

    def down(self):
        ipdb = IPDB(nl=NetNS(self.ns_name))
        with ipdb.interfaces[self.name] as iface:
            iface.down()
            print("[info] Network Interface(%s) is Down" % self.name)

    def set_addr(self, in_ns: bool):
        ipdb = IPDB()
        if in_ns:
            ipdb = IPDB(nl=NetNS(self.ns_name))
        with ipdb.interfaces[self.name] as iface:
            iface.add_ip(str(self.ip))
            print("[info] set address=%s to %s" % (str(self.ip), self.name))

class InterfaceType(Enum):
    veth = 0
    vlan = 1
    bridge = 2
    unknown = 3

    def __str__(self):
        if self == InterfaceType.veth:
            return 'veth'
        elif self == InterfaceType.vlan:
            return 'vlan'
        elif self == InterfaceType.bridge:
            return 'bridge'
        else:
            return ''

def interface_type_from_string(typ: str):
    if typ == "veth":
        return InterfaceType.veth
    elif typ == "vlan":
        return InterfaceType.vlan
    elif typ == "bridge":
        return InterfaceType.bridge
    else:
        return InterfaceType.unknown


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

def is_exist_interface(ifname: str, ns_name: str = None):
    ipdb = IPDB()
    if ns_name is not None:
        ipdb = IPDB(nl=NetNS(ns_name))

    return ifname in ipdb.interfaces
