# from parser.parser import parse
import fire
from parser.parser import parse

class NetNsSiml(object):

    def create(self, config: str = None):
        print("create command ", config)
        siml = parse(config)
        print(siml)
        siml.create()

    def init(self, config: str = None):
        print("init command")

    def delete(self, config: str = None):
        print("delete command")
        siml = parse(config)
        siml.delete()
    
    def list(self):
        print("list command")


if __name__ == "__main__":
    fire.Fire(NetNsSiml)
