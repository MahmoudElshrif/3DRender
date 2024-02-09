import customtkinter as ct
class App:
    def __init__(self,master):
        self.master = master
        self.master.geometry("900x600")
        self.switchpage(self.page1)
    
    def switchpage(self,page):
        for i in self.master.winfo_children():
            i.destroy()
        page()
    def page1(self):
        frame = ct.CTkFrame(self.master)
        frame.pack()
        
        button = ct.CTkButton(frame,text="page2",command=lambda: self.switchpage(self.page2))
        button.pack()
    
    def page2(self):
        frame = ct.CTkFrame(self.master)
        frame.pack()
        button = ct.CTkButton(frame,text="page1",command=lambda: self.switchpage(self.page1))
        button.pack()
        

root = ct.CTk()
a = App(root)
root.mainloop()