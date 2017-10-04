from common import *
from units import *


class Fight():
    """Class for fights between two parties"""
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
        #TODO: IMPLEMENT DIFFICULTY 
        for x in range(self.difficulty):
            name = random.choice(Baddienames)
            hp = random.randint(BAD_HP_LO, BAD_HP_HI)
            stronk = random.randint(4, 7)
            self.baddieparty.join_party(Baddie(name, self.baddieparty, hp, stronk))

    def fight_print(self, sentence, fg=None):
        self.heroparty.print_t(sentence)

    def prepareforbattle(self):
        """Initial start of a battle"""
        self.fight_print("A FIGHT APPEARS!")
        self.fight_print("Attacking forces :")
        self.heroparty.partyprep(self, self.baddieparty)

        self.fight_print("\nOpposing forces :")
        self.baddieparty.partyprep(self, self.heroparty)


    def loss(self):
        self.fight_print("Thats a loss.. Remaining units:")
        for unit in self.baddieparty.members:
            print(unit)


    def victory(self):
        self.fight_print("Victory!! \nVictors of this battle:")

        for unit in self.heroparty.members:
            self.fight_print(unit)

        self.heroparty.team_getexp(1)


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
