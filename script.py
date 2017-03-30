import argparse
import yaml
import chargen

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates a character.\n If a character is supplied as a file, validate the character"
    )
    parser.add_argument("-f", "--file", default=None, help="A properly formatted YAML file containing a character")
    parser.add_argument("-a", "--age", default=None, type=int, help="The age of the character to be created")
    parser.add_argument("-n", "--name", default=None, help="The name of the character to be created")

    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            raw = yaml.load(f)
        name, data = raw.popitem()
        char = chargen.Character(name=name, data=data)
        char.validate()
        raw = {name: char.data}
        with open("/tmp/test.yml", "w") as f:
            f.write(str(char))
    else:
        if args.name:
            char = chargen.Character(name=args.name, age=args.age)
        else:
            char = chargen.Character(age=args.age)
        print(char)
