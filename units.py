import random
from common import *
import time


class Party():
    """Party-class to keep everything and everyone on the same team organized"""
    def __init__(self):
        self.members = []
        self.killed = []
        self.inventory = []
        self.cur_fight = None
        

    def join_party(self, person):
        self.members.append(person)

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

    def partyprep(self, fight):
        for unit in self.members:
            print(unit)
            unit.cur_fight = fight


    def tick(self, targetparty):
        """Main loop for a party-fight"""
        for unit in self.members:
            if unit.is_alive():
                unit.tick(targetparty)
            else:
                print("%s is killed!" % unit.name)
                self.killed.append(unit)
                self.members.remove(unit)


        time.sleep(1)



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
        self.cur_fight = None
        self.alive = True
        

    def __str__(self):
        return("Name: %s \t Hp: %d/%d\tStrength: %d" 
            %(self.name,    self.hp, self.maxhp, self.stronk))

    def get_target(self, target):
        print("%s looks towards %s" %(self.name, target.name))
        self.target = target

    def search_target(self, targetparty):
        """Search for a hostile target"""
        #Current strategy : Target the lowest HP-baddie
        if targetparty.team_alive():
            potentialtarget = targetparty.members[0]
            lowesthp = targetparty.members[0].hp
            for i in targetparty.members:
                if i.hp < lowesthp:
                    potentialtarget = targetparty.members[i]
                    lowesthp = targetparty.members[i].hp
            self.get_target(potentialtarget)
        else:
            print("%s has no more targets" % self.name)
        
    def is_alive(self):
        return self.hp > 0

    def get_experience(self, amountxp):
        self.xp += amountxp
        print ("%s got %d experience!" % (self.name, amountxp))

        if self.xp >= self.nextlvl:
            self.level_up()


    def level_up(self):
        self.xp -= self.nextlvl
        self.lvl +=1
        hpgain = 5
        stronkgain = 2
        smrtgain = 1

        self.maxhp += hpgain
        self.stronk += stronkgain
        self.smart += smrtgain
        self.rest()
            
        print("%s Leveled up! Gained %d HP, %d str, %d int" % (self.name, hpgain, stronkgain, smrtgain))
        print (self)

    def attack(self, target):
        #TODO: Randomized damage
        if target:
            damage = random.randint(int(self.stronk/2), self.stronk)
            target.hp -= damage
            print("%s hit %s for %d damage! Target has %d hp left" %(self.name, target.name, damage, target.hp))

            if target.hp <= 0:

                self.get_experience(3)
                self.target = None

    def defend(self, target):
        #TODO: Some sort of block\damage reduction
        pass

    def rest(self):
        self.hp = self.maxhp
        print("%s rested to full!" % self.name)

    def tick(self, hostileparty):
        if self.target:
            if self.target.is_alive():
                self.attack(self.target)
        else:
            self.search_target(hostileparty)


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