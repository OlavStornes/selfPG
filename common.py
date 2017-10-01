import random

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


######  UNITS  ######

LVL_HPGAIN = 5
LVL_STRONKGAIN = 2
LVL_SMRTGAIN = 1

TEST_XPGET = 3


######  ACTIVITIES  ######
TRAVEL_DISTANCE = 4
TRAVEL_NAME = "Testlocation"

TR_LO = 1
TR_HI = 3

######  EVENTS  ######

BAD_HP_LO = 10
BAD_HP_HI = 20