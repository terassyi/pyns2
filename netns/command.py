from pyroute2 import NSPopen
import os
import subprocess


class Command(object):
    def __init__(self, cmd: str, ns_name: str = None, background: bool = True):
        self.cmd = cmd
        self.ns_name = ns_name
        self.background = background

    def exec(self):
        cmd = self.cmd.split(' ')
        
        p = NSPopen(self.ns_name, cmd)
        print("[INFO] execute command: %s" % self.cmd)
        p.release()
        return
