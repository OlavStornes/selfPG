import tkinter as tk
import tkinter.ttk as ttk
import events as m
import activities as a
from common import *

# Gui.py:
# GUI-implementation which handles the main loop and everything mainly front-end


class Character_gui(tk.Frame):
    def __init__(self, master, character):
        tk.Frame.__init__(self, master, borderwidth=5, relief='groove')
        self.pack()
        self.master.title("Character sheet: %s" % (character.name))
        self.character = character
        self.char_var = tk.StringVar()
        self.init_detailedstats()
        self.init_charportrait()
        self.init_healthbar()
        #self.statbox = tk.Label(self, textvariable=self.char_var).pack()
        self.tick_update()

    def update_gui(self):
        """Update all variables in a character sheet"""
        name = self.character.name + "\n"
        hp = str(self.character.hp) + "/" + str(self.character.maxhp) + "\n"
        lvl = str(self.character.lvl) + "\n"
        exp = str(self.character.exp) + "\n"
        nextlvl = str(self.character.nextlvl) + "\n"
        stronk = str(self.character.stronk) + "\n"
        smart = str(self.character.smart) + "\n"
        party = str(self.character.party.partyname)

        varstring = name + hp + lvl + exp + nextlvl + stronk + smart + party

        self.char_var.set(varstring)
        self.hpbar_var.set(self.character.hp)

    def init_charportrait(self):
        """Creates a character portrait"""

        # as of now, classes should have images identical to their class name
        img_path = "img/portraits/%s.gif" % (
            str(self.character.__class__.__name__))

        try:
            self.portrait = tk.PhotoImage(file=img_path)
        except:
            self.portrait = tk.PhotoImage(file="img/portraits/GenericUnit.gif")

        portraitlabel = tk.Label(self, image=self.portrait)
        portraitlabel.grid(row=0, column=1)

    def init_detailedstats(self):

        self.statframe = tk.LabelFrame(self, text="STATS", labelanchor="n")
        statvar = ttk.Label(
            self.statframe, textvariable=self.char_var).grid(row=0, column=1)

        staticstring = "Name: \n HP: \n Lvl: \n Experience: \n Next level: \n Stronk: \n Smart: \n Partyname:"

        statname = ttk.Label(
            self.statframe,
            text=staticstring,
            justify="right"
        ).grid(row=0, column=0)
        self.statframe.grid(row=0, column=0, sticky="n")

    def init_healthbar(self):
        self.hpbar_var = tk.IntVar()
        self.hpbar = ttk.Progressbar(
            self,
            maximum=self.character.maxhp,
            mode="determinate",
            variable=self.hpbar_var
        )

        self.hpbar.grid(row=1, column=0, columnspan=2, sticky="WE")

    def tick_update(self):
        self.update_gui()
        self.after(1000, self.tick_update)


class Party_gui(tk.Frame):
    def __init__(self, master, party):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("Party status of: %s" % (party.partyname))
        self.init_widgets()
        self.party = party
        self.createtext_log()
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
        self.statusbar = tk.Label(
            self, textvariable=self.statusbar_var, fg="white", bg="darkgreen").grid(row=0, column=1)

    def create_partyframe(self):
        """Create a frame where partymembers go"""
        self.pframe_var = tk.StringVar()
        self.partyframe = tk.Listbox(
            self,
            bg="green",
            width=0,
            height=0,
            listvariable=self.pframe_var,
            activestyle="dotbox",
            exportselection=0
        )

        self.pframe_var.set(self.party.members)
        self.partyframe.bind("<Button-1>", func=self.open_charwindow)

        self.partyframe.grid(
            row=1, column=0, rowspan=MAX_PARTYSIZE, sticky=tk.N)

    def create_baddieframe(self):

        self.bframe_var = tk.StringVar()
        self.baddielist = tk.Listbox(
            self,
            bg="red",
            width=0,
            height=0,
            listvariable=self.bframe_var
        )

        self.baddielist.grid(row=2, column=0, rowspan=4, sticky=tk.N)

    def createtext_log(self):
        """Create a log for party-related stuff"""

        self.T_log = tk.Text(self, height=LOG_HEIGHT, width=LOG_WIDTH)
        self.T_log.grid(row=LOG_ROW, column=LOG_COL, rowspan=LOG_ROWSPAN)
        self.T_log.insert(tk.END, "Hello Party-log\n")

        self.party.log = self.T_log

    def init_widgets(self):
        buttonframe = tk.Frame(self)
        buttonframe.grid(
            row=BUT_FRAME_ROW,
            column=BUT_FRAME_COL,
            rowspan=BUT_ROWSPAN
        )

        tk.Button(
            buttonframe,
            text="Placeholder button",
            fg="red").pack()
        self.gold_var = tk.StringVar()
        tk.Label(buttonframe, textvariable=self.gold_var).pack()

    def update_gui(self):
        """Update gui with all elements"""
        self.update_statusbar()
        self.update_partylist(
            self.partyframe, self.party.members, self.pframe_var)

        if self.party.cur_fight:
            self.update_partylist(
                self.baddielist, self.party.cur_fight.baddieparty.members, self.bframe_var)

    def update_partylist(self, listbox, partylist, party_string):
        listbox.config(height=len(partylist), width=45)
        party_string.set(partylist)

    def update_statusbar(self):
        self.gold_var.set("Gold: " + str(self.party.gold))
        self.statusbar_var.set(
            str(self.party.partyname) +
            ": " +
            str(self.party.activity)
        )

    def tick(self):
        """Main-loop with ticks"""
        self.update_gui()
        self.after(self.master.master.tick_rate, self.tick)

