import random
import events as M
import units as U
from common import *


class Travel():
    """An activity where the party travels from one point to another"""
    def __init__(self, party, destination=None):
        self.party = party
        self.destination = destination
        self.vector_x = 0 
        self.vector_y = 0
        #HACK: Must implement better later
        test_x = random.randint(2, MAP_WIDTH)
        test_y = random.randint(2, MAP_HEIGHT)
        
        self.target = Point(test_x, test_y)

        self.startjourney()

    def __str__(self):
        return ("Traveling to %d, %d - Distance left: %d units" %(self.target.x, self.target.y, self.party.pos.distance(self.target)))

    def startjourney(self):

        #If nothing is specified, the party wants to travel to a city for further missions
        if self.destination is None:
            self.find_closesttown()
        
        else:
            pass

        self.calc_vector()
        self.party.print_t("Traveling to: %s." %(self.destination))

    def find_closesttown(self):
        """Find closest town known, and set destination there"""

        closest_distance = 9999999999 #HACK: Find a better way to start from the top
        closest_town = None
        for town in self.party.townmap:
            if town.pos.distance(self.party.pos) < closest_distance:
                closest_town = town
                closest_distance = town.pos.distance(self.party.pos)

        #Found the closest town. Assign travel vector
        self.target = closest_town.pos
        self.destination = Visit_town(self.party, closest_town)
        
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
            self.party.activity = self.destination
        




class Visit_town():
    """A place where you can rest, drink and recruit freshmen"""
    def __init__(self, party, town):
        self.party = party
        self.daysintown = 0
        self.town = town

    def recruit(self):
        if len(self.party.members) + len(self.party.killed) < MAX_PARTYSIZE:
            self.party.gold -= RECRUIT_COST
            newmember = U.Fighter("Newcomer")
            self.party.join_party(newmember)
            self.party.print_t(str(newmember.name) + " joined the team!")
        else:
            print("Cant recruit anymore: MAX SIZE REACHED")

    def tick(self):
        #self.party.team_rest()

        self.daysintown += 1

        if self.daysintown == 2:
            if self.party.gold > RECRUIT_COST:
                self.recruit()

        elif self.daysintown == 3:
            self.party.team_rest()

        elif self.daysintown > 4:
            #Find a quest in town - ie. a dungeon to crawl
            quest = Dungeon(self.party, 3)
            self.party.activity = Travel(self.party, quest)

        #TODO:
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
        dice = roll_dice(1, 20)
        if dice < 20:
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