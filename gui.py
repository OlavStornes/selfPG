import tkinter as tk
import main 
import random



class Party_gui(tk.Frame):
    def __init__(self, master=None, maingame=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("selfRPG")
        self.maingame = maingame


        
        #self.test_createparty()
        self.createWidgets()
        self.createText()
        #self.update_partyframe()
        print("initialised")

    def tick(self):
        self.update_idletasks()
        self.update()
        self.after(10, self.master.tick)

    def test_damagerandom(self):
        dude = random.choice(self.party.members)
        dude.hp -= 10
        self.print_text("Attacked someone!\n")
        


    def test_createparty(self):
        self.party = main.Party()
        self.party.join_party(main.Unit("Stronk", 20, 8, 1))

    def test_herojoin(self):
        name = random.choice(main.Baddienames)
        hp = random.randint(10, 20)
        stronk = random.randint(4, 7)
        self.party.join_party(main.Unit(name, hp, stronk, 0))

        self.T.insert(tk.END, name + " Joined the party!\n")

        self.update_partyframe()
        
    def print_text(self, string):
        self.T.insert(tk.END, string)

    def update_partyframe(self):
        
        
        for i, npc in enumerate(self.maingame.heroparty.members):
            tk.Label(self, text=npc, background="gray50").grid(row=i, column=0, sticky="NW",ipadx=20)
        self.after(1000, self.update_partyframe)


    def createText(self):
        self.T = tk.Text(self, height=20, width=50)
        self.T.grid(row=0, column=1, rowspan= 20)
        self.T.insert(tk.END, "Hello Party-log\n")

    def say_hi(self):
        print ("hi there, everyone!")

    def insert_txt(self):
        self.T.insert(tk.END, "hello team\n")






    def createWidgets(self):
        buttonframe = tk.Frame(self)
        buttonframe.grid(row = 0, column =2, rowspan=2)


        tk.Button(buttonframe, text="QUIT", fg="red", command=self.quit).pack()
        tk.Button(buttonframe, text="joinhero", command=self.test_herojoin).pack()
        #tk.Button(buttonframe, text="test", command=self.create_hero).pack()








if __name__ == "__main__":
    root = Party_gui()


    root.mainloop()