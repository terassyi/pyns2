# from parser.parser import parse
import fire
from pyns2.parser.parser import parse
from pyns2.netns.exec import exec_command
from pyns2.siml.util import register_netns_id, get_netns_name


class NetNsSiml(object):

    def create(self, config: str = None):
        siml = parse(config)
        siml.create()

    def set(self, config: str = None):
        siml = parse(config)
        siml.set_netns()

    def delete(self, config: str = None):
        siml = parse(config)
        siml.delete()

    def run(self, config: str = None):
        siml = parse(config)
        siml.run()

    def up(self, config: str = None):
        siml = parse(config)
        siml.up()

    def down(self, config: str = None):
        siml = parse(config)
        siml.down()

    def exec(self, ns: str, command='bash'):
        exec_command(ns, command)

    def list(self, config: str = None):
        siml = parse(config)
        siml.list()

    def validate(self, config: str = None):
        siml = parse(config)
        siml.show()

    def check_netns(self):
        name = get_netns_name()
        print(name)

    def register_netns_id(self, ns_name):
        print('[info] register netns id %s' % ns_name)
        register_netns_id(ns_name)


def main():
    fire.Fire(NetNsSiml)
