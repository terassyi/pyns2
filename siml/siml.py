from siml.error import SimlCreateException
from netns.netns import NetNs
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

        for k, v in config[self.name].items():
            ns = NetNs(k, v)
            netns_list.append(ns)
        self.netns = netns_list

    def create(self):
        for ns in self.netns:
            ns.create()

    def delete(self):
        ns_list = netns.listnetns()
        for ns in self.netns:
            if not ns.name in ns_list:
                continue
            ns.remove()

    def list(self):
        ns_list = netns.listnetns()
        print(ns_list)
