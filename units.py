
import events as m
import activities as a
import tkinter as tk
from common import *
from ailment import *

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
        self.members = []
        self.killed = []
        self.inventory = []
        self.log = gui_log
        self.cur_fight = None
        self.activity = None
        self.townmap = None
        self.targetparty = None
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
        for npc in self.members:
            npc.target = None

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
    """The groundwork for every npc"""
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

        self.statuses = {}
        self.skills = {}

        self.maxmp = 100
        self.mana = self.maxmp

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
        self.maxhp += increase_stat_hp(self.statgrowth["hp"])
        self.stronk += increase_stat(self.statgrowth["stronk"])
        self.smart += increase_stat(self.statgrowth["smart"])

    def level_up(self):
        self.exp -= self.nextlvl
        self.lvl += 1

        #make an exponential growth of next lvl
        self.nextlvl = int(XP_BASE * (self.lvl ** XP_EXPONENT))

        self.increase_all_stat()
        self.print_t("%s Leveled up!" % (self.name))


    def attack(self, target):
        #TODO: Better randomized damage
        if target:
            damage = random.randint(int(self.stronk/2), self.stronk)
            target.defend(damage)
            self.print_t("%s hit %s for %d damage! Target has %d hp left" %(self.name, target.name, damage, target.hp))

            if target.hp <= 0:
                #Target is killed. Get some xp and remove target
                self.get_experience(int(target.lvl * 10))
                self.target = None

    def defend(self, damage):
        """Recieve damage from another target. NOTE: Some units can defend more effiecently than this"""
        self.hp -= damage

    def rest(self):
        self.hp = self.maxhp
        self.print_t("%s rested to full!" % self.name)

    def attack_tick(self, hostileparty):
        """Main logic for a basic physical attack"""
        if self.target:
            if self.target.is_alive():
                self.attack(self.target)
                return

        self.search_target(hostileparty)
        self.attack(self.target)

    def tick_statuses(self):
        """Tick and remove eventual status aliments that have occured"""
        #We cant iterate and delete from a dictionary at the same time
        done_statuses = []

        for key, status in self.statuses.items():
            status.tick()
            if status.rounds_left == 0:
                done_statuses.append(key)
        
        for expired in done_statuses:
            print(str(expired) + "is out of the system")
            del self.statuses[expired]

    def tick(self, hostileparty):
        self.tick_statuses()

        self.attack_tick(hostileparty)

class Fighter(Unit):
    """A fighter that specialies in melee. Stronk dude, but not so smart"""
    def __init__(self, name):
        Unit.__init__(self, name)
        self.statgrowth = {"hp": "med", "stronk": "high", "smart": "low"}


class Tank(Unit):
    """A large fighter that is more defensively capable. Doesnt hit as hard, but can taunt enemies"""
    def __init__(self, name):
        Unit.__init__(self, name)
        self.statgrowth = {"hp": "high", "stronk": "med", "smart": "low"}
        self.tauntcooldown = 10

    def taunt_unit(self, target):
        tmp = Taunt(target, self)
        target.statuses[tmp.statustype] = tmp
        self.tauntcooldown = 0

    def defend(self, damage):

        #The tank can handle some more hits
        #TODO: Make this a skill instead

        self.hp -= int(damage * 0.70)

    def tick(self, hostileparty):
        self.tauntcooldown += 1
        if self.tauntcooldown >= 20:
            target = random.choice(hostileparty.members)
            self.taunt_unit(target)
        else:
            self.attack_tick(hostileparty)



class Baddie(Unit):
    def __init__(self, name):
        Unit.__init__(self, name)
        #NOTE: For now they have an disadvantage
        self.hp = int(self.hp * 0.85)
        self.maxhp = self.hp
        self.stronk = int(self.stronk * 0.85)
        self.statgrowth = {"hp": "low", "stronk": "low", "smart": "low"}

    def search_target(self, hostileparty):
        """Enemy targeting: Find a random hero and hit him"""
        if hostileparty.team_alive():
            self.get_target(random.choice(hostileparty.members))

    def attack_tick(self, hostileparty):


        if TAUNT in self.statuses:
            self.get_target(self.statuses[TAUNT].target)
            #print("Taunted by" + str(self.target))
        else:
            self.search_target(hostileparty)
            
        self.attack(self.target)