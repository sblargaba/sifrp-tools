#!/bin/env python

import random
import yaml
import math

statuses = [
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


def roller(n):
    """Rolls nd6"""
    res = 0
    for i in range(n):
        res += random.randint(1, 6)
    return res


def set_status():
    roll = roller(2)
    if roll == 2:
        return 2
    elif roll <= 4:
        return 3
    elif roll <= 9:
        return 4
    elif roll <= 11:
        return 5
    elif roll <= 12:
        return 6


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
    """The Character class
    
    This class represents a character and provides methods for character generation and validation.
    On class creation if a dictionary with the character data is not provided, the informations are randomly generated.
    
    **Character Generation**
    
    The following data is genearated randomly:

        - Age (can be overridden providing the proper argument on class creation)
        - Status
        - Goal
        - Motivation
        - Virtue
        - Vice
        - Events
    
    The following data is calculated based on the age of the character:
    
        - Ability points (The points necesary to buy Status are already subtracted from this)
        - Specialty points
        - Minumum drawbacks
        - Maximum benefits
    
    Pages of the core rulebook are are included for convenience.
    
    Args:
        name (str): The name of the character.
        age (int): When generating a random character set the age.
        data (dict): A dictionary containing a character data. Example::
    
            data = {
                "Abilities": {
                    "Experience": (int)
                    ability_name: ability_rank (int),
                    ability_name: {
                        "Stat": ability_rank (int),
                        specialty_name: specialty_rank (int)
                    }
                },
                "Attributes": {
                    "Destiny Points": (int),
                    "Benefits": {
                        benefit_name: benefit_description (str),
                        benefit_name: [
                            benefit_application (str)
                        ]
                    },
                    "Drawbacks": {
                        drawback_name: drawback_description (str),
                        drawback_name: [
                            drawback_application (str)
                        ]
                    "Combat Defense": (int)
                    "Health": (int)
                    "Intrigue Defense": (int)
                    "Composture": (int)
                    }
                },
                "Background":{
                    "Age": (int),
                    "Goal": (str),
                    "Motivation": (str),
                    "Virtue": (str),
                    "Vice": (str),
                    "Events": [
                        event (str)
                    ]
                },
                "Armor": (list),
                "Arms": (list)
            }
    """

    def __init__(self, name="Ser Example", data=None, age=None):
        self.legal = True
        self.name = name
        if data:
            self.data = data
            self.ageVal = age_to_val(data["Background"]["Age"])
            self.exp = data["Abillities"]["Experience"]
        else:
            self.ageVal = age_to_val(age) if age is not None else set_age()
            self.data = {
                "Armor": None,
                "Arms": None,
                "Abilities": self.generate_abilities(),
                "Attributes": self.generate_attributes()
            }

    def __str__(self):
        out = {self.name: self.data}
        return yaml.dump(out, default_flow_style=False)

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

    def generate_attributes(self):
        """Generates the available destiny points, max benefits and min drawbacks. Update the derived statistics"""
        return self.get_derived()

    def generate_abilities(self):
        """To be overridden by child classess"""
        pass

    def validate(self):
        """Checks if the character ha the correct values and updates the derived statistics"""
        self.validate_abilities()
        self.validate_attributes()
        self.data["Attributes"].update(self.get_derived())
        return self.legal

    def validate_specialties(self, ability):
        pass

    def validate_abilities(self):
        pass

    def validate_attributes(self):
        pass


class PlayerCharacter(Character):
    ab_points = [120, 150, 180, 210, 240, 270, 330, 360]
    spec_points = [40, 40, 60, 80, 100, 160, 200, 240]
    min_drawbacks = [0, 0, 0, 1, 1, 2, 3, 4]
    max_benefits = [3, 3, 3, 3, 3, 2, 1, 0]
    ab_max_rank = [4, 4, 5, 7, 6, 5, 5, 5]

    def __init__(self, name="Ser Example", data=None, age=None):
        super().__init__(name, data, age)
        self.data["Backgrounds"] = self.generate_bg()

    def generate_abilities(self):
        """Generate the ability and specialities points available to spend. Include handbook pages"""
        status = set_status()
        status_exp = (status - 2) * 30 - 20
        abilities = {
            "Abilities List": "p56",
            "Abilities Costs": "p50",
            "Specialties Costs": "p51",
            "Abilities Points": self.ab_points[self.ageVal] - status_exp,
            "Specialties points": self.spec_points[self.ageVal],
            "Experience": 0,
            "Status": status
        }
        return abilities

    def generate_attributes(self):
        """Generates the available destiny points, max benefits and min drawbacks. Update the derived statistics"""
        attributes = {
            "Destiny Points": self.dp,
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

    def generate_bg(self):
        """Random generation of background informations"""
        status = self.data["Abilities"]["Status"]
        bg = {
            "Age": str(ages[self.ageVal]),
            "Status": statuses[status - 2],
            "Goal": goals[roller(2) - 2],
            "Motivation": motivations[roller(2) - 2],
            "Virtue": virtues[roller(2) - 2],
            "Vice": vices[roller(2) - 2],
            "Events": self.generate_events()
        }
        return bg

    def generate_events(self):
        """Generate a list of background events"""
        events = []
        while len(events) < self.ageVal:
            event = roller(2) - 2
            if backgrounds[event] not in events:
                events.append(backgrounds[event])
        return events

    @property
    def dp(self):
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

    def validate_abilities(self):
        """Check if the abilities are correct.

        For each ability the method checks the rank does not exceeds the maximum allowed for the caracter.
        The method also calculates the amount of experience needed for the character's abilities.
        The output of the check is printed on the screen; flaws are taken into consideration when perofrming checks.

        Returns:
            bool: True if none of the checks fails
        """
        legal = True
        ab_total = self.ab_points[self.ageVal]
        spec_total = self.spec_points[self.ageVal]
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
                ab_total -= (rank - 2) * 30 - 20
            if rank > self.ab_max_rank[self.ageVal]:
                print("{} at {} exceeds the maximum value of {} for the age".format(
                    ab, rank, self.ab_max_rank[self.ageVal]
                ))
            sp_legal, sp = self.validate_specialties(ab)
            if not sp_legal:
                legal = False
            spec_total -= sp

        print("Ability points: starting {}, left: {}".format(self.ab_points[self.ageVal], ab_total))
        print("Specialty points: starting {}, left: {}".format(self.spec_points[self.ageVal], spec_total))
        if ab_total < 0 or spec_total < 0:
            legal = False

        if not legal:
            self.legal = False
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

        dp = self.dp - ben_n + db_bought
        print("Destiny points: {} initial - {} benefits + {} drawbacks = {}".format(
            self.dp, ben_n, db_bought, dp
        ))
        if dp < 0:
            legal = False

        if not legal:
            self.legal = False
        return legal

    def validate_specialties(self, ability):
        legal = True
        total = 0
        if type(ability) == dict:
            for spec, val in ability:
                if spec is not "Stat":
                    total += val * 10
                    rank = self.get_rank(ability)
                    if val > rank:
                        print("{} at {} exceeds the {} rank of {}".format(spec, val, ability, rank))
                        legal = False
        return legal, total


class NCTier1(PlayerCharacter):
    def __init__(self, name="Ser Example", data=None, age=None):
        super().__init__(name, data, age)

    def generate_abilities(self):
        abilities = super().generate_abilities()
        abilities["Experience"] = roller(1) * 10
        return abilities


class NCTier2(Character):
    def __init__(self, name="Ser Example", data=None, age=None):
        super().__init__(name, data, age)

    def generate_abilities(self):
        """Generate the ability and specialities points available to spend. Include handbook pages"""
        status = set_status()
        abilities = {
                "Abilities List": "p56",
                "1 ability": 5,
                "2 ablities": 4,
                "4 abilities": 3,
                "4 specialties": "half the ability rank (rounded down)",
                "Status": status
            }
        return abilities

    def validate_specialties(self, ability):
        legal = True
        total = 0
        if type(ability) == dict:
            for spec, val in ability:
                if spec is not "Stat":
                    total += 1
                    rank = self.get_rank(ability)
                    if val != math.floor(rank):
                        print("{} at {} exceeds half of the {} rank of {}".format(spec, val, ability, rank))
                        legal = False
        return legal, total

    def validate_abilities(self):
        legal = True
        ab_checklist = [5, 4, 4, 3, 3, 3, 3]
        spec_total = 4

        for ab in self.data["Abilities"]:
            rank = self.get_rank(ab)
            try:
                ab_checklist.remove(rank)
            except ValueError:
                print("{} rank {} is not in checklist {}".format(ab, rank, ab_checklist))
                legal = False
            sp_legal, sp = self.validate_specialties(ab)
            if not sp_legal:
                legal = False
            spec_total -= sp

        print("Abilities left: {}".format(ab_checklist))
        print("Specialties left: {}".format(spec_total))
        if spec_total < 0:
            legal = False

        if not legal:
            self.legal = False
        return legal


class NCTier3(Character):
    def __init__(self, name="Ser Example", data=None, age=None):
        super().__init__(name, data, age)

    def generate_abilities(self):
        """Generate the ability and specialities points available to spend. Include handbook pages"""
        status = set_status()
        abilities = {
            "Abilities List": "p56",
            "1 or 2 abilities": "3 or 4",
            "if first ability is 4 chose another two": 3,
            "2 or 3 specialties": 1,
            "Status": status
        }
        return abilities

    def validate_specialties(self, ability):
        legal = True
        total = 0
        if type(ability) == dict:
            for spec, val in ability:
                if spec is not "Stat":
                    if val != 1:
                        print("{} should be 1, is {}".format(spec, val))
                        legal = False
        return legal, total

    def validate_abilities(self):
        legal = True
        spec_total = 3
        ab_checklist = []
        ab_checklist_allowed = [
            [3],
            [3, 3],
            [3, 3, 3, 4],
            [3, 3, 4, 4]
        ]

        for ab in self.data["Abilities"]:
            rank = self.get_rank(ab)
            ab_checklist.append(rank)
            sp_legal, sp = self.validate_specialties(ab)
            if not sp_legal:
                legal = False
            spec_total -= sp

        print("Abilities spent: {}".format(ab_checklist))
        print("Specialties left: {}".format(spec_total))
        if spec_total < 0 or ab_checklist in ab_checklist_allowed:
            legal = False

        if not legal:
            self.legal = False
        return legal