##########################################################################


class Main_gui(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title(GAME_TITLE)
        self.auto_tick = tk.IntVar()
        self.tick_rate = GUI_UPDATE_RATE
        self.pack()
        self.allparties = []
        self.alltowns = []
        self.init_widgets()
        self.init_menu()
        self.init_textlog()
        self.init_partyoverview()
        self.init_minimap()

        # Start with one town existing
        self.createtown_random()
        self.init_townoverview()

    def init_minimap(self):
        self.minimap = tk.Canvas(
            self, bg="black", width=MAP_WIDTH, height=MAP_HEIGHT)
        self.minimap.grid(row=0, column=3)
        self.blip_dict = {}

    def init_townoverview(self):
        self.alltowns_var = tk.StringVar()
        self.townframe = tk.Listbox(
            self,
            bg="blue",
            fg="white",
            width=60,
            height=0,
            listvariable=self.alltowns_var,
            activestyle="dotbox",
            exportselection=0
        )

        self.townframe.grid(row=0, column=4, sticky="n")

        self.alltowns_var.set(self.alltowns)

    def minimap_createblip(self, obj):
        """Returns an integer which is a type-ID for this blip on the minimap"""

        # NOTE: Resizing or own images would be a good thing
        if isinstance(obj, m.Party):
            imagepath = "img/icons/cowled.png"

        elif isinstance(obj, m.Town):
            imagepath = "img/icons/village.png"

        # .subsample(2) #<-- shrink the image as of now
        image = tk.PhotoImage(file=imagepath)

        minimapID = self.minimap.create_image(
            obj.pos.x, obj.pos.y, image=image)

        # Must save the image as a reference. NOTE: Look into optimisations of icon storage
        self.blip_dict[obj] = (minimapID, image)

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
        # Blip_tuple containts a minimap_id and the image for given minimap_id-object
        for obj, blip_tuple in self.blip_dict.items():
            self.minimap.coords(blip_tuple[0], obj.pos.x, obj.pos.y)

    def init_partyoverview(self):
        """Create a frame where parties go"""
        self.allparty_var = tk.StringVar()
        self.partyframe = tk.Listbox(
            self,
            bg="green",
            fg="white",
            width=60,
            height=0,
            listvariable=self.allparty_var,
            activestyle="dotbox",
            exportselection=0
        )

        self.allparty_var.set(self.allparties)
        self.partyframe.bind("<Button-1>", func=self.open_partywindow)

        self.partyframe.grid(row=0, column=0, rowspan=10, sticky=tk.N)

    def init_textlog(self):
        """Create a log for main-related stuff"""

        self.Main_log = tk.Text(self, height=LOG_HEIGHT, width=LOG_WIDTH)
        self.Main_log.grid(row=3, column=3, rowspan=LOG_ROWSPAN)
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
        """Initialize a set of widgets"""
        buttonframe = tk.Frame(self)
        buttonframe.grid(row=6, column=0, sticky="SE")

        tk.Button(
            buttonframe,
            text="QUIT",
            fg="red",
            command=self.quit).pack()
        tk.Button(
            buttonframe,
            text="START",
            fg="green",
            command=self.test_tick).pack()
        tk.Button(
            buttonframe,
            text="Createparty",
            fg="blue",
            command=self.test_createparty).pack()
        tk.Button(
            buttonframe,
            text="Create town",
            fg="blue",
            command=self.createtown_random).pack()

        scale = tk.Scale(
            self,
            from_=1,
            to=GUI_UPDATE_RATE,
            orient="horizontal",
            command=self.update_tickspeed
        )
        scale.set(GUI_UPDATE_RATE)
        scale.grid(row=7, column=0, sticky="WE")

        self.auto_tick.set(1)
        tk.Checkbutton(
            buttonframe,
            text="DB: AUTOTICK",
            variable=self.auto_tick).pack()

    def update_tickspeed(self, tickspeed):

        self.tick_rate = tickspeed

    def open_partywindow(self, event):
        index = self.partyframe.nearest(event.y)
        top = tk.Toplevel(self)
        tmpgui = Party_gui(top, self.allparties[index])

    def test_createparty(self):
        """DEBUG: Creates a party for testing purposes"""
        party = m.Party()

        party.join_party(m.Fighter("Stronk1"))
        party.join_party(m.Tank("Tankie"))

        party.test_gettownmap(self.alltowns)
        self.print_mainlog(
            "%s is attempting the life of adventurers!" % (party.partyname))
        self.minimap_createblip(party)
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
        self.minimap_createblip(party)
        self.allparties.append(party)

    def createtown_random(self):
        """Create a random persistent town"""
        town = m.Town()
        town.name = town.name + str(len(self.alltowns))
        self.print_mainlog(
            "A new town, %s, appeared at %d,%d!" %
            (town.name, town.pos.x, town.pos.y)
        )
        self.minimap_createblip(town)
        self.alltowns.append(town)

    def update_partylist(self):
        self.partyframe.config(height=len(self.allparties), width=60)

        self.allparty_var.set(self.allparties)

    def update_townlist(self):
        self.townframe.config(height=len(self.alltowns), width=60)

        self.alltowns_var.set(self.alltowns)

    def update_gui(self):
        self.update_partylist()
        self.update_townlist()
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

        for town in self.alltowns:
            town.tick()
            if town.party_queue:
                self.createparty_fromtown(town)

        if self.auto_tick.get():
            self.after(self.tick_rate, self.test_tick)


if __name__ == "__main__":
    game = Main_gui()
    game.mainloop()
