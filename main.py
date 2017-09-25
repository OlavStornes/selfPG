import time
import random
import colorama as cr
from colorama import Fore
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

        self.startfight()


    def createbaddies(self):
        #TODO: MORE VARIATION
        #TODO: IMPLEMENT DIFFICULTY 
        for x in range(self.difficulty):
            self.baddieparty.join_party(Unit(random.choice(Baddienames), 15, 10, 4))

    def prepareforbattle(self):
        print("\n\tA FIGHT APPEARS!\n")
        print("Attacking forces :")
        self.heroparty.partyprep(self)

        print("\nOpposing forces :")
        self.baddieparty.partyprep(self)

        time.sleep(3)


    def loss(self):
        print("Thats a loss.. Remaining units:")
        for unit in self.baddieparty.members:
            print(unit)


    def victory(self):
        print("\n\nVictory!! \nVictors of this battle:")

        for unit in self.heroparty.members:
            print(unit)

        self.heroparty.team_getexp(1)
        self.heroparty.team_rest()
        time.sleep(3)

    def endofbattle(self):
        if not self.baddieparty.team_alive():
            self.victory()

        elif not self.heroparty.team_alive():
            self.loss()


    def startfight(self):
        """Main loop inside a fight"""
        while self.heroparty.team_alive() and self.baddieparty.team_alive():
            print("\n\t\t\tTURN %d" % self.turn)
            self.turn += 1
                    #HERO TURN
            changecolor(Fore.LIGHTBLUE_EX)
            self.heroparty.tick(self.baddieparty)
                    #BADDIE TURN
            changecolor(Fore.RED)
            self.baddieparty.tick(self.heroparty)

            changecolor(Fore.RESET)



        self.endofbattle()


############################################################################

class Maingame():
    """The main game"""
    def __init__(self):
        self.heroparty = Party()
        self.createheroparty()
        cr.init()

        self.run()

    def createheroparty(self):
        #TODO: BETTER HERO-IMPLEMENTATION
        dude = Unit("Stronk", 10, 5, 1)
        otherdude = Unit("Tank", 25, 2, 1)

        self.heroparty.join_party(dude)
        self.heroparty.join_party(otherdude)



    def run(self):
        for x in range (1, 5):
            fight = Fight(self.heroparty, x)

            if not self.heroparty.team_alive():
                break




if __name__ == '__main__':
    Maingame()