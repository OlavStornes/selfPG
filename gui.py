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

        self.init_widgets()
        self.init_menu()
        self.createText_log()
        self.party = m.Party(self.T_log)
        self.test_createparty()
        self.create_partyframe()

        self.baddieframe = None


    def test_fight(self):
        self.party.activity = a.Dungeon(self.party, TEST_ROOMS)

    def test_createparty(self):
        """DEBUG: Creates a party for testing purposes"""

        self.party.join_party(m.Unit("Stronk1", self.party, 20, 6, 1))
        self.party.join_party(m.Unit("Stronk2", self.party, 20, 6, 1))

        
    def print_log(self, string):
        self.T_log.insert(tk.END, string)

    def update_statusbar(self):
        self.statusbar = tk.Label(self, text=self.party.activity, bg="darkgreen").grid(row=0, column=1)

    def update_partyframe(self, partylist, variable_array):
        """Updates party in GUI"""

        #Clean up partyframe
        for i in range(len(variable_array)):
            variable_array[i].set("")

        for i, npc in enumerate(partylist):
            variable_array[i].set(npc)


    def create_partyframe(self):
        """Create a frame where partymembers go"""
        #TODO: Try to create a child window for specific heroes
        self.pframe_var = tk.StringVar()
        self.partyframe = tk.LabelFrame(self, bg="green", text="Partymembers:")

        self.pframe_var_array = []


        for i in range(len(self.party.members)):
            self.pframe_var_array.append(tk.StringVar())
            tk.Label(self.partyframe, textvariable=self.pframe_var_array[i]).pack()


        self.partyframe.grid(row=0 ,column=0, rowspan=10)


    def create_baddieframe(self):

        self.bframe_var = tk.StringVar()
        self.baddieframe = tk.LabelFrame(self, bg="red", text="Enemies:")

        self.bframe_var_array = []


        for i in range(len(self.party.cur_fight.baddieparty.members)):
            self.bframe_var_array.append(tk.StringVar())
            tk.Label(self.baddieframe, textvariable=self.bframe_var_array[i]).pack()


        self.baddieframe.grid(row=10 ,column=0, rowspan=10)


    def test_tick(self):
        """Main-loop with ticks"""
        self.party.tick()
        self.update_gui()
        self.after(GUI_UPDATE_RATE, self.test_tick)


    def update_gui(self):
        """Update gui with all elements"""
        self.update_statusbar()
        self.update_partyframe(self.party.members, self.pframe_var_array)

        if self.party.cur_fight:
            if self.party.cur_fight.turn == 0:
                self.create_baddieframe()
            else:
                self.update_partyframe(self.party.cur_fight.baddieparty.members, self.bframe_var_array)
            




    def createText_log(self):
        """Create a log for party-related stuff, plus a scrollwheel"""

        self.T_log = tk.Text(self, height=LOG_HEIGHT, width=LOG_WIDTH)
        self.T_log.grid(row=LOG_ROW, column=LOG_COL, rowspan= LOG_ROWSPAN)
        self.T_log.insert(tk.END, "Hello Party-log\n")

        #self.scroll = tk.Scrollbar(self, command=self.T_log.yview)
        #self.scroll.grid(row=SCROLL_ROW, column= SCROLL_COL, rowspan=LOG_ROWSPAN, sticky=tk.N + tk.S)

        #Need to configure this after a scrollwheel is inited
        #self.T_log.config(yscrollcommand=self.scroll)


    def insert_txt(self):
        print(self.party.members)

    def init_widgets(self):
        buttonframe = tk.Frame(self)
        buttonframe.grid(row = BUT_FRAME_ROW, column = BUT_FRAME_COL, rowspan=BUT_ROWSPAN)


        tk.Button(buttonframe, text="QUIT", fg="red", command=self.quit).pack()
        tk.Button(buttonframe, text="START", fg="green", command=self.test_tick).pack()
        tk.Button(buttonframe, text="testfight", command=self.test_fight).pack()
        tk.Button(buttonframe, text="testprint", command=self.insert_txt).pack()

    def init_menu(self):
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        #filemenu.add_command(label="Open", command=lambda: print("This feature isnt implemented yet"))
        #filemenu.add_command(label="Save", command=lambda: print("hello"))
        filemenu.add_command(label="Start", command=self.test_tick)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.master.config(menu=menubar)




if __name__ == "__main__":
    game = Party_gui()
    game.mainloop()