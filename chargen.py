#!/bin/env python

from random import randint
from argparse import ArgumentParser
from yaml import load, dump


def roller(n):
    """Rolls nd6"""
    res = 0
    for i in range(n):
        res += randint(1, 6)
    return res


def set_status():
    roll = roller(2)
    if roll == 2:
        return 0
    elif roll <= 4:
        return 1
    elif roll <= 9:
        return 2
    elif roll <= 11:
        return 3
    elif roll <= 12:
        return 4


def set_age(roll=roller(3)):
    if roll == 3:
        return 0
    elif roll <= 4:
        return 1
    elif roll <= 5:
        return 2
    elif roll <= 7:
        return 3
    elif roll <= 12:
        return 4
    elif roll <= 16:
        return 5
    elif roll <= 17:
        return 6
    elif roll <= 18:
        return 7


def age_to_val(age):
    if 0 <= age < 10:
        return 0
    elif 10 <= age < 14:
        return 1
    elif 14 <= age < 18:
        return 2
    elif 18 <= age < 30:
        return 3
    elif 30 <= age < 50:
        return 4
    elif 50 <= age < 70:
        return 5
    elif 70 <= age < 80:
        return 6
    elif 80 <= age:
        return 7


class Character:
    _status = [
        "House retainer, common hedge knight, freeman",
        "Sworn sword, guardsman, squire",
        "Ranking member of household, maester, junior septon, landed knight, noble bastard",
        "Banner lord, ward, courtier, septon, advisor",
        "Lord of the house, heir, lady, offspring"
    ]
    _goals = [
        "Enlightenment", "Skill, mastery in a specific ability",
        "Fame", "Knowledge", "Love", "Power", "Security", "Revenge", "Wealth",
        "Justice", "Good"
    ]
    _motivations = [
        "Charity", "Duty", "Fear", "Greed", "Love", "Hatred",
        "Lust", "Peace", "Stability", "Excellence", "Madness"
    ]
    _virtues = [
        "Charitable", "Chaste", "Courageous", "Devoted", "Honest",
        "Humble", "Just", "Magnanimous", "Merciful", "Pious", "Wise"
    ]
    _vices = [
        "Ambitious/Grasping", "Arrogant", "Avaricious", "Cowardly",
        "Cruel", "Foolish", "Licentious", "Miserly", "Prejudiced", "Scheming",
        "Wrathful"
    ]
    _backgrounds = [
        "You served another house (page, sworn sword).",
        "You had a torrid love affair.",
        "You fought or were involved in a battle.",
        "You were kidnapped and escaped, were ransomed, or rescued.",
        "You traveled across the narrow sea for a time.",
        "You achieved a significant deed, maybe saving the life of your lord, "
        "killed a giant boar, and so on.",
        "You kept the company of a famous individual.",
        "You were present at a significant tournament (competing or watching).",
        "You were involved in a villainous scandal.",
        "You were falsely accused of wrongdoing.",
        "You were held hostage by another house as a ward or prisoner."
    ]
    ages = [
        ("0-9", "Youth"),
        ("10-13", "Adolescent"),
        ("14-18", "Young Adult"),
        ("18-30", "Adult"),
        ("30-50", "Middle Age"),
        ("50-70", "Old"),
        ("70-80", "Very Old"),
        ("80+", "Venerable")
    ]
    exp_points = [120, 150, 180, 210, 240, 270, 330, 360]
    spec_points = [40, 40, 60, 80, 100, 160, 200, 240]
    min_drawbacks = [0, 0, 0, 1, 1, 2, 3, 4]
    max_benefits = [3, 3, 3, 3, 3, 2, 1, 0]
    max_rank = [4, 4, 5, 7, 6, 5, 5, 5]

    def __init__(self, name, data=None, age=None):
        """
        Args:
            name (str): The name of the character.
            data (dict): A dictionary containing a character data.
            age (int): When generating a random character set the age.
        """
        self.name = name
        if data:
            self.data = data
            self.ageVal = age_to_val(data["Background"]["Age"])
            self.statusVal = self.get_rank("Status")
        else:
            self.ageVal = age_to_val(age) if age is not None else set_age()
            self.statusVal = set_status()
            self.data = {
                "Armor": None,
                "Arms": None,
                "Background": self.generate_bg(),
                "Abilities": self.generate_abilities(),
                "Attributes": self.generate_attributes()
            }

    def __str__(self):
        out = {self.name: self.data}
        return dump(out, default_flow_style=False)

    def get_rank(self, ability):
        """Get the rank of a specified ability

        Args:
            ability (str): The ability to retrieve

        Returns:
            int: the ablity rank. Defaults to 2 if the ability is not listed

        """
        try:
            a = self.data["Abilities"][ability]
        except (KeyError, AttributeError):
            return 2

        if type(a) == int:
            return a
        else:
            return a["Stat"]

    def get_derived(self):
        """Calculate the derived statistics (Combat/Intrigue Defense, Health, Composture)

        Returns:
            dict: A dictionary containig the derived statistics
        """
        der = {
            "Combat Defense": self.get_rank("Agility") + self.get_rank("Athletics") + self.get_rank("Awareness"),
            "Health": 3 * self.get_rank("Endurance"),
            "Intrigue Defense": self.get_rank("Cunning") + self.get_rank("Status") + self.get_rank("Awareness"),
            "Composture": 3 * self.get_rank("Will")
        }
        return der

    def get_dp(self):
        """Calculate the destiny points"""
        return 7 - self.ageVal

    def get_traits_n(self, trait):
        """Get the number of traits

        Args:
            trait (str): Defines the traits to check, either "Drawbacks" or "Benefit"

        Returns:
            int: The number of traits 
        """
        total = 0
        for db in self.data["Attributes"][trait].values():
            if type(db) is list:
                total += len(db)
            else:
                total += 1
        return total

    def generate_bg(self):
        bg = {
            "Age": str(self.ages[self.ageVal]), "Status": str(self._status[self.statusVal]),
            "Goal": self._goals[roller(2) - 2],
            "Motivation": self._motivations[roller(2) - 2],
            "Virtue": self._virtues[roller(2) - 2],
            "Vice": self._vices[roller(2) - 2],
            "Events": self.generate_events()
        }
        return bg

    def generate_events(self):
        """Generate background events

        Returns:
            list of str: A list of all the events
        """
        events = []
        while len(events) < self.ageVal:
            event = roller(2) - 2
            if self._backgrounds[event] not in events:
                events.append(self._backgrounds[event])
        return events

    def generate_abilities(self):
        """Generate the ability and specialities points available to spend and handbook pages"""
        status_exp = self.statusVal * 30 - 20

        abilities = {
            "Abilities List": "p56",
            "Abilities Costs": "p50",
            "Abilities Points": self.exp_points[self.ageVal] - status_exp,
            "Status": {
              "Stat": self.statusVal + 2,
              "Specialties points": self.spec_points[self.ageVal]
            }
        }
        return abilities

    def generate_attributes(self):
        """Generates the available destiny points, max benefits and min drawbacks. Update the derived statistics"""
        attributes = {
            "Destiny Points": self.get_dp(),
            "Benefits": {
                "max": self.max_benefits[self.ageVal],
                "list": "p73"
            },
            "Drawbacks": {
                "min": self.min_drawbacks[self.ageVal],
                "list": "p94"
            }
        }
        attributes.update(self.get_derived())
        return attributes

    def validate(self):
        """Checks if the character ha the correct values and updates the derived statistics"""
        legal = self.validate_abilities() and self.validate_attributes()
        self.data["Attributes"].update(self.get_derived())
        return legal

    def validate_abilities(self):
        """Check if the abilities are correct.
        
        For each ability the method checks the rank does not exceeds the maximum allowed for the caracter.
        The method also calculates the amount of experience needed for the character's abilities.
        The output of the check is printed on the screen; flaws are taken into consideration when perofrming checks.
        
        Returns:
            bool: True if none of the checks fails
        """
        legal = True
        total = self.exp_points[self.ageVal]
        try:
            flaws = self.data["Attributes"]["Drawbacks"]["Flaws"]
        except KeyError:
            flaws = []

        for ab in self.data["Abilities"]:
            rank = self.get_rank(ab)
            if ab in flaws:
                rank += 1
            if rank > 2:
                print("{}: {} exp {}".format(ab, rank, (rank - 2) * 30 - 20))
                total -= (rank - 2) * 30 - 20
            if rank > self.max_rank[self.ageVal]:
                print("{} at {} exceeds the maximum value of {} for the age".format(
                    ab, rank, self.max_rank[self.ageVal]
                ))
                legal = False
        print("Experience: starting {}, left: {}".format(self.exp_points[self.ageVal], total))
        if total < 0:
            legal = False

        return legal

    def validate_attributes(self):
        """Checks attributes and destiny points
        
        The methods checks if the character has at least the required number of drawbacks and less the maximum
        benefits allowed
        
        Returns:
            bool: True if none of the checks fails        
        """
        legal = True
        db_n = self.get_traits_n("Drawbacks")
        if db_n < self.min_drawbacks[self.ageVal]:
            print("{} Drawbacks, expected min {}".format(
                db_n,
                self.min_drawbacks[self.ageVal]
            ))
            legal = False
        ben_n = self.get_traits_n("Benefits")
        if ben_n > self.max_benefits[self.ageVal]:
            print("{} Benefits, expected max {}".format(
                ben_n,
                self.max_benefits[self.ageVal]
            ))
            legal = False

        db_bought = db_n - self.min_drawbacks[self.ageVal]

        dp = self.get_dp() - ben_n + db_bought
        print("Destiny points: {} initial - {} benefits + {} drawbacks = {}".format(
            self.get_dp(), ben_n, db_bought, dp
        ))
        if dp < 0:
            legal = False

        return legal


parser = ArgumentParser(
    description="Generates a character.\n If a character is supplied as a file, validate the character"
)
parser.add_argument("-f", "--file", default=None, help="A properly formatted YAML file containing a character")
parser.add_argument("-a", "--age", default=None, type=int, help="The age of the character to be created")
parser.add_argument("-n", "--name", default="Ser Example", help="The name of the character to be created")

args = parser.parse_args()

if args.file:
    with open(args.file) as f:
        raw = load(f)
    name, data = raw.popitem()
    char = Character(name=name, data=data)
    char.validate()
    raw = {name: char.data}
    with open("/tmp/test.yml", "w") as f:
        f.write(str(char))
else:
    char = Character(name=args.name, age=args.age)
    print(char)

