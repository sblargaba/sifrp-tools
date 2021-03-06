import random
import yaml
import abc

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
    """Class to be extended for specific use depending on the particular type of character needing to be represented
    
    It provides a basic initialization and a few helper methods; it also defines abstract methods needing implementation
    in subclasses
    
    Args:
        name (str): The name of the character.
        age (int): When generating a random character set the age.
        data (dict): A dictionary containing a character data.
    """
    def __init__(self, name="Ser Example", data=None, age=None):
        self.is_legal = True
        self.name = name
        if data:
            self.data = data
            self.ageVal = age if age else age_to_val(data["Background"]["Age"])
            self.exp = data["Abilities"]["Experience"]
        else:
            self.ageVal = age_to_val(age) if age is not None else set_age()
            self.data = {
                "Armor": None,
                "Arms": None,
                "Abilities": self.generate_abilities(),
                "Attributes": self.generate_attributes(),
                "Derived": self.calculate_derived()
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

    def calculate_derived(self):
        """Calculate the derived statistics (Combat and Intrigue Defense, Health, Composture)

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

    @abc.abstractmethod
    def generate_attributes(self):
        """Generates the available destiny points, max benefits and min drawbacks.

        Returns:
            dict: A dictionary containing 
                    - Information about the available options regarding attributes.
                    - Handbook pages to aid the choice of attributes. 
        """

    @abc.abstractmethod
    def generate_abilities(self):
        """Generate the abilities of the character
        
        Returns:
            dict: A dictionary containing 
                    - Information about the available options regarding abilities.
                    - Handbook pages to aid in the choice of abilities. 
        """

    def validate(self):
        """Check if the character has allowed values for abilities, attributes and derived statistics
        
        Returns:
            bool: True if the character can be considered legal
        """
        self.validate_abilities()
        self.validate_attributes()
        self.validate_derived()
        return self.is_legal

    def validate_derived(self):
        """Checks if the derived statistics of the character are correct
        
        The method updates the ``is_legal`` class attribute if needed
        """
        derived = self.calculate_derived()
        if derived != self.data["Derived"]:
            self.is_legal = False
            print("Calculated derived statistics is {} instead of {}".format(derived, self.data["Derived"]))
            return False
        return True

    @abc.abstractmethod
    def validate_abilities(self):
        """Check if the abilities of the character adhere to the rules
        
        The method updates the ``is_legal`` class attribute if needed"""

    @abc.abstractmethod
    def validate_attributes(self):
        """Check if the attributes of the character adhere to the rules
        
        The method updates the ``is_legal`` class attribute if needed"""


