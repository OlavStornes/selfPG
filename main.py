import time
import random
from common import *
from units import *


class Fight():
    def __init__(self, heroes, difficulty):
        self.heroes  = heroes
        self.baddies = []
        self.difficulty = difficulty
        self.createbaddies()
        self.prepareforbattle()
        self.turn = 0

    def bad_get(self):
        self.heroes[0].get_target(self.baddies[0])
        self.baddies[0].get_target(self.heroes[0])
        self.baddies[1].get_target(self.heroes[0])


    def createbaddies(self):
        #TODO: MORE VARIATION
        for x in range(self.difficulty):
            self.baddies.append(Unit(random.choice(Baddienames), 10, 1, 4))

    def prepareforbattle(self):
        print("A FIGHT APPEARS!\n\n")
        for unit in self.heroes:
            print(unit)
            unit.cur_fight = self
        for unit in self.baddies:
            print(unit)
            unit.cur_fight = self

        time.sleep(3)


    def loss(self):
        print("Thats a loss.. Remaining units:")
        for unit in self.baddies:
            print(unit)


    def victory(self):
        print("\n\nVictory!! \nVictors of this battle:")

        for unit in self.heroes:
            print(unit)
        for unit in self.heroes:
            unit.rest()

    def endofbattle(self):
        if len(self.baddies) == 0:
            self.victory()

        elif len(self.heroes) == 0:
            self.loss()

    def teamaction(self, teamlist, targetlist):
        #TODO: AVOID LIST INDEX OUT OF RANGE - REMOVED TARGET
        for unit in teamlist:
            if not unit.target:
                unit.search_target(targetlist)
            unit.tick()
            if unit.alive == False:
                teamlist.remove(unit)


    def tick(self):
        while team_alive(self.heroes) and team_alive(self.baddies):
            print("\n\t\tTURN %d" % self.turn)
            self.turn += 1
                    #HERO TURN
            self.teamaction(self.heroes, self.baddies)
                    #BADDIE TURN
            self.teamaction(self.baddies, self.heroes)
            time.sleep(1)

        self.endofbattle()


############################################################################

class Maingame():

    def __init__(self):
        self.heroes = []
        self.baddies = []
        self.teamlist = []

        self.createheroes()
        self.run()

    def createheroes(self):
        #TODO: BETTER HERO-IMPLEMENTATION
        self.heroes.append(Unit("Stornk", 10, 5, 4))



    def run(self):
        for x in range (1, 5):
            fight = Fight(self.heroes, x)
            fight.tick()

            if not team_alive(self.heroes):
                break




if __name__ == '__main__':
    Maingame()