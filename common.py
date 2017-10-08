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


def roll_d6():
    return random.randint(1, 6)

def roll_d10():
    return random.randint(1, 10)

def roll_d12():
    return random.randint(1, 12)

def roll_d20():
    return random.randint(1, 20)



######  GUI  ######

PARTY_TITLE = "selfRPG"


TEST_ROOMS = 2
GUI_UPDATE_RATE = 1000
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
BUT_ROWSPAN = 2

MAP_WIDTH = 484
MAP_HEIGHT = 269


######  UNITS  ######

LVL_HPGAIN = 5
LVL_STRONKGAIN = 2
LVL_SMRTGAIN = 1

TEST_XPGET = 3

MAX_PARTYSIZE = 4


######  ACTIVITIES  ######
TRAVEL_DISTANCE = 4
TRAVEL_NAME = "Testlocation"

TR_LO = 1
TR_HI = 3

######  EVENTS  ######

BAD_HP_LO = 10
BAD_HP_HI = 20