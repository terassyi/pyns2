import yaml
from pyns2.siml.siml import Siml

def parse(path: str):
    with open(path, 'r') as yml:
        config = yaml.load(yml, Loader=yaml.SafeLoader)
        s = Siml(config)
        return s


if __name__ == '__main__':
    s = parse("../../examples/example.yml")
    print(s.netns[0])

