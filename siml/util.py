import os

tmp_path = '/tmp/pyns2'

def register_netns_id(ns_name: str):
    res = os.stat("/proc/self/ns/net")
    netns_id = res.st_ino

    with open(os.path.join(tmp_path, ns_name), mode="w") as f:
        f.write(str(netns_id))

def get_netns_id(ns_name: str):
    with open(os.path.join(tmp_path, ns_name), mode='r') as f:
        return f.read()


def mkdir_tmp():
    try:
        os.mkdir(tmp_path)
    except FileExistsError:
        pass
