import time
import random
import gui
import colorama as cr
from colorama import Fore
from common import *
from units import *


#Initialize colors
cr.init()

class Fight():
    """Class for fights between two parties"""
    def __init__(self, heroes, difficulty):

        self.heroparty = heroes
        self.baddieparty = Party()
        self.difficulty = difficulty
        self.createbaddies()
        self.turn = 0

        self.gui = gui.Party_gui(master=None, maingame=self)
        self.gui.after(0, self.gui.tick)

        self.prepareforbattle()

    def createbaddies(self):
        """Create enemies in a party"""
        #TODO: MORE VARIATION
        #TODO: IMPLEMENT DIFFICULTY 
        for x in range(self.difficulty):
            name = random.choice(Baddienames)
            hp = random.randint(10, 20)
            stronk = random.randint(4, 7)
            self.baddieparty.join_party(Baddie(name, hp, stronk))

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
        time.sleep(1)

    def endofbattle(self):
        self.heroparty.team_endoffight()

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
        self.dungeon_lvl = self.heroparty.get_teamlevel()
        self.tick()

    def newroom(self):
        d10 = roll_d10()
        if d10 < 7:
            n_mobs = random.randint(2, 5)
            Fight(self.heroparty, n_mobs)
        else:
            print("Nothing of value was found")
            self.heroparty.team_rest()

    def endcondition(self):
        if self.heroparty.team_alive():
            print("You are a winner!")
            self.heroparty.team_rest()

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


        self.GUI_init()
        self.run()

    def GUI_init(self):
        self.gui = gui.Party_gui()
        self.gui.tick()

    def createheroparty(self):
        #TODO: BETTER HERO-IMPLEMENTATION
        self.heroparty.join_party(Unit("Stronk", 20, 8, 1))
        self.heroparty.join_party(Unit("Tank", 40, 6, 1))



    def run(self):
        numberrooms = 1
        while self.heroparty.team_alive():
            Dungeon(self.heroparty, numberrooms)
            numberrooms +=1


if __name__ == '__main__':
    #Maingame()
    party = Party()
    party.join_party(Unit("Stronk", 20, 8, 1))

    Fight(party, 1)