import events as M
import units as U
from common import *


class Travel():
    """An activity where the party travels from one point to another"""
    def __init__(self, party, destination=None):
        self.party = party
        self.vector_x = 0 
        self.vector_y = 0
        #NOTE: Must implement better later
        test_x = random.randint(2, MAP_WIDTH)
        test_y = random.randint(2, MAP_HEIGHT)
        
        #Destination is an activity, while target is the position of abovementioned activity
        self.destination = destination
        try:
            self.target = destination.pos
        except AttributeError:
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
        """Calculate how far a party will travel one given direction(north/south, east/west)"""

        travel_speed = 2

        #Slow down the party if someone is killed
        if self.party.killed:
            travel_speed = 1

        #A negative vector = travel north/west
        if tmpvec < 0:
            dist = -travel_speed
        #A positive vector = travel south/east
        elif tmpvec > 0:
            dist = travel_speed
        #This axis is aligned
        elif tmpvec == 0:
            dist = 0

        #avoid overshooting
        if abs(dist) > abs(tmpvec):
            dist = tmpvec

        return dist

    def tick(self):
        #NOTE: Early access implementation

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

        self.is_hospitalised = False
        self.has_rested = False
        self.attempted_recruit = False

        self.days_hospitalized = 30
        self.days_left = self.days_hospitalized

    def hospital_trip(self):
        """Wait at the hospital for dead heroes to get alive"""
    
        #First time at the hospital. Pay up and chill
        if self.days_left == self.days_hospitalized:
            #Gotta pay up for healing services
            #NOTE: Should i just eliminate dead people that heroes cant afford? :thinking:
            res_price = len(self.party.killed)*self.party.get_killedlvl()*50
            self.town.inputgold(self.party, res_price)
            self.party.print_t("Visiting the hospital for a few turns..")
            self.is_hospitalised = True 
        
        #This will take some days
        self.days_left -= 1 

        if self.days_left == 0:
            self.is_hospitalised = False
            for person in self.party.killed:
                self.party.resurrect_hero(person)
        

    def recruit(self):
        """Recruit someone from the town if the party can afford it"""
        if self.party.gold > RECRUIT_COST:
            if len(self.party.members) + len(self.party.killed) < MAX_PARTYSIZE:
                #self.party.gold -= RECRUIT_COST
                self.town.inputgold(self.party, RECRUIT_COST)
                newmember = U.Fighter("Newcomer")
                self.party.join_party(newmember)
                self.party.print_t(str(newmember.name) + " joined the team!")
            else:
                self.party.print_t("Cant recruit anymore: MAX SIZE REACHED")

        self.attempted_recruit = True

    def town_inn_rest(self):
        """Try to buy a room to rest in"""
        price_room = (TOWN_REST_PR * len(self.party.members))

        if self.party.gold > price_room:
            #self.party.gold -= price_room
            self.town.inputgold(self.party, price_room)
            self.party.print_t("Payed %d gold for a good nights rest" %(price_room))
            self.party.team_rest()
        
        self.has_rested = True

    def plan_journey(self):
        #Create a random vector with a given distance away
        x_vector = random.randint(-TOWN_QUEST_DISTANCE, TOWN_QUEST_DISTANCE)
        y_vector = random.randint(-TOWN_QUEST_DISTANCE, TOWN_QUEST_DISTANCE)

        #Apply vector to current location
        x = self.town.pos.x + x_vector
        y = self.town.pos.y + y_vector

        #edge cases on the map
        x = statistics.median([0, x, MAP_WIDTH])
        y = statistics.median([0, y, MAP_HEIGHT])
        
        return Point(x, y)

    def tick(self):
        """Main tick for visiting a town"""

        self.daysintown += 1

        if self.party.killed:
            self.hospital_trip()

        if self.is_hospitalised is True:
            return

        elif self.has_rested is False:
            self.town_inn_rest()
            

        elif self.attempted_recruit is False:
            self.recruit()


        else:
            #Find a quest in town - ie. a dungeon to crawl
            marker = self.plan_journey()
            quest = Dungeon(self.party, 3, marker)
            self.party.activity = Travel(self.party, quest)

        #TODO:
        # Attempt sell
        # plan yourney
        # go 

class Dungeon():
    """A dungeon where a party must traverse to the end. Random battles ensues"""
    def __init__(self, party, rooms, pos=None):
        self.heroparty = party
        self.depth = rooms
        self.room = 0
        self.dungeon_lvl = self.heroparty.get_teamlevel()
        self.cur_room = None

        if pos:
            self.pos = pos
        else:
            x = random.randint(2, MAP_WIDTH)
            y = random.randint(2, MAP_HEIGHT)
            self.pos = Point(x, y)
        
            

    def __str__(self):
        return ("A dungeon. Progress: %d of %d rooms " %(self.room, self.depth))

    def newroom(self):
        """Create a new room. TODO: Get more varied rooms"""
        dice = roll_dice(1, 20)
        if dice < 20:
            self.cur_room = M.Fight(self.heroparty, self.dungeon_lvl)
        else:
            self.heroparty.print_t("Nothing of value was found")


    def dungeon_complete(self):
        self.heroparty.print_t("You are a winner of whole dungeon!!!")

        #HACK: Just a way to start something that intensifies an economy
        gold_chest = self.dungeon_lvl * 100
        self.heroparty.gold += gold_chest

        #Exiting dungeon
        self.heroparty.activity = None

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