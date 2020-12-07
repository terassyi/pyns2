import iptc

class NAT(object):
    def __init__(self, config, ns_name: str = None):
        self.src = config['src']
        self.out_iface = config['out_iface']
        self.ns = ns_name
        
    def create(self):
        nat = iptc.Table(iptc.Table.NAT)
        pr = iptc.Chain(nat, "POSTROUTING")
        rule = iptc.Rule()
        rule.out_interface = self.out_iface
        rule.src = self.src
        target = iptc.Target(rule, "MASQUERADE")
        rule.target = target
        pr.insert_rule(rule)
        enable_ipv4_forward()
        print("[info] create NAT setting")

    def delete(self):
        nat = iptc.Table(iptc.Table.NAT)
        pr = iptc.Chain(nat, "POSTROUTING")
        rule = iptc.Rule()
        rule.out_interface = self.out_iface
        rule.src = self.src
        target = iptc.Target(rule, "MASQUERADE")
        rule.target = target
        pr.delete_rule(rule)
        disable_ipv4_forward()
        print("[info] delete NAT setting")

def enable_ipv4_forward():
    ip_forward_path = "/proc/sys/net/ipv4/ip_forward"
    with open(ip_forward_path, "w") as f:
        f.write('1')

def disable_ipv4_forward():
    ip_forward_path = "/proc/sys/net/ipv4/ip_forward"
    with open(ip_forward_path, "w") as f:
        f.write('0')

if __name__ == '__main__':
    enable_ip_forward()
    