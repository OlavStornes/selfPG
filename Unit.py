import random

class Unit():

    def __init__(self, name, hp, stronk, smart):
        self.name = name
        self.hp = hp
        self.maxhp = hp
        self.stronk = stronk
        self.smart = smart
        self.target = None
        self.alive = True
        

    def __str__(self):
        return("Name: %s \t Health: %d of %d \t Strength: %d" %(self.name, self.hp, self.maxhp, self.stronk))

    def get_target(self, target):
        print("%s looks towards %s" %(self.name, target.name))
        self.target = target
        
    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        #TODO: Randomized damage
        if target:
            damage = random.randint(1, self.stronk)
            target.hp -= damage
            print("%s hit %s for %d damage!" %(self.name, target.name, damage))
        else:
            print("No target in sight!")

    def defend(self, target):
        #TODO: Some sort of block\damage reduction
        pass

    def heal(self):
        #TODO: Some sort of heal
        pass

    def tick(self):
        if (self.is_alive()):    
            self.attack(self.target)

        else:
            print("%s has been killed!" %self.name)
            self.alive = False