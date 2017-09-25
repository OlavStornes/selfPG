import random
from common import *


class Party():
    """Party-class to keep evereything and everyone on the same team organized"""
    def __init__(self):
        self.members = []
        self.killed = []
        self.inventory = []
        self.cur_fight = None
        

    def join_party(self, person):
        self.members.append(person)

    def team_alive(self):
        return len(self.members) > 0

    def team_rest(self):
        for unit in self.members:
            unit.rest()

    def partyprep(self, fight):
        for unit in self.members:
            print(unit)
            unit.cur_fight = fight


    def tick(self, targetparty):
        """Main loop for a party-fight"""
        #TODO: AVOID LIST INDEX OUT OF RANGE - REMOVED TARGET
        for unit in self.members:
            if not unit.target:
                unit.search_target(targetparty)
            unit.tick()

            if unit.alive == False:
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
        self.cur_fight = None
        self.alive = True
        

    def __str__(self):
        return("Name: %s \t Hp: %d of %d\tStrength: %d" 
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
        print ("%s got %d experience!" % (self.name, self.xp))

        if self.xp > self.nextlvl:
            self.level_up()


    def level_up(self):
        hpgain = 10
        stronkgain = 4
        smrtgain = 3

        self.maxhp += hpgain
        self.stronk += stronkgain
        self.smart += smrtgain
        self.rest()
            
        print("%s Leveled up! Gained %d HP, %d str, %d int" % (self.name, hpgain, stronkgain, smrtgain))
        print (self)

    def attack(self, target):
        #TODO: Randomized damage
        if target:
            damage = random.randint(1, self.stronk)
            target.hp -= damage
            print("%s hit %s for %d damage! Target has %d hp left" %(self.name, target.name, damage, target.hp))

            if target.hp <= 0:
                self.get_experience(10)
                self.target = None

    def defend(self, target):
        #TODO: Some sort of block\damage reduction
        pass

    def rest(self):
        self.hp = self.maxhp
        print("%s rested to full!" % self.name)

    def heal(self):
        #TODO: Some sort of heal
        pass

    def tick(self):
        if (self.is_alive()):
            if self.target:   
                self.attack(self.target)
            else:
                self.target = False

        else:
            print("%s has been killed!" %self.name)
            self.alive = False