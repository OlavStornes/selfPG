import random


class Point():
    """A point to keep track off positions"""
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y


    def distance(self, target):
        """Return a distance in units"""
        #TODO: Proberly implement both directions
        x_distance = abs(self.x - target.x)
        y_distance = abs(self.y - target.y)
        return x_distance + y_distance

    def vector(self, target):
        """Return a tuple for distance and which way the target point is"""
        x_vec = target.x - self.x
        y_vec = target.y - self.y
        return (x_vec, y_vec)

Baddienames = [
                "Bawb",
                "Beamos",
                "Bee",
                "Beetle",
                "Bellum Blob",
                "Big Baba",
                "Big Blin",
                "Big Deku Baba",
                "Big Poe",
                "Skulltula",
                "Bigocto",
                "Bio-Cube"]

Partynames = [
    "wu tang",
    "hyrule suckas",
    "gogo gadgets"
]

def roll_d2():
    return random.randint(1, 2)

def roll_d3():
    return random.randint(1, 2)

def roll_d6():
    return random.randint(1, 6)

def roll_d10():
    return random.randint(1, 10)

def roll_d12():
    return random.randint(1, 12)

def roll_d20():
    return random.randint(1, 20)

def roll_dice(n_dice, dicetype):
    dicesum = 0
    for x in range(n_dice):
        dicesum += random.randint(1, dicetype)
    return dicesum

def increase_stat(growth):
        #TODO: Make an unique way for HP. Maybe multiply it all at the end?
        if growth == "low":
            #1D2
            return roll_dice(1, 2)
        elif growth == "med":
            #1D3
            return roll_dice(1, 3)
        elif growth == "high":
            #3D2
            return roll_dice(3, 2)

######  GUI  ######

PARTY_TITLE = "selfRPG"


TEST_ROOMS = 2
GUI_UPDATE_RATE = 250
PARTY_BG = "gray50"
BADDIE_BG = "red"

PARTY_COL = 0

LOG_HEIGHT = 20
LOG_WIDTH = 60
LOG_ROW = 1
LOG_COL = 1
LOG_ROWSPAN = LOG_HEIGHT
SCROLL_ROW = LOG_ROW + 1
SCROLL_COL = LOG_COL + 1

BUT_FRAME_ROW = 1
BUT_FRAME_COL = 3
BUT_ROWSPAN = 1

MAP_WIDTH = 484
MAP_HEIGHT = 269


######  UNITS  ######

XP_BASE = 100
XP_EXPONENT = 1.5

LVL_HPGAIN = 5
LVL_STRONKGAIN = 2
LVL_SMRTGAIN = 1

TEST_XPGET = 3

MAX_PARTYSIZE = 4

TOWN_NAME = "Townie"


######  ACTIVITIES  ######
TRAVEL_DISTANCE = 4
TRAVEL_NAME = "Testlocation"

TR_LO = 1
TR_HI = 3

RECRUIT_COST = 1000

######  EVENTS  ######

BAD_HP_LO = 10
BAD_HP_HI = 20