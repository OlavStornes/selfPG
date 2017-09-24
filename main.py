import time
import random
import names
from Unit import *




class Maingame():

    def __init__(self):
        self.heroes = []
        self.baddies = []
        self.teamlist = []

        self.getheroes()
        self.createbaddies()
        self.run()

    def getheroes(self):

        self.heroes.append(Unit("Stornk", 30, 4, 4))


    def createbaddies(self):
        name = random.choice(names.Baddienames)
        self.baddies.append(Unit(name, 10, 1, 4))

    def run(self):
        self.heroes[0].get_target(self.baddies[0])
        self.baddies[0].get_target(self.heroes[0])



        while len(self.heroes) > 0 and len(self.baddies) > 0:
                for unit in self.heroes:
                    unit.tick()
                    if unit.alive == False:
                        self.heroes.remove(unit)

                for unit in self.baddies:
                    unit.tick()
                    if unit.alive == False:
                        self.baddies.remove(unit)
            #time.sleep(1)


if __name__ == '__main__':
    Maingame()