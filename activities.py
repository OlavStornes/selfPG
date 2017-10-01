import random
import events as M
from common import *


class Travel():
    """An activity where the party travels from one point to another"""
    def __init__(self, party):
        self.party = party
        self.progress = 0
        self.distance = TRAVEL_DISTANCE
        self.destination = TRAVEL_NAME
        self.startjourney()

    def __str__(self):
        return ("Traveling to %s - traveled %d of %d units" %(self.destination, self.progress, self.distance))

    def startjourney(self):
        self.party.print_t("Traveling to: %s. Its %d units away" %(self.destination, self.distance))

    def arewethereyet(self):
        return self.distance <= self.progress

    def tick(self):
        self.progress += random.randint(TR_LO, TR_HI)
        if self.arewethereyet():
            self.party.print_t("Arrived at %s!" %(self.destination))

            self.party.activity = Dungeon(self.party, 3)




class Dungeon():
    def __init__(self, party, rooms):
        self.heroparty = party
        self.depth = rooms
        self.room = 0
        self.dungeon_lvl = self.heroparty.get_teamlevel()
        self.cur_room = None

    def __str__(self):
        return ("Wandering in a dungeon. Progress: %d of %d rooms " %(self.room, self.depth))

    def newroom(self):
        """Create a new room. TODO: Get more varied rooms"""
        self.print_dungeon()
        d10 = roll_d10()
        if d10 < 9:
            #n_mobs = random.randint(2, 5)
            n_mobs = 1
            self.cur_room = M.Fight(self.heroparty, n_mobs)
        else:
            print("Nothing of value was found")
            self.heroparty.team_rest()


    def dungeon_complete(self):
        self.heroparty.print_t("You are a winner of whole dungeon!!!")
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
        self.heroparty.print_t ("DUNGEON MAP\n" + border + "\n" + mid + "\n" + border)

    def tick(self):
        if self.heroparty.team_alive():
            if self.heroparty.cur_fight:
                self.cur_room.tick()
            else:
                #If there is no room, generate a new one
                self.room += 1
                if self.room == self.depth:
                    #Victory condition
                    self.dungeon_complete()
                else:
                    self.newroom()