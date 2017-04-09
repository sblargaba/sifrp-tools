import unittest
from chargen.chargen import PlayerCharacter


class GenerationTest(unittest.TestCase):
    PC = PlayerCharacter()

    def test_specialties_generation(self):
        """Check if the specialty points are correct for the age of the character"""
        result = self.PC.data["Abilities"]["Specialties points"]
        expected = self.PC.spec_points[self.PC.ageVal]
        self.assertEqual(expected, result)

    def test_abilities_generation(self):
        """Number of ability points should be correct for the age of the character"""
        result = self.PC.data["Abilities"]["Abilities Points"]
        status_exp = (self.PC.get_rank("Status") - 2) * 30 - 20
        expected = self.PC.ab_points[self.PC.ageVal] - status_exp
        self.assertEqual(expected, result)

    def test_benefit_generation(self):
        """Value of `maximum benefits` should be correct for the age of the character"""
        self.assertEqual(self.PC.max_benefits[self.PC.ageVal], self.PC.data["Attributes"]["Benefits"]["max"])

    def test_drawbacks_generation(self):
        """Value of `minimum drawbacks` shouold be correct for the age of the character"""
        self.assertEqual(self.PC.min_drawbacks[self.PC.ageVal], self.PC.data["Attributes"]["Drawbacks"]["min"])

    def test_dp_generation(self):
        """Number of destiny points should be correct for the age of the character"""
        dp = 7 - self.PC.ageVal
        self.assertEqual(dp, self.PC.dp)
        self.assertEqual(dp, self.PC.data["Attributes"]["Destiny Points"])

    def test_bg_event_generation(self):
        """Number of background events should be correct for the age of the character"""
        self.assertEqual(self.PC.ageVal, len(self.PC.data["Background"]["Events"]))

    if __name__ == '__main__':
        unittest.main()
