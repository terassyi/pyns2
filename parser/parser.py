import yaml
from siml.siml import Siml

def parse(path: str):
    with open(path, 'r') as yml:
        config = yaml.load(yml)
        s = Siml(config)
        return s


if __name__ == '__main__':
    s = parse("../examples/example.yml")
    print(s.netns[0])

