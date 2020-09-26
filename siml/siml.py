from siml.error import SimlCreateException
from netns.netns import NetNs
from netns.interface import InterfaceType, interface_type_from_string
from netns.veth import Veth
from netns.vlan import Vlan
from netns.bridge import Bridge
from pyroute2 import netns
from pyroute2 import NetNS

class Siml():
    def __init__(self, config):
        if len(list(config.keys())) == 0:
            raise SimlCreateException
        elif len(list(config.keys())) > 1:
            raise SimlCreateException

        self.name = list(config.keys())[0]

        netns_list = []
        interface_list = []
        interface_name_list = []
        for ns_name, ifaces in config[self.name].items():
            for iface in ifaces:
                interface_name_list.append(list(iface.keys())[0])
        for ns_name, ifaces in config[self.name].items():
            ns = NetNs(ns_name, ifaces)
            netns_list.append(ns)
            for iface in ifaces:
                # switch interface types
                name = list(iface.keys())[0]
                typ = interface_type_from_string(iface[name]["type"])
                if typ == InterfaceType.veth:
                    if "peer" in iface[name].keys() and not iface[name]["peer"] in interface_name_list:
                        # peer interface is not existing
                        raise SimlCreateException
                    if "peer" in iface[name].keys():
                        interface_list.append(Veth(ifname=name, address=iface[name]["address"], peer=iface[name]["peer"], ns_name=ns_name))
                    else:
                        interface_list.append(Veth(ifname=name, address=iface[name]["address"], ns_name=ns_name))
                elif typ == InterfaceType.vlan:
                    interface_list.append(Vlan(ifname=name, address=iface[name]["address"], ns_name=ns_name))
                elif typ == InterfaceType.bridge:
                    interface_list.append(Bridge(ifname=name, address=iface[name]["address"], ns_name=ns_name))
        
        self.netns = netns_list
        self.interfaces = interface_list


    def create(self):
        for ns in self.netns:
            ns.create()
        for iface in self.interfaces:
            print("reach here")
            iface.create()

    def set_netns(self):
        for iface in self.interfaces:
            iface.set_netns()
        
        self.set_addr()

    def set_addr(self):
        for iface in self.interfaces:
            iface.set_addr(in_ns=True)

    def run(self):
        for ns in self.netns:
            ns.run()

    def up(self):
        for ns in self.netns:
            for iface in ns.interfaces:
                iface.up()

    def down(self):
        for ns in self.netns:
            for iface in ns.interfaces:
                iface.down()

    def delete(self):
        ns_list = netns.listnetns()
        for ns in self.netns:
            if not ns.name in ns_list:
                continue
            ns.remove()

    def list(self):
        ns_list = netns.listnetns()
        for ns in ns_list:
            print(ns)

    def status(self):

        pass
