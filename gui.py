import tkinter as tk
import events as m
import activities as a
import random
from common import *



class Party_gui(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title(PARTY_TITLE)

        self.createWidgets()
        self.createText_log()
        self.party = m.Party(self.T_log)
        self.create_partyframe()
        self.test_createparty()

        #self.update_gui()

    def test_fight(self):
        self.party.activity = a.Dungeon(self.party, TEST_ROOMS)

    def test_createparty(self):
        """DEBUG: Creates a party for testing purposes"""

        self.party.join_party(m.Unit("Stronk1", self.party, 20, 8, 1))
        self.party.join_party(m.Unit("Stronk2", self.party, 20, 8, 1))

        
    def print_log(self, string):
        self.T_log.insert(tk.END, string)

    def update_statusbar(self):
        self.statusbar = tk.Label(self, text=self.party.activity, bg="green").grid(row=0, column=1)

    def update_partyframe(self):
        """Updates party in GUI"""

        partystring = ""
        for i in self.party.members:
            partystring += str(i) + "\n"

        self.pframe_var.set(partystring[:-1])   #<--- Dirty hack to slice last newline


    def create_partyframe(self):
        """Create a frame where partymembers go"""
        #TODO: Try to create a child window for spesific characters
        self.pframe_var = tk.StringVar()
        self.partyframe = tk.LabelFrame(self, bg="green", text="Partymembers:")
        tk.Label(self.partyframe, textvariable=self.pframe_var).pack()
        self.partyframe.grid(row=0 ,column=0, rowspan=10)


    def test_tick(self):
        """Main-loop with ticks"""
        self.party.tick()
        self.update_gui()
        self.after(GUI_UPDATE_RATE, self.test_tick)


    def update_gui(self):
        """Update gui with all elements"""
        self.update_statusbar()
        self.update_partyframe()



    def createText_log(self):
        """Create a log for party-related stuff, plus a scrollwheel"""

        self.T_log = tk.Text(self, height=LOG_HEIGHT, width=LOG_WIDTH)
        self.T_log.grid(row=LOG_ROW, column=LOG_COL, rowspan= LOG_ROWSPAN)
        self.T_log.insert(tk.END, "Hello Party-log\n")

        self.scroll = tk.Scrollbar(self, command=self.T_log.yview)
        self.scroll.grid(row=SCROLL_ROW, column= SCROLL_COL, rowspan=LOG_ROWSPAN)

        #Need to configure this after a scrollwheel is inited
        self.T_log.config(yscrollcommand=self.scroll)


    def insert_txt(self):
        print(self.party.members)

    def createWidgets(self):
        buttonframe = tk.Frame(self)
        buttonframe.grid(row = BUT_FRAME_ROW, column = BUT_FRAME_COL, rowspan=BUT_ROWSPAN)


        tk.Button(buttonframe, text="QUIT", fg="red", command=self.quit).pack()
        tk.Button(buttonframe, text="START", fg="green", command=self.test_tick).pack()
        tk.Button(buttonframe, text="testfight", command=self.test_fight).pack()
        tk.Button(buttonframe, text="testprint", command=self.insert_txt).pack()



if __name__ == "__main__":
    game = Party_gui()
    game.mainloop()