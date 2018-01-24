from common import *

"""Code contains different status ailments, such as buffs, debuffs and other temporary effects"""

class Ailment():
    """General class of an status ailment"""
    def __init__(self, afflicted):
        self.statustype = type(self).__name__
        self.rounds_left = 0
        self.afflicted = afflicted

    def tick(self):
        self.rounds_left -= 1



class Taunt(Ailment):
    """A status where a unit is forced to attack one spesific person"""
    def __init__(self, afflicted, taunted_by):
        Ailment.__init__(self, afflicted)
        self.target = taunted_by
        self.rounds_left = 5

class Bleed(Ailment):
    """Target is losing hp for a set period of rounds"""
    def __init__(self, afflicted):
        Ailment.__init__(afflicted)
        self.rounds_left = 3

    def tick(self):
        self.afflicted.hp -= 10
        self.rounds_left -= 1



TAUNT = Taunt.__name__
