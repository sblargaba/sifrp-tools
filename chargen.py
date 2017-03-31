#!/bin/env python

import random
import yaml

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

exp_points = [120, 150, 180, 210, 240, 270, 330, 360]

spec_points = [40, 40, 60, 80, 100, 160, 200, 240]

min_drawbacks = [0, 0, 0, 1, 1, 2, 3, 4]

max_benefits = [3, 3, 3, 3, 3, 2, 1, 0]

ability_max_rank = [4, 4, 5, 7, 6, 5, 5, 5]


def roller(n):
    """Rolls nd6"""
    res = 0
    for i in range(n):
        res += random.randint(1, 6)
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
        self.name = name
        if data:
            self.data = data
            self.ageVal = age_to_val(data["Background"]["Age"])
        else:
            self.ageVal = age_to_val(age) if age is not None else set_age()
            self.data = {
                "Armor": None,
                "Arms": None,
                "Abilities": self.generate_abilities(),
                "Background": self.generate_bg(),
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

    def generate_abilities(self):
        """Generate the ability and specialities points available to spend and handbook pages"""
        status = set_status()
        status_exp = (status - 2) * 30 - 20
        abilities = {
            "Abilities List": "p56",
            "Abilities Costs": "p50",
            "Abilities Points": exp_points[self.ageVal] - status_exp,
            "Status": {
              "Stat": status,
              "Specialties points": spec_points[self.ageVal]
            }
        }
        return abilities

    def generate_attributes(self):
        """Generates the available destiny points, max benefits and min drawbacks. Update the derived statistics"""
        attributes = {
            "Destiny Points": self.get_dp(),
            "Benefits": {
                "max": max_benefits[self.ageVal],
                "list": "p73"
            },
            "Drawbacks": {
                "min": min_drawbacks[self.ageVal],
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
        total = exp_points[self.ageVal]
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
            if rank > ability_max_rank[self.ageVal]:
                print("{} at {} exceeds the maximum value of {} for the age".format(
                    ab, rank, ability_max_rank[self.ageVal]
                ))
                legal = False
        print("Experience: starting {}, left: {}".format(exp_points[self.ageVal], total))
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
        if db_n < min_drawbacks[self.ageVal]:
            print("{} Drawbacks, expected min {}".format(
                db_n,
                min_drawbacks[self.ageVal]
            ))
            legal = False
        ben_n = self.get_traits_n("Benefits")
        if ben_n > max_benefits[self.ageVal]:
            print("{} Benefits, expected max {}".format(
                ben_n,
                max_benefits[self.ageVal]
            ))
            legal = False

        db_bought = db_n - min_drawbacks[self.ageVal]

        dp = self.get_dp() - ben_n + db_bought
        print("Destiny points: {} initial - {} benefits + {} drawbacks = {}".format(
            self.get_dp(), ben_n, db_bought, dp
        ))
        if dp < 0:
            legal = False

        return legal
