from common import *
import events as M


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