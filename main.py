import time
import random
from common import *
from units import *


class Fight():
    """Class for fights between two parties"""
    def __init__(self, heroes, difficulty):
        self.heroparty  = heroes
        self.baddieparty = Party()
        self.difficulty = difficulty
        self.createbaddies()

        self.prepareforbattle()
        self.turn = 0


    def createbaddies(self):
        #TODO: MORE VARIATION
        for x in range(self.difficulty):
            self.baddieparty.join_party(Unit(random.choice(Baddienames), 10, 1, 4))

    def prepareforbattle(self):
        print("A FIGHT APPEARS!\n\n")
        self.heroparty.partyprep(self)


        time.sleep(1)


    def loss(self):
        print("Thats a loss.. Remaining units:")
        for unit in self.baddieparty.members:
            print(unit)


    def victory(self):
        print("\n\nVictory!! \nVictors of this battle:")

        for unit in self.heroparty.members:
            print(unit)
        self.heroparty.team_rest()

    def endofbattle(self):
        if not self.baddieparty.team_alive():
            self.victory()

        elif not self.heroparty.team_alive():
            self.loss()


    def tick(self):
        """Main loop inside a fight"""
        while self.heroparty.team_alive() and self.baddieparty.team_alive():
            print("\n\t\tTURN %d" % self.turn)
            self.turn += 1
                    #HERO TURN
            self.heroparty.tick(self.baddieparty)
                    #BADDIE TURN
            self.baddieparty.tick(self.heroparty)
            time.sleep(1)

        self.endofbattle()


############################################################################

class Maingame():
    """The main game"""
    def __init__(self):
        self.heroparty = Party()
        self.createheroparty()
        self.run()

    def createheroparty(self):
        #TODO: BETTER HERO-IMPLEMENTATION
        dude = Unit("Stronk", 10, 5, 1)
        self.heroparty.join_party(dude)



    def run(self):
        for x in range (1, 5):
            fight = Fight(self.heroparty, x)
            fight.tick()

            if not self.heroparty.team_alive():
                break




if __name__ == '__main__':
    Maingame()