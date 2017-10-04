import random
from common import *
import events as m
import activities as a
import time
import tkinter as tk


class Party():
    """Party-class to keep everything and everyone on the same team organized"""
    def __init__(self, gui_log=None):
        self.partyname = random.choice(Partynames)
        self.members = []
        self.killed = []
        self.inventory = []
        self.cur_fight = None
        self.activity = None
        self.log = gui_log

    def __str__(self):
        return str(self.partyname) + ": " + str(self.activity)
        

    def join_party(self, person):
        if len(self.members) + len(self.killed) < MAX_PARTYSIZE:
            person.party = self
            self.print_t(str(person.name) + " joined the team!")
            self.members.append(person)
        else:
            print("Cant recruit anymore: MAX SIZE REACHED")

    def print_t(self, sentence, fg=None):
        """Prints inside the party-log of chosen team"""
        if self.log:
            self.log.insert(tk.END, str(sentence) + "\n")
            self.log.see(tk.END)

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
            self.print_t("Lets go explore somewhere!")
            #self.activity = a.Travel(self)
            self.activity = a.Dungeon(self, 3)

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

    def __init__(self, name, hp, stronk, smart):
        self.name = name
        self.hp = hp
        self.maxhp = hp
        self.lvl = 1
        self.xp = 0
        self.nextlvl = 10 * self.lvl
        self.stronk = stronk
        self.smart = smart
        self.target = None
        
        self.party = None

    def __str__(self):
        return("Name: %s \t Hp: %d/%d\t Strength: %d - LVL %d" 
            %(self.name,    self.hp, self.maxhp, self.stronk, self.lvl))

    def print_t(self, sentence, fg=None):
        """Print into the party-combat log"""
        self.party.print_t(sentence)

    def get_target(self, target):
        self.print_t("%s looks towards %s" %(self.name, target.name))
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
        self.xp += amountxp
        self.print_t ("%s got %d experience!" % (self.name, amountxp))

        if self.xp >= self.nextlvl:
            self.level_up()


    def level_up(self):
        self.xp -= self.nextlvl
        self.lvl +=1
        hpgain = LVL_HPGAIN
        stronkgain = LVL_STRONKGAIN
        smrtgain = LVL_SMRTGAIN

        self.maxhp += hpgain
        self.stronk += stronkgain
        self.smart += smrtgain
        self.rest()
            
        self.print_t("%s Leveled up! Gained %d HP, %d str, %d int" % (self.name, hpgain, stronkgain, smrtgain))


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