import random
import events as M
import units as U
from common import *


class Travel():
    """An activity where the party travels from one point to another"""
    def __init__(self, party):
        self.party = party
        self.progress = 0
        self.destination = TRAVEL_NAME
        #HACK: Must implement better later
        test_x = random.randint(2, MAP_WIDTH)
        test_y = random.randint(2, MAP_HEIGHT)
        
        self.target = Point(test_x, test_y)

        self.startjourney()

    def __str__(self):
        return ("Traveling to %s - Distance left: %d units" %(self.destination, self.party.pos.distance(self.target)))

    def startjourney(self):
        self.calc_vector()
        self.party.print_t("Traveling to: %s." %(self.destination))
        
    def calc_vector(self):
        """Calculate what direction and how far a travel must go"""
        self.vector_x, self.vector_y = self.party.pos.vector(self.target)


    def progress_towards_dest(self, tmpvec):
        """Calculate how far a party will travel a given direction"""

        if tmpvec < 0:
            #A negative vector = travel north/west
            dist = -2

            
            
        elif tmpvec > 0:
            #A positive vector = travel south/east
            dist = 2

            
        elif tmpvec == 0:
            #This axis is aligned
            dist = 0

        #avoid overshooting
        if abs(dist) > abs(tmpvec):
            dist = tmpvec

        return dist
            



    def tick(self):
        #HACK: Early access implementation

        if self.vector_x or self.vector_y:
            travel_x = self.progress_towards_dest(self.vector_x)
            travel_y = self.progress_towards_dest(self.vector_y)

            #Update vector
            self.vector_x -= travel_x
            self.vector_y -= travel_y

            #Update party
            self.party.pos.x += travel_x
            self.party.pos.y += travel_y

        else:
            #Arrived at location
            self.party.print_t("Arrived at %s!" %(self.destination))
            self.party.activity = Dungeon(self.party, 3)
        

class Town():
    """A place where you can rest, drink and recruit freshmen"""
    def __init__(self, party):
        print("In town")
        self.party = party
        self.daysintown = 0

    def recruit(self):
        self.party.join_party(U.Unit("Newcomer", 10, 3, 6))

    def tick(self):
        #self.party.team_rest()

        self.daysintown += 1

        if self.daysintown ==2:
            self.recruit()

        elif self.daysintown > 4:
            self.party.activity = Travel(self.party)
        #good rest
        #attempt sell
        # use money
        # recruit
        # plan yourney
        # go 

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
            self.cur_room = M.Fight(self.heroparty, self.dungeon_lvl)
        else:
            self.heroparty.print_t("Nothing of value was found")
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