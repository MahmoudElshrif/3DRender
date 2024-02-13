from testclasses import *
from pages import *
import customtkinter as ct
import time

class App:
    
    def __init__(self,master):
        self.master = master
        self.master.geometry("900x600")
        self.master.grid_rowconfigure(0,weight = 1)
        self.master.grid_columnconfigure(0,weight = 1)
        self.master.grid_propagate(False)
        
        self.manger = PagesManger(self.master)


root = ct.CTk()
root.title("Control")
app = App(root)
root.mainloop()
