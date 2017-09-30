import time
import random
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
        self.heroparty.partyprep(self, self.baddieparty)

        print("\nOpposing forces :")
        self.baddieparty.partyprep(self, self.heroparty)

        self.tick()


    def loss(self):
        print("Thats a loss.. Remaining units:")
        for unit in self.baddieparty.members:
            print(unit)


    def victory(self):
        print("\n\nVictory!! \nVictors of this battle:")

        for unit in self.heroparty.members:
            print(unit)

        self.heroparty.team_getexp(1)


    def endofbattle(self):

        if not self.baddieparty.team_alive():
            self.victory()

        elif not self.heroparty.team_alive():
            self.loss()
        self.heroparty.team_endoffight()

    def is_fight_active(self):
        return self.heroparty.team_alive() and self.baddieparty.team_alive()


    def tick(self):
        """Main loop inside a fight"""
        if self.heroparty.team_alive() and self.baddieparty.team_alive():
            print("\n\t\t\tTURN %d" % self.turn)
            self.turn += 1
                    #HERO TURN
            changecolor(Fore.LIGHTBLUE_EX)
            self.heroparty.team_attack()
                    #BADDIE TURN
            changecolor(Fore.RED)
            self.baddieparty.team_attack()

            changecolor(Fore.RESET)

        else:
            self.endofbattle()


##################################################

class Dungeon():
    def __init__(self, party, rooms):
        self.heroparty = party
        self.depth = rooms
        self.room = 0
        self.dungeon_lvl = self.heroparty.get_teamlevel()
        self.cur_room = None

    def newroom(self):
        """Create a new room. TODO: Get more varied rooms"""
        self.print_dungeon()
        d10 = roll_d10()
        if d10 < 9:
            #n_mobs = random.randint(2, 5)
            n_mobs = 1
            self.cur_room = Fight(self.heroparty, n_mobs)
        else:
            print("Nothing of value was found")
            self.heroparty.team_rest()


    def dungeon_complete(self):
        print("You are a winner of whole dungeon!!!")
        self.heroparty.team_rest()
        #Exiting dungeon
        self.heroparty.activity = None
    
    def print_dungeon(self):
        border = ""
        mid = ""
        for i in range(self.depth):
            border += "###|"
            if self.room == i:
                mid += " X ="
            else:
                mid += "   ="
        print (Fore.CYAN +"\tDUNGEON MAP\n\t" + border + "\n\t" + mid + "\n\t" + border, Fore.RESET)

    def tick(self):
        if self.heroparty.team_alive():
            if self.heroparty.cur_fight:
                self.cur_room.tick()
            else:
                #If there is no room, generate a new one
                self.room += 1
                print(self.room, self.depth)
                if self.room >= self.depth:
                    #Victory condition
                    self.dungeon_complete()
                else:
                    self.newroom()


############################################################################





class Maingame():
    """The main game"""
    def __init__(self):
        self.heroparty = Party()
        self.createheroparty()



        self.run()

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
    pass