import unittest
from units import *

# test_units.py
# Unit-testing of the different classes and functions inside units.py

class Herotest(unittest.TestCase):

    def setUp(self):
        self.guy1 = Unit("Testhero", 10, 4, 1)
        self.guy2 = Unit("Testbaddie", 20, 4, 1)


    def test_get_experience(self):
        self.assertEqual(self.guy1.exp, 0)
        self.guy1.get_experience(5)
        self.assertEqual(self.guy1.exp, 5)

    def test_level_up(self):
        self.assertEqual(self.guy1.lvl, 1)
        self.guy1.level_up()
        self.assertEqual(self.guy1.lvl, 2)

    def test_rest(self):
        self.guy1.hp = 1
        self.guy1.rest()
        self.assertEqual(self.guy1.hp, self.guy1.maxhp)

    def test_attack(self):
        self.guy1.attack(self.guy2)
        self.assertLess(self.guy2.hp, self.guy2.maxhp)

    def test_search_target(self):
        badparty = Party()
        badparty.join_party(self.guy2)
        self.guy1.search_target(badparty)
        self.assertEqual(self.guy1.target, self.guy2)

if __name__ == '__main__':
    unittest.main()