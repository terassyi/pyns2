# from parser.parser import parse
import fire
from parser.parser import parse
from netns.exec import exec_command

class NetNsSiml(object):

    def create(self, config: str = None):
        print("create command ", config)
        siml = parse(config)
        siml.create()

    def set(self, config: str = None):
        siml = parse(config)
        siml.set_netns()
        
    def init(self, config: str = None):
        print("init command")

    def delete(self, config: str = None):
        print("delete command")
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

    def exec(self, ns: str, command= 'bash'):
        exec_command(ns, command)
    
    def list(self, config: str = None):
        print("list command")
        siml = parse(config)
        siml.list()

    

    def status(self, config: str = None):
        pass


if __name__ == "__main__":
    fire.Fire(NetNsSiml)
