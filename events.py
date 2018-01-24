from common import *
from units import *

"""Events that happens during an activity. Short-term and resolved in a relatively quick matter"""

class Fight():
    """Class for fights between the hero-party and a baddie-party"""
    def __init__(self, heroes, difficulty):

        self.heroparty = heroes
        self.baddieparty = Party(heroes.log)
        self.difficulty = difficulty
        self.createbaddies()
        self.turn = 0
        self.prepareforbattle()


        #self.tick()



    def createbaddies(self):
        """Create enemies in a party"""
        #TODO: MORE VARIATION
        
        n_mobs = random.randint(1, self.difficulty)
        baddielvls = self.difficulty - n_mobs

        for x in range(n_mobs):
            name = random.choice(Baddienames)

            self.baddieparty.join_party(Baddie(name))

        for lvlgain in range(baddielvls):
            dude = random.choice(self.baddieparty.members)
            dude.level_up()
            dude.hp = dude.maxhp

    def fight_print(self, sentence):
        if sentence:
            self.heroparty.print_t(sentence)

    def prepareforbattle(self):
        """Initial start of a battle"""
        self.fight_print("A FIGHT APPEARS!")
        self.heroparty.partyprep(self, self.baddieparty)

        self.baddieparty.partyprep(self, self.heroparty)


    def loss(self):
        self.fight_print("Thats a loss.. Remaining units:")
        for unit in self.baddieparty.members:
            print(unit)


    def victory(self):
        self.fight_print("Victory!! ")

        self.heroparty.team_getexp(10)


    def endofbattle(self):

        if not self.baddieparty.team_alive():
            self.victory()

        elif not self.heroparty.team_alive():
            self.loss()
        self.heroparty.team_endoffight()

    def is_fight_active(self):
        return self.heroparty.team_alive() and self.baddieparty.team_alive()


    def tick(self):
        """Main loop inside a fight"""
        if self.heroparty.team_alive() and self.baddieparty.team_alive():
            self.fight_print("\nTURN %d" % self.turn)
            self.turn += 1
                    #HERO TURN
            self.heroparty.team_attack()
                    #BADDIE TURN

            self.baddieparty.team_attack()


        else:
            self.endofbattle()


##################################################
