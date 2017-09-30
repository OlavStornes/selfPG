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
        self.test_createparty()

        self.update_gui()

    def test_fight(self):
        self.party.activity = a.Dungeon(self.party, TEST_ROOMS)

    def test_createparty(self):
        """DEBUG: Creates a party for testing purposes"""

        self.party.join_party(m.Unit("Stronk", self.party, 20, 8, 1))

        
    def print_log(self, string):
        self.T_log.insert(tk.END, string)

    def update_statusbar(self):
        self.statusbar = tk.Label(self, text=self.party.activity, bg="green").grid(row=0, column=1)

    def update_partyframe(self):
        """Updates party in GUI"""
        #self.statusbar = tk.Label(self, text=self.party.activity).grid(row=0, column=1)
        currentrow = 0
        for i, npc in enumerate(self.party.members):
            tk.Label(self, text=npc, background=PARTY_BG).grid(row=i, column=PARTY_COL, sticky="NW",ipadx=20)
            currentrow = i
        
        currentrow +=1
        
        if self.party.cur_fight:
            for i_2, npc in enumerate(self.party.cur_fight.baddieparty.members):
                tk.Label(self, text=npc, background=BADDIE_BG).grid(row=(i_2+currentrow), column=PARTY_COL, sticky="NW",ipadx=20) 

    def test_tick(self):
        """Main-loop with ticks"""
        self.party.tick()
        self.update_gui()
        self.after(GUI_UPDATE_RATE, self.test_fight)


    def update_gui(self):
        """Update gui with all elements"""
        self.update_statusbar()
        self.update_partyframe()



    def createText_log(self):
        """Create a log for party-related stuff, plus a scrollwheel"""

        self.T_log = tk.Text(self, height=LOG_HEIGHT, width=LOG_WIDTH)
        self.T_log.grid(row=1, column=1, rowspan= 20)
        self.T_log.insert(tk.END, "Hello Party-log\n")

        self.scroll = tk.Scrollbar(self, command=self.T_log.yview)
        self.scroll.grid(row=LOG_ROW, column= LOG_COL, rowspan=LOG_ROWSPAN)

        #Need to configure this after a scrollwheel is inited
        self.T_log.config(yscrollcommand=self.scroll)


    def insert_txt(self):
        self.T_log.insert(tk.END, "hello team\n")



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