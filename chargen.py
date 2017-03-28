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
    if age:
        if 0 <= age < 10:
            age = 0
        elif 10 <= age < 14:
            age = 1
        elif 14 <= age < 18:
            age = 2
        elif 18 <= age < 30:
            age = 3
        elif 30 <= age < 50:
            age = 4
        elif 50 <= age < 70:
            age = 5
        elif 70 <= age < 80:
            age = 6
        elif 80 <= age:
            age = 7
    return age


class Character:
    status = [
        "House retainer, common hedge knight, freeman",
        "Sworn sword, guardsman, squire",
        "Ranking member of household, maester, junior septon, landed knight, noble bastard",
        "Banner lord, ward, courtier, septon, advisor",
        "Lord of the house, heir, lady, offspring"
    ]
    goals = [
        "Enlightenment", "Skill, mastery in a specific ability",
        "Fame", "Knowledge", "Love", "Power", "Security", "Revenge", "Wealth",
        "Justice", "Good"
    ]
    motivations = [
        "Charity", "Duty", "Fear", "Greed", "Love", "Hatred",
        "Lust", "Peace", "Stability", "Excellence", "Madness"
    ]
    virtues = [
        "Charitable", "Chaste", "Courageous", "Devoted", "Honest",
        "Humble", "Just", "Magnanimous", "Merciful", "Pious", "Wise"
    ]
    vices = [
        "Ambitious/Grasping", "Arrogant", "Avaricious", "Cowardly",
        "Cruel", "Foolish", "Licentious", "Miserly", "Prejudiced", "Scheming",
        "Wrathful"
    ]
    backgrounds = [
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

    def __init__(self, data=None):
        if data:
            self.data = data
            self.ageVal = age_to_val(data["Background"]["Age"])
            self.statusVal = self.get_rank("Status")
        else:
            self.ageVal = None
            self.statusVal = None
            self.data = {
                "Armor": None,
                "Arms": None,
                "Background": self.generate_bg(),
                "Abilities": self.generate_abilities(),
                "Attributes": self.generate_attributes()
            }

    def generate_bg(self, age=None, status=None, goal=None, motivation=None, virtue=None, vice=None, backgrounds=None):
        self.ageVal = age_to_val(age) if age else set_age()
        self.statusVal = status if status else set_status()
        bg = {
            "Age": str(self.ages[self.ageVal]), "Status": str(self.status[self.statusVal]),
            "Goal": goal if goal else self.goals[roller(2) - 2],
            "Motivation": motivation if motivation else self.motivations[roller(2) - 2],
            "Virtue": virtue if virtue else self.virtues[roller(2) - 2],
            "Vice": vice if vice else self.vices[roller(2) - 2],
            "Events": backgrounds if backgrounds else self.generate_backgrounds()
        }
        return bg

    def generate_abilities(self):
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
        attributes.update(self.get_derivated())
        return attributes

    def get_rank(self, ability):
        try:
            a = self.data["Abilities"][ability]
        except (KeyError, AttributeError):
            return 2

        if type(a) == int:
            return a
        else:
            return a["Stat"]

    def get_derivated(self):
        der = {
            "Combat Defense": self.get_rank("Agility") + self.get_rank("Athletics") + self.get_rank("Awareness"),
            "Health": 3 * self.get_rank("Endurance"),
            "Intrigue Defense": self.get_rank("Cunning") + self.get_rank("Status") + self.get_rank("Awareness"),
            "Composture": 3 * self.get_rank("Will")
        }
        return der

    # def __str__(self):
    #     res = "Age:\t\t" + str(self.ages[self.ageVal])
    #     res += "\nStatus:\t\t" + str(self.status[self.statusVal])
    #     res += "\nGoal:\t\t" + self.goal
    #     res += "\nMotivation:\t" + self.motivation
    #     res += "\nVirtue:\t" + self.virtue
    #     res += "\nVice:\t\t" + self.vice
    #     res += "\nEvents:"
    #     for bg in self.backgrounds:
    #         res += "\n\t" + bg
    #     return res

    def get_dp(self):
        return 7 - self.ageVal

    def generate_backgrounds(self):
        events = []
        while len(events) < self.ageVal:
            event = roller(2) - 2
            if self.backgrounds[event] not in events:
                events.append(self.backgrounds[event])
        return events

    def validate(self):
        self.validate_abilities()
        self.validate_attributes()

    def get_flaws(self):
        try:
            return self.data["Attributes"]["Drawbacks"]["Flaws"]
        except KeyError:
            return []

    def get_traits_n(self, trait):
        total = 0
        for db in self.data["Attributes"][trait].values():
            if type(db) is list:
                total += len(db)
            else:
                total += 1
        return total

    def validate_abilities(self):
        total = self.exp_points[self.ageVal]
        flaws = self.get_flaws()
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
        print("Experience: starting {}, left: {}".format(self.exp_points[self.ageVal], total))

    def validate_attributes(self):
        db_n = self.get_traits_n("Drawbacks")
        if db_n < self.min_drawbacks[self.ageVal]:
            print("{} Drawbacks, expected min {}".format(
                db_n,
                self.min_drawbacks[self.ageVal]
            ))
        ben_n = self.get_traits_n("Benefits")
        if ben_n > self.max_benefits[self.ageVal]:
            print("{} Benefits, expected max {}".format(
                ben_n,
                self.max_benefits[self.ageVal]
            ))

        db_bought = db_n - self.min_drawbacks[self.ageVal]

        dp = self.get_dp() - ben_n + db_bought
        print("Destiny points: {} initial - {} benefits + {} drawbacks = {}".format(
            self.get_dp(), ben_n, db_bought, dp
        ))

        self.data["Attributes"].update(self.get_derivated())


parser = ArgumentParser()
parser.add_argument("--file", default=None)
parser.add_argument("--age", default=None, type=int)
args = parser.parse_args()

if args.age:
    args.age = age_to_val(args.age)

if args.file:
    with open(args.file) as f:
        raw = load(f)
    name, data = raw.popitem()
    char = Character(data)
    char.validate()
    raw = {name: char.data}
    with open("/tmp/test.yml", "w") as f:
        f.write(dump(raw, default_flow_style=False))
else:
    char = Character()
    print(dump(char.data, default_flow_style=False))

