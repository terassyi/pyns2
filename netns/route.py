from pyroute2 import NetNS, IPDB

class Route(object):
    def __init__(self, gateway: str, dest: str = "0.0.0.0/0"):
        self.dest = dest
        self.gateway = gateway

    def set(self, ns_name: str = None):
        ipdb = IPDB(nl=NetNS(ns_name))
        print("[info] dest=%s gateway=%s in ns=%s" % (self.dest, self.gateway, ns_name))
        ipdb.routes.add(dst=self.dest, gateway=self.gateway).commit()
