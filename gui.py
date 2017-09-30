import tkinter as tk
import main as m
import random



class Party_gui(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("selfRPG")

        self.party = m.Party()

        self.test_createparty()
        self.createWidgets()
        self.createText_log()
        self.update_partyframe()

    def test_fight(self):
        self.party.activity = m.Dungeon(self.party, 2)

    def test_tick(self):
        self.party.tick()
        self.after(1000, self.test_tick)

    def test_damagerandom(self):
        dude = random.choice(self.party.members)
        dude.hp -= 10
        


    def test_createparty(self):

        self.party.join_party(m.Unit("Stronk", 20, 8, 1))

        
    def print_log(self, string):
        self.T_log.insert(tk.END, string)

    def update_partyframe(self):
        """Updates party in GUI"""
        for i, npc in enumerate(self.party.members):
            tk.Label(self, text=npc, background="gray50").grid(row=i, column=0, sticky="NW",ipadx=20)
        self.after(1000, self.update_partyframe)


    def createText_log(self):
        self.T_log = tk.Text(self, height=20, width=50)
        self.T_log.grid(row=0, column=1, rowspan= 20)
        self.T_log.insert(tk.END, "Hello Party-log\n")

    def insert_txt(self):
        self.T_log.insert(tk.END, "hello team\n")



    def createWidgets(self):
        buttonframe = tk.Frame(self)
        buttonframe.grid(row = 0, column =2, rowspan=2)


        tk.Button(buttonframe, text="QUIT", fg="red", command=self.quit).pack()
        tk.Button(buttonframe, text="testtick", command=self.test_tick).pack()
        tk.Button(buttonframe, text="testfight", command=self.test_fight).pack()



if __name__ == "__main__":
    game = Party_gui()


    game.mainloop()