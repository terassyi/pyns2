from pyroute2 import NetNS, IPDB

class Route(object):
    def __init__(self, gateway: str, dest: str = "0.0.0.0/0", ns_name: str = None):
        self.dest = dest
        self.gateway = gateway
        self.ns_name = ns_name

    def set(self):
        ipdb = IPDB(nl=NetNS(self.ns_name))
        print("[info] dest=%s gateway=%s in ns=%s" % (self.dest, self.gateway, self.ns_name))
        ipdb.routes.add(dst=self.dest, gateway=self.gateway).commit()
