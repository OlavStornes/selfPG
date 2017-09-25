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


def changecolor(whatcolor):
    print(whatcolor, end='')


def roll_d6():
    return random.randint(1, 6)

def roll_d10():
    return random.randint(1, 10)

def roll_d12():
    return random.randint(1, 12)

def roll_d20():
    return random.randint(1, 20)
