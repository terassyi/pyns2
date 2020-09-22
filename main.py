from parser.parser import parse

def main():
    s = parse("./examples/example.yml")
    s.create()
    s.list()

    s.netns[0].interfaces[0].delete()


if __name__ == "__main__":
    main()
