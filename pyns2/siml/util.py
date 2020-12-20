import os
import glob

tmp_path = '/tmp/pyns2'

def register_netns_id(ns_name: str):
    res = os.stat("/proc/self/ns/net")
    netns_id = res.st_ino

    with open(os.path.join(tmp_path, ns_name), mode="w") as f:
        f.write(str(netns_id))


def get_netns_id(ns_name: str):
    with open(os.path.join(tmp_path, ns_name), mode='r') as f:
        return f.read()


def get_netns_name():
    res = os.stat('/proc/self/ns/net')
    netns_id = res.st_ino
    file_list = list(map(lambda f: os.path.basename(f), glob.glob(os.path.join(tmp_path, '*'))))
    for name in file_list:
        ns_id = get_netns_id(name)
        if int(ns_id) == int(netns_id):
            return name
    return ""



def remove_netns_id():
    file_list = glob.glob(os.path.join(tmp_path, '*'))
    for file in file_list:
        os.remove(file)


def is_host_namespace():
    name = get_netns_name()
    if name != 'host':
        return False
    return True


def mkdir_tmp():
    try:
        os.mkdir(tmp_path)
    except FileExistsError:
        pass
