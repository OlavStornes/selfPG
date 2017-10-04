import tkinter as tk
import tkinter.ttk as ttk
import events as m
import activities as a
import random
from common import *

class Character_gui(tk.Frame):
    def __init__(self, master, character):
        tk.Frame.__init__(self, master, borderwidth=5, relief='groove')
        self.pack()
        self.character = character

        self.char_var = tk.StringVar()
        
        self.statbox = tk.Label(self, textvariable=self.char_var).pack()

        self.tick_update()



    def update_gui(self):
        
        self.char_var.set(self.character)

    def tick_update(self):
        self.update_gui()
        self.after(1000, self.tick_update)



class Party_gui(tk.Frame):
    def __init__(self, master, party):
        tk.Frame.__init__(self, master)
        self.pack()
        self.debug_tick = tk.IntVar()

        self.init_widgets()
        self.party = party
        self.createText_log()
        self.create_partyframe()
        self.create_baddieframe()
        self.create_statusbar()

        self.baddieframe = None

        self.test_tick()


    def test_fight(self):
        self.party.activity = a.Dungeon(self.party, TEST_ROOMS)
        
    def print_log(self, string):
        self.T_log.insert(tk.END, string)

    def update_partylist(self, listbox, partylist, party_string):
        listbox.config(height=len(partylist),
                        width=45)
        party_string.set(partylist)
        

    def update_statusbar(self):
        self.statusbar_var.set(self.party.activity)

    def create_statusbar(self):
        self.statusbar_var = tk.StringVar()
        self.statusbar = tk.Label(self, textvariable=self.statusbar_var, bg="darkgreen").grid(row=0, column=1)

    def create_partyframe(self):
        """Create a frame where partymembers go"""
        self.pframe_var = tk.StringVar()
        self.partyframe = tk.Listbox(self, 
                        bg="green",
                        width=0,
                        height=0,
                        listvariable=self.pframe_var,
                        activestyle="dotbox",
                        exportselection=0
                        )

        self.pframe_var.set (self.party.members)
        self.partyframe.bind("<Button-1>", func=self.open_charwindow)

        self.partyframe.grid(row=1 ,column=0, rowspan=MAX_PARTYSIZE, sticky=tk.N)



    def create_baddieframe(self):

        self.bframe_var = tk.StringVar()
        self.baddielist = tk.Listbox(self, 
                                    bg="red",
                                    width=0,
                                    height=0,
                                    listvariable=self.bframe_var)

        self.baddielist.grid(row=2 ,column=0, rowspan=4, sticky=tk.N)


    def test_tick(self):
        """Main-loop with ticks"""
        self.party.tick()
        self.update_gui()

        
        if self.debug_tick.get():
            self.after(GUI_UPDATE_RATE, self.test_tick)



    def update_gui(self):
        """Update gui with all elements"""
        self.update_statusbar()
        self.update_partylist(self.partyframe, self.party.members, self.pframe_var)

        if self.party.cur_fight:
            self.update_partylist(self.baddielist, self.party.cur_fight.baddieparty.members, self.bframe_var)
            




    def createText_log(self):
        """Create a log for party-related stuff, plus a scrollwheel"""

        self.T_log = tk.Text(self, height=LOG_HEIGHT, width=LOG_WIDTH)
        self.T_log.grid(row=LOG_ROW, column=LOG_COL, rowspan= LOG_ROWSPAN)
        self.T_log.insert(tk.END, "Hello Party-log\n")

        self.party.log = self.T_log

        #self.scroll = tk.Scrollbar(self, command=self.T_log.yview)
        #self.scroll.grid(row=SCROLL_ROW, column= SCROLL_COL, rowspan=LOG_ROWSPAN, sticky=tk.N + tk.S)

        #Need to configure this after a scrollwheel is inited
        #self.T_log.config(yscrollcommand=self.scroll)


    def insert_txt(self):
        print(self.party.members)

    def open_charwindow(self, event):

        index = self.partyframe.nearest(event.y)
        top = tk.Toplevel(self)
        Character_gui(top, self.party.members[index])



    def init_widgets(self):
        buttonframe = tk.Frame(self)
        buttonframe.grid(row = BUT_FRAME_ROW, column = BUT_FRAME_COL, rowspan=BUT_ROWSPAN)


        tk.Button(buttonframe, text="QUIT", fg="red", command=self.quit).pack()
        tk.Button(buttonframe, text="START", fg="green", command=self.test_tick).pack()
        tk.Button(buttonframe, text="testfight", command=self.test_fight).pack()
        tk.Button(buttonframe, text="testtick", command=self.test_tick).pack()
        tk.Checkbutton(buttonframe, text="DB: AUTOTICK", variable=self.debug_tick).pack()


##########################################################################


class Main_gui(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.allparties = []
        self.init_menu()
        self.init_textlog()
        self.init_partyoverview()



        tk.Button(self, text="test_go_party_one", command=self.test_go_party_one).grid()
        tk.Button(self, text="create_party", command=self.test_createparty).grid()

    def init_partyoverview(self):
        """Create a frame where partymembers go"""
        self.allparty_var = tk.StringVar()
        self.partyframe = tk.Listbox(self, 
                        bg="green",
                        width=0,
                        height=0,
                        listvariable=self.allparty_var,
                        activestyle="dotbox",
                        exportselection=0
                        )

        self.allparty_var.set(self.allparties)
        self.partyframe.bind("<Button-1>", func=self.open_partywindow)

        self.partyframe.grid(row=5 ,column=0, rowspan=10, sticky=tk.N)

    def open_partywindow(self, event):
        index = self.partyframe.nearest(event.y)
        top = tk.Toplevel(self)
        Party_gui(top, self.allparties[index])

    def init_textlog(self):
        """Create a log for main-related stuff"""

        self.Main_log = tk.Text(self, height=LOG_HEIGHT, width=LOG_WIDTH)
        self.Main_log.grid(row=3, column=3, rowspan= LOG_ROWSPAN)
        self.Main_log.insert(tk.END, "Welcome to selfRPG\n")

    def init_menu(self):
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        #filemenu.add_command(label="Open", command=lambda: print("This feature isnt implemented yet"))
        #filemenu.add_command(label="DEBUG:recruit", command=self.test_createparty)
        #filemenu.add_command(label="Start", command=self.test_tick)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Button(self, text="testtick", command=self.test_tick).grid()

        self.master.config(menu=menubar)

    def test_go_party_one(self):

        self.partygui = tk.Toplevel(self)
        test = Party_gui(self.partygui, self.allparties[0])

    def update_partylist(self):
        self.partyframe.config(height=len(self.allparties),width=60)

        self.allparty_var.set(self.allparties)

    def update_gui(self):
        self.update_partylist()
        
    def test_tick(self):
        """Main-loop with ticks"""
        for party in self.allparties:
            party.tick()
        self.update_gui()

        self.after(GUI_UPDATE_RATE, self.test_tick)

    def test_createparty(self):
        """DEBUG: Creates a party for testing purposes"""
        party = m.Party()

        party.join_party(m.Unit("Stronk1", 20, 6, 1))
        party.join_party(m.Unit("Stronk2", 20, 6, 1))
        self.allparties.append(party)

if __name__ == "__main__":
    game = Main_gui()
    game.mainloop()