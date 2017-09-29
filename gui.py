import tkinter as tk
import main 



class Party_gui(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("selfRPG")

        self.create_partyframe()
        self.createWidgets()
        self.createText()


    def create_partyframe(self):
        frame = tk.Frame()
        frame.pack({"side": "left"})

        for i in range(5):
            b = tk.Button(frame)
            b["text"] = "YO"
            b.pack()


    def createText(self):
        self.T = tk.Text(self, height=20, width=50)
        self.T.pack()
        self.T.insert(tk.END, "Just a text Widget\nin two lines\n")

    def say_hi(self):
        print ("hi there, everyone!")

    def insert_txt(self):
        self.T.insert(tk.END, "hello team\n")



    def createWidgets(self):
        QUIT = tk.Button(self)
        QUIT["text"] = "QUIT"
        QUIT["fg"]   = "red"
        QUIT["command"] =  self.quit

        QUIT.pack()
        

        hi_there = tk.Button(self)
        hi_there["text"] = "Hello",
        hi_there["command"] = self.say_hi

        hi_there.pack({"side": "right"})

        insert_txt = tk.Button(self)
        insert_txt["text"] = "insert",
        insert_txt["command"] = self.insert_txt
        insert_txt.pack()








if __name__ == "__main__":
    root = Party_gui()

    root.mainloop()