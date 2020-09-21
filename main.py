from parser.parser import parse

def main():
    s = parse("./examples/example.yml")
    s.create()
    s.list()


if __name__ == "__main__":
    main()
