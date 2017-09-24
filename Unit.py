import random

class Unit():

    def __init__(self, name, hp, stronk, smart):
        self.name = name
        self.hp = hp
        self.maxhp = hp
        self.stronk = stronk
        self.smart = smart
        self.target = None
        self.cur_fight = None
        self.alive = True
        

    def __str__(self):
        return("Name: %s \t Health: %d of %d \t Strength: %d" %(self.name, self.hp, self.maxhp, self.stronk))

    def get_target(self, target):
        print("%s looks towards %s" %(self.name, target.name))
        self.target = target

    def search_target(self, targetlist):
        
            potentialtarget = targetlist[0]
            lowesthp = targetlist[0].hp
            for i in targetlist:
                if i.hp < lowesthp:
                    potentialtarget = targetlist[i]
                    lowesthp = targetlist[i].hp
        
            self.get_target(potentialtarget)
        
    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        #TODO: Randomized damage
        if target:
            damage = random.randint(1, self.stronk)
            target.hp -= damage
            print("%s hit %s for %d damage! Target has %d hp left" %(self.name, target.name, damage, target.hp))

            if target.hp < 0:
                self.target = False

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