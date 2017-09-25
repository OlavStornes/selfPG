import time
import random
import colorama as cr
from colorama import Fore
from common import *
from units import *



class Fight():
    """Class for fights between two parties"""
    def __init__(self, heroes, difficulty):

        self.heroparty = heroes
        self.baddieparty = Party()
        self.difficulty = difficulty
        self.createbaddies()
        self.turn = 0
        self.prepareforbattle()


    def createbaddies(self):
        """Create enemies in a party"""
        #TODO: MORE VARIATION
        #TODO: IMPLEMENT DIFFICULTY 
        for x in range(self.difficulty):
            self.baddieparty.join_party(Unit(random.choice(Baddienames), 15, 2, 4))

    def prepareforbattle(self):
        """Initial start of a battle"""
        print("\n\tA FIGHT APPEARS!\n")
        print("Attacking forces :")
        self.heroparty.partyprep(self)

        print("\nOpposing forces :")
        self.baddieparty.partyprep(self)

        time.sleep(3)
        self.startfight()


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


class Dungeon():
    def __init__(self, party, rooms):
        self.heroparty = party
        self.rooms = rooms
        self.currentroom = 0
        self.tick()

    def newroom(self):
        Fight(self.heroparty, 1)

    def endcondition(self):
        if self.heroparty.team_alive():
            print("You are a winner!")

        else:
            print("Game over")
    
    def print_dungeon(self):
        border = ""
        mid = ""
        for i in range(self.rooms):
            border += "###|"
            if self.currentroom == i:
                mid += " X ="
            else:
                mid += "   ="

        print (Fore.CYAN +"\tDUNGEON MAP\n\t" + border + "\n\t" + mid + "\n\t" + border, Fore.RESET)

    def tick(self):
        for i in range(self.rooms):
            self.print_dungeon()
            self.newroom()
            if not self.heroparty.team_alive():
                break
            self.currentroom +=1
        self.endcondition()



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
        self.heroparty.join_party(Unit("Stronk", 10, 5, 1))
        self.heroparty.join_party(Unit("Tank", 25, 2, 1))



    def run(self):
        Dungeon(self.heroparty, 4)


if __name__ == '__main__':
    Maingame()