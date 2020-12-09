
arp_table_path = "/proc/net/arp"

class ArpTableEntry(object):
    def __init__(self, line):
        entry = line.split()
        self.ip_address = entry[0]
        self.hw_type = entry[1]
        self.flags = entry[2]
        self.hw_address = entry[3]
        self.mask = entry[4]
        self.device = entry[5]

    def __str__(self):
        return self.ip_address + '\t' + self.hw_type + '\t' + self.flags + '\t' + self.hw_address + '\t' + self.mask + '\t' + self.device

def get_arp_table():
    lines = []
    entrys = []
    with open(arp_table_path) as f:
        lines = f.readlines()
    
    if len(lines) == 1:
        return None
    for l in lines[1:]:
        entrys.append(ArpTableEntry(l))
    return entrys


if __name__ == '__main__':
    table = get_arp_table()
    for e in table:
        print(str(e))
