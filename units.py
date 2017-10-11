import random
from common import *
import events as m
import activities as a
import time
import tkinter as tk

class Town():
    """A persistent town inside the world"""
    def __init__(self):
        self.name = TOWN_NAME
        self.reputation = 0

        x = random.randint(10, MAP_WIDTH-10)
        y = random.randint(10, MAP_HEIGHT-10)

        self.pos = Point(x, y)

class Party():
    """Party-class to keep everything and everyone on the same team organized"""
    def __init__(self, gui_log=None):
        self.partyname = random.choice(Partynames)
        # self.pos_x = 200 #HACK:
        # self.pos_y = 200 #HACK:
        self.members = []
        self.killed = []
        self.inventory = []
        self.log = gui_log
        self.cur_fight = None
        self.activity = None
        self.townmap = None
        self.gold = 0

        self.test_setrandompos()

    def test_gettownmap(self, townmap):
        """ALPHA: get worldmap from main game"""
        self.townmap = townmap

    def test_setrandompos(self):
        x = random.randint(1, MAP_WIDTH)
        y = random.randint(1, MAP_HEIGHT)

        self.pos = Point(x, y)

    def __str__(self):
        return str(self.partyname) + ": " + str(self.activity)
        

    def join_party(self, person):
        person.party = self
        self.members.append(person)


    def print_t(self, sentence):
        """Prints inside the party-log of chosen team"""
        #Everything crashes if a party-window has been opened and closed. Avoiding the problem here
        try:
            self.log.insert(tk.END, str(sentence) + "\n")
            self.log.see(tk.END)
        except:
            pass

    def team_alive(self):
        return len(self.members) > 0

    def team_endoffight(self):
        self.cur_fight = None

    def get_teamlevel(self):
        tmp = 0
        for i, point in enumerate(self.members):
            tmp += point.lvl
        return tmp

    def team_getexp(self, xp):
        for unit in self.members:
            unit.get_experience(xp)

    def team_rest(self):
        for unit in self.members:
            unit.rest()

    def partyprep(self, fight, targetparty):
        self.cur_fight = fight
        self.targetparty = targetparty
        for unit in self.members:
            unit.cur_fight = fight

    def tick(self):
        if not self.activity:
            self.print_t("Lets go to a town!")
            self.activity = a.Travel(self)
            #self.activity = a.Dungeon(self, 3)

        else:
            self.activity.tick()


    def team_attack(self):
        """Main loop for a party-fight"""
        for unit in self.members:
            if unit.is_alive():
                unit.tick(self.targetparty)
            else:
                self.print_t("%s is killed!" % unit.name)
                self.killed.append(unit)
                self.members.remove(unit)




class Unit():

    def __init__(self, name):
        self.name = name
        self.maxhp = 100
        self.hp = self.maxhp
        self.lvl = 1
        self.exp = 0
        self.nextlvl = XP_BASE
        self.stronk = 10
        self.smart = 10
        self.target = None
        self.party = None

        self.statgrowth = {"hp": "med", "stronk": "med", "smart": "med"}

    def __str__(self):
        return("Name: %s \t Hp: %d/%d\t Strength: %d - LVL %d" 
            %(self.name,    self.hp, self.maxhp, self.stronk, self.lvl))

    def print_t(self, sentence, fg=None):
        """Print into the party-combat log"""
        self.party.print_t(sentence)

    def get_target(self, target):
        #self.print_t("%s looks towards %s" %(self.name, target.name))
        self.target = target

    def search_target(self, targetparty):
        """Search for a hostile target"""
        #Current strategy : Target the lowest HP-baddie
        if targetparty.team_alive():
            potentialtarget = targetparty.members[0]
            lowesthp = targetparty.members[0].hp
            for npc in targetparty.members:
                if npc.hp < lowesthp:
                    potentialtarget = npc
                    lowesthp = npc.hp
            self.get_target(potentialtarget)
        else:
            self.print_t("%s has no more targets" % self.name)
        
    def is_alive(self):
        return self.hp > 0

    def get_experience(self, amountxp):
        self.exp += amountxp
        self.print_t ("%s got %d experience!" % (self.name, amountxp))

        if self.exp >= self.nextlvl:
            self.level_up()

    

    def increase_all_stat(self):
        """Increase all stats of a hero"""
        #Note: increase_stat is in common.py
        self.maxhp += increase_stat(self.statgrowth["hp"])
        self.stronk += increase_stat(self.statgrowth["stronk"])
        self.smart += increase_stat(self.statgrowth["smart"])
        


    def level_up(self):
        self.exp -= self.nextlvl
        self.lvl += 1

        #make an exponential growth of next lvl
        self.nextlvl = int(XP_BASE * (self.lvl ** XP_EXPONENT))

        self.increase_all_stat()

        print (self.statgrowth)
        print(self.lvl, self.nextlvl, self.stronk, self.hp)
        self.print_t("%s Leveled up!" % (self.name))


    def attack(self, target):
        #TODO: Better randomized damage
        if target:
            damage = random.randint(int(self.stronk/2), self.stronk)
            target.hp -= damage
            self.print_t("%s hit %s for %d damage! Target has %d hp left" %(self.name, target.name, damage, target.hp))

            if target.hp <= 0:

                self.get_experience(TEST_XPGET)
                self.target = None

    def defend(self, target):
        #TODO: Some sort of block\damage reduction
        pass

    def rest(self):
        self.hp = self.maxhp
        self.print_t("%s rested to full!" % self.name)

    def tick(self, hostileparty):
        if self.target:
            if self.target.is_alive():
                self.attack(self.target)
        else:
            self.search_target(hostileparty)
            self.attack(self.target)

class Fighter(Unit):
    """A fighter that specialies in melee. Stronk dude, but not so smart"""
    def __init__(self, name, hp, stronk, smart):
        Unit.__init__(self, name, hp, stronk, smart)



class Baddie(Unit):
    def __init__(self, name, hp, stronk):
        Unit.__init__(self, name, hp, stronk, smart=0)

    def search_target(self, hostileparty):
        """Enemy targeting: Find a random hero and hit him"""
        #TODO: AGGRO-abillity from tanks etc
        if hostileparty.team_alive():
            self.get_target(random.choice(hostileparty.members))

    def tick(self, hostileparty):

        self.search_target(hostileparty)
        self.attack(self.target)