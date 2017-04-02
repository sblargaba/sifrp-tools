import argparse

import yaml

from chargen import classes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates a character.\n If a character is supplied as a file, validate the character"
    )
    parser.add_argument("-f", "--file", default=None, help="A properly formatted YAML file containing a character")
    parser.add_argument("-a", "--age", default=None, type=int, help="The age of the character to be created")
    parser.add_argument("-n", "--name", default="Ser Example", help="The name of the character to be created")

    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            raw = yaml.load(f)
        name, data = raw.popitem()
        char = classes.PlayerCharacter(name=name, data=data)
        char.validate()
        raw = {name: char.data}
        with open("/tmp/test.yml", "w") as f:
            f.write(str(char))
    else:
        char = classes.PlayerCharacter(age=args.age)
        print(char)
        char = classes.NCTier3(age=args.age)
        print(char)
        char = classes.NCTier2(age=args.age)
        print(char)
        char = classes.NCTier1(age=args.age)
        print(char)
