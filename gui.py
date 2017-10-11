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
        self.init_detailedstats()
        #self.statbox = tk.Label(self, textvariable=self.char_var).pack()
        #tk.Button(self, text="DB: LeVEL UP", command=character.level_up).pack() 
        self.tick_update()

    def update_gui(self):
        
        name = self.character.name + "\n"
        hp = str(self.character.hp) + "/" + str(self.character.maxhp)+ "\n"
        lvl =  str(self.character.lvl)+ "\n"
        exp =  str(self.character.exp)+ "\n"
        nextlvl = str(self.character.nextlvl)+ "\n"
        stronk = str(self.character.stronk)+ "\n"
        smart = str(self.character.smart)+ "\n"
        party = str(self.character.party.partyname)

        varstring = name + hp + lvl + exp + nextlvl + stronk + smart + party

        self.char_var.set(varstring)

    def init_detailedstats(self):

        #self.statframe = tk.LabelFrame(self, text="STATS", labelanchor="n").pack()
        statvar = ttk.Label(self, textvariable=self.char_var).grid(row=0, column=1)

        staticstring = "Name: \n HP: \n Lvl: \n Experience: \n Next level: \n Stronk: \n Smart: \n Partyname:"
        
        statname = ttk.Label(self, text=staticstring, justify="right").grid(row=0, column=0)
        


    def tick_update(self):
        self.update_gui()
        self.after(1000, self.tick_update)



class Party_gui(tk.Frame):
    def __init__(self, master, party):
        tk.Frame.__init__(self, master)
        self.pack()
        self.init_widgets()
        self.party = party
        self.createText_log()
        self.create_partyframe()
        self.create_baddieframe()
        self.create_statusbar()
        self.baddieframe = None

        self.tick()

        
    def print_log(self, string):
        self.T_log.insert(tk.END, string)

    def insert_txt(self):
        print(self.party.members)

    def open_charwindow(self, event):

        index = self.partyframe.nearest(event.y)
        top = tk.Toplevel(self)
        Character_gui(top, self.party.members[index])



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

    def createText_log(self):
        """Create a log for party-related stuff"""

        self.T_log = tk.Text(self, height=LOG_HEIGHT, width=LOG_WIDTH)
        self.T_log.grid(row=LOG_ROW, column=LOG_COL, rowspan= LOG_ROWSPAN)
        self.T_log.insert(tk.END, "Hello Party-log\n")

        self.party.log = self.T_log


    def init_widgets(self):
        buttonframe = tk.Frame(self)
        buttonframe.grid(row = BUT_FRAME_ROW, column = BUT_FRAME_COL, rowspan=BUT_ROWSPAN)


        tk.Button(buttonframe, text="Placeholder button", fg="red").pack()

    def update_gui(self):
        """Update gui with all elements"""
        self.update_statusbar()
        self.update_partylist(self.partyframe, self.party.members, self.pframe_var)

        if self.party.cur_fight:
            self.update_partylist(self.baddielist, self.party.cur_fight.baddieparty.members, self.bframe_var)
            


    def update_partylist(self, listbox, partylist, party_string):
        listbox.config(height=len(partylist),
                        width=45)
        party_string.set(partylist)
        

    def update_statusbar(self):
        self.statusbar_var.set(str(self.party.partyname) + ": " + str(self.party.activity))

    def tick(self):
        """Main-loop with ticks"""
        self.update_gui()
        self.after(GUI_UPDATE_RATE, self.tick)

##########################################################################


class Main_gui(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.debug_tick = tk.IntVar()
        self.pack()
        self.allparties = []
        self.alltowns = []
        self.init_widgets()
        self.init_menu()
        self.init_textlog()
        self.init_partyoverview()
        self.init_minimap()

        #Start with one town existing
        self.createtown_random()





    def init_minimap(self):
        self.minimap = tk.Canvas(self, bg="black", width=MAP_WIDTH, height=MAP_HEIGHT)
        self.minimap.grid(row = 0, column=3)
        self.blip_dict = {}


    def minimap_createblip(self, obj):
        """Returns an integer which is a type-ID for this blip on the minimap"""

        testframe = tk.Frame(None, relief="flat")
        if isinstance(obj, m.Party):
            tk.Label(testframe, text="-X-", bg="black", fg="white").grid(row=1)
        elif isinstance(obj, m.Town):
            tk.Label(testframe, bitmap="info", bg="black", fg="white").grid(row=1)

        minimapID = self.minimap.create_window(obj.pos.x, obj.pos.y, window=testframe)

        self.blip_dict[obj] = minimapID

    def minimap_removeblip(self, obj):
        """Remove a blip from the map"""
        minimapID = self.blip_dict[obj]
        if isinstance(obj, m.Party):
            self.minimap.delete(minimapID)
            del self.blip_dict[obj]
        elif isinstance(obj, m.Town):
            print("Removal of a town is not yet implemented")

    def update_minimap(self):
        """Update map coordinates"""
        for obj, map_id in self.blip_dict.items():
            self.minimap.coords(map_id, obj.pos.x, obj.pos.y)

    def init_partyoverview(self):
        """Create a frame where parties go"""
        self.allparty_var = tk.StringVar()
        self.partyframe = tk.Listbox(self, 
                        bg="green",
                        width=60,
                        height=0,
                        listvariable=self.allparty_var,
                        activestyle="dotbox",
                        exportselection=0
                        )

        self.allparty_var.set(self.allparties)
        self.partyframe.bind("<Button-1>", func=self.open_partywindow)

        self.partyframe.grid(row=0 ,column=0, rowspan=10, sticky=tk.N)

    def init_textlog(self):
        """Create a log for main-related stuff"""

        self.Main_log = tk.Text(self, height=LOG_HEIGHT, width=LOG_WIDTH)
        self.Main_log.grid(row=3, column=3, rowspan= LOG_ROWSPAN)
        self.Main_log.insert(tk.END, "Welcome to selfRPG\n")

    def print_mainlog(self, string):
        self.Main_log.insert(tk.END, string + "\n")

    def init_menu(self):
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        #filemenu.add_command(label="Open", command=lambda: print("This feature isnt implemented yet"))
        #filemenu.add_command(label="DEBUG:recruit", command=self.test_createparty)
        #filemenu.add_command(label="Start", command=self.test_tick)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)


        self.master.config(menu=menubar)

    def init_widgets(self):

        buttonframe = tk.Frame(self)
        buttonframe.grid(row=6, column=0, sticky="SE")


        tk.Button(buttonframe, text="QUIT", fg="red", command=self.quit).pack()
        tk.Button(buttonframe, text="START", fg="green", command=self.test_tick).pack()
        tk.Button(buttonframe, text="Createparty", fg="blue", command=self.test_createparty).pack()
        tk.Button(buttonframe, text="Create town", fg="blue", command=self.createtown_random).pack()
        
        self.debug_tick.set(1)
        tk.Checkbutton(buttonframe, text="DB: AUTOTICK", variable=self.debug_tick).pack()

    def open_partywindow(self, event):
        index = self.partyframe.nearest(event.y)
        top = tk.Toplevel(self)
        tmpgui = Party_gui(top, self.allparties[index])




    def test_createparty(self):
        """DEBUG: Creates a party for testing purposes"""
        party = m.Party()

        party.join_party(m.Fighter("Stronk1"))
        party.join_party(m.Fighter("Stronk2"))

        party.test_gettownmap(self.alltowns)
        self.print_mainlog("%s is attempting the life of adventurers!" %(party.partyname))
        self.minimap_createblip(party)
        self.allparties.append(party)

    def createtown_random(self):
        """DEBUG: Create a random persistent town"""
        town = m.Town()
        town.name = town.name + str(len(self.alltowns))
        self.print_mainlog("A new town, %s, appeared at %d,%d!" %(town.name, town.pos.x, town.pos.y))
        self.minimap_createblip(town)
        self.alltowns.append(town)

    def update_partylist(self):
        self.partyframe.config(height=len(self.allparties),width=60)

        self.allparty_var.set(self.allparties)


    def update_gui(self):
        self.update_partylist()
        self.update_minimap()
        
    def test_tick(self):
        """Main-loop with ticks"""
        for party in self.allparties:
            if party.team_alive():
                party.tick()
            else:
                self.minimap_removeblip(party)
                self.allparties.remove(party)
        self.update_gui()


        if self.debug_tick.get():
            self.after(GUI_UPDATE_RATE, self.test_tick)

if __name__ == "__main__":
    game = Main_gui()
    game.mainloop()