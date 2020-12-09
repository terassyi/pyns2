from siml.error import SimlCreateException
from netns.netns import NetNs
from netns.interface import InterfaceType, interface_type_from_string
from netns.route import Route
from netns.veth import Veth
from netns.vlan import Vlan
from netns.bridge import Bridge
from netns.nat import NAT
from pyroute2 import netns
from pyroute2 import NetNS, IPDB

class Siml():
    def __init__(self, config):
        if len(list(config.keys())) == 0:
            raise SimlCreateException
        elif len(list(config.keys())) > 1:
            raise SimlCreateException

        self.name = list(config.keys())[0]

        self.netns = []
        self.interfaces = []
        self.interfaces_name = []
        self.routes = []
        self.nat_list = []

        if "host" in config[self.name].keys():
            self.load_host(config[self.name]["host"])

        for ns_name, resources in config[self.name]["netns"].items():
            ifaces = resources['ifaces']
            # print(ifaces)
            ns = NetNs(ns_name, ifaces)
            self.netns.append(ns) 
            self.load_host(resources, ns_name=ns_name)

    def load_host(self, config, ns_name: str = None):
        ifaces = config["ifaces"]
        routes = {}
        if "routes" in config:
            routes = config["routes"]
        for ifname, iface in ifaces.items():
            typ = interface_type_from_string(iface["type"])
            if typ == InterfaceType.veth:
                if "peer" in iface.keys():
                    self.interfaces.append(Veth(ifname=ifname, address=iface["address"], peer=iface["peer"], ns_name=ns_name))
                    # self.interfaces.append(Veth(ifname=iface["peer"], address=iface["address"]))
                else:
                    self.interfaces.append(Veth(ifname=ifname, address=iface["address"], ns_name=ns_name))
            elif typ == InterfaceType.bridge:
                if "address" in iface.keys():
                    self.interfaces.append(Bridge(ifname=ifname, iflist=iface["ifaces"], addr=iface["address"], ns_name=ns_name))
                else:
                    self.interfaces.append(Bridge(ifname=ifname, iflist=iface["ifaces"], ns_name=ns_name))
                # for v in iface["ifaces"]:
                #     self.interfaces.append(Veth(ifname=v, ns_name=ns_name))
            else:
                pass

        for route in routes:
            self.routes.append(Route(gateway=route['route']['gateway'], dest=route['route']['dest'], ns_name=ns_name))

        # nat configure
        if "nat" in config:
            nat_config = config["nat"]
            nat = NAT(nat_config, ns_name=ns_name)
            self.nat_list.append(nat)
            # nat.create()


    def create(self):
        for ns in self.netns:
            ns.create()
        for iface in self.interfaces:
            iface.create()
        for nat in self.nat_list:
            nat.create()

    def set_netns(self):
        for iface in self.interfaces:
            iface.set_netns()
        

    def set_addr(self):
        for iface in self.interfaces:
            iface.set_addr()

    def start(self):
        self.set_netns()
        self.set_bridge()
        self.set_addr()
        self.up()

    def run(self):
        self.create()
        self.set_netns()
        self.set_bridge()
        self.set_addr()
        self.up()

    def up(self):
        for iface in self.interfaces:
            iface.up()
        for route in self.routes:
            route.set()

    def down(self):
        for ns in self.netns:
            for iface in ns.interfaces:
                iface.down()

    def delete(self):
        # delete resources in host namespaces
        ipdb = IPDB()
        for iface in self.interfaces:
            if iface.ns_name is not None:
                continue
            print("[INFO] Delete interface %s in host namespace" % iface.name)
            with ipdb.interfaces[iface.name] as i:
                i.remove()

        for nat in self.nat_list:
            nat.delete()

        ns_list = netns.listnetns()
        for ns in self.netns:
            if not ns.name in ns_list:
                continue
            print("[INFO] Delete netns %s" % ns.name)
            ns.remove()

    def list(self):
        ns_list = netns.listnetns()
        for ns in ns_list:
            print(ns)

    def status(self):

        pass

    def show(self):
        print("[Network Name] ", self.name)
        for ns in self.netns:
            print("[NETNS] ", ns.name)
            for iface in ns.interfaces:
                print("[INTERFACE] ", iface.name)

    def set_bridge(self):
        for iface in self.interfaces:
            if iface.type == InterfaceType.bridge:
                iface.set_if()

    # def output_state(self, path):
        

def enable_ipv4_forward():
    ip_forward_path = "/proc/sys/net/ipv4/ip_forward"
    with open(ip_forward_path, "w") as f:
        f.write('1')

def disable_ipv4_forward():
    ip_forward_path = "/proc/sys/net/ipv4/ip_forward"
    with open(ip_forward_path, "w") as f:
        f.write('0')
