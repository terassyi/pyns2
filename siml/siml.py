from siml.error import SimlCreateException
from netns.netns import NetNs

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
