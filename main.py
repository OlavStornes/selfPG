import events as m
import activities as a
from common import *
from db_api import *
from time import sleep


class Game():
    def __init__(self, master=None):
        self.db = Database()

        self.tick_rate = GUI_UPDATE_RATE
        self.allparties = []
        self.alltowns = []

        # Start with one town existing
        self.createtown_random()

    def init_minimap(self):
        self.minimap = tk.Canvas(
            self, bg="black", width=MAP_WIDTH, height=MAP_HEIGHT)
        self.minimap.grid(row=0, column=3)
        self.blip_dict = {}

    def print_mainlog(self, string):
        print (string)


    def update_tickspeed(self, tickspeed):

        self.tick_rate = tickspeed


    def test_createparty(self):
        """DEBUG: Creates a party for testing purposes"""
        party = m.Party()

        party.join_party(m.Fighter("Stronk1"))
        party.join_party(m.Tank("Tankie"))

        party.test_gettownmap(self.alltowns)
        self.print_mainlog(
            "%s is attempting the life of adventurers!" % (party.partyname))
        self.allparties.append(party)

    def createparty_fromtown(self, town):
        """Creates a party inside a town"""
        party = m.Party(point=town.pos)

        party.join_party(m.Fighter("Stronk1"))
        party.join_party(m.Tank("Tankie"))

        town.party_queue -= 1

        party.test_gettownmap(self.alltowns)
        self.print_mainlog(
            "%s is attempting the life of adventurers!" % (party.partyname))
        self.allparties.append(party)

    def createtown_random(self):
        """Create a random persistent town"""
        town = m.Town()
        town.name = town.name + str(len(self.alltowns))
        self.print_mainlog(
            "A new town, %s, appeared at %d,%d!" %
            (town.name, town.pos.x, town.pos.y)
        )
        self.alltowns.append(town)

    def test_tick(self):
        """Main-loop with ticks"""
        for party in self.allparties:
            if party.team_alive():
                party.tick()
            else:
                self.allparties.remove(party)

        for town in self.alltowns:
            town.tick()
            if town.party_queue:
                self.createparty_fromtown(town)

    def mainloop(self):
        while True:
            self.test_tick()
            self.db.insert_table_parties(self.allparties)
            sleep(self.tick_rate)
            




if __name__ == "__main__":
    game = Game()
    game.mainloop()
