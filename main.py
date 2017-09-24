import time
import random
import names
from Unit import *


class Fight():
    def __init__(self, heroes):
        self.heroes  = heroes
        self.baddies = []
        self.createbaddies()
        self.prepareforbattle()
        self.bad_get()
        self.turn = 0

    def bad_get(self):
        self.heroes[0].get_target(self.baddies[0])
        self.baddies[0].get_target(self.heroes[0])
        self.baddies[1].get_target(self.heroes[0])


    def createbaddies(self):

        for x in range(2):
            self.baddies.append(Unit(random.choice(names.Baddienames), 10, 1, 4))

    def prepareforbattle(self):
        for unit in self.heroes:
            unit.cur_fight = self
        for unit in self.baddies:
            unit.cur_fight = self

    def loss(self):
        print("Thats a loss.. Remaining units:")
        for unit in self.baddies:
            print(unit)


    def victory(self):
        print("\n\nVictory!! \nVictors of this battle:")

        for unit in self.heroes:
            print(unit)

    def endofbattle(self):
        if len(self.baddies) == 0:
            self.victory()

        elif len(self.heroes) == 0:
            self.loss()
            

    def tick(self):

        

        while len(self.heroes) > 0 and len(self.baddies) > 0:
            print("\n\t\tTURN %d" % self.turn)
            self.turn += 1
            for unit in self.heroes:
                if not unit.target:
                    unit.search_target(self.baddies)
                unit.tick()
                if unit.alive == False:
                    self.heroes.remove(unit)

            for unit in self.baddies:
                if not unit.target:
                    unit.search_target()
                unit.tick()
                if unit.alive == False:
                    self.baddies.remove(unit)

            time.sleep(1)

        self.endofbattle()




class Maingame():

    def __init__(self):
        self.heroes = []
        self.baddies = []
        self.teamlist = []

        self.createheroes()
        self.run()

    def createheroes(self):

        self.heroes.append(Unit("Stornk", 10, 5, 4))

    def run(self):
        fight = Fight(self.heroes)
        fight.tick()




if __name__ == '__main__':
    Maingame()