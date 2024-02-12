import customtkinter as ct
from prototype import *

def main_frame(self,root):
    frame = ct.CTkFrame(root,fg_color="transparent")
    return frame
    
def button(root,gridx,gridy,text,font_size = 16,width = 200,height = 50,padx = 20,pady = 10,command = lambda : print("test")):
    btn = ct.CTkButton(root,text = text,font = ("",font_size),width = width,height = height,command = command)
    btn.grid(row = gridx,column = gridy,padx = padx,pady = pady)
    return btn   

def header(root,text,gridx = 0,gridy = 0,font_size = 52,pady = (0,50),padx = 20):
    text = ct.CTkLabel(root,text = text,font = ("",font_size))
    text.grid(row = gridx,column = gridy,padx = padx,pady = pady)
    return text


class Page(ct.CTkFrame):
    def __init__(self, master, manger, *args, **kwargs):
        self.master = master
        self.manger = manger
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="transparent")
    
    def enter(self):
        self.grid(row=0,column=0)
        
        self.manger.current = self
        
    def goto(self,nextpage):
        
        self.manger.pages[nextpage].enter()
        
        self.grid_forget()
        
    
        
   
    
    


class Login(Page):
    def textbox_enter(self,event,button):
        button.invoke()
        return ("break")
    
    def textbox_tab(self,event):
        event.widget.tk_focusNext ().focus ()
        return ("break")
    
    def __init__(self,master,manger,*args,**kwargs):
        super().__init__(master,manger,*args,**kwargs)
            
        self.manger = manger
        header(self,"Sign in...")
        
        input = ct.CTkFrame(self)
        input.grid(row=1,column=0)
        
        self.wrongpassword = None
        def checkpasswrod(id, password,student):
            if(student):
                user = Student(id)
            else:
                user = Control(id)
            if(user.checkpassword(password)):
                self.manger.user = user
                if(student):
                    self.goto("Student_menu")
                else:
                    self.goto("Control_menu")
            else:
                self.wrongpassword = ct.CTkLabel(self,text = "Wrong id or password",text_color="red")
                self.wrongpassword.grid(row = 2,column = 0)
        
        
        ct.CTkLabel(input,text = "ID",anchor="w").grid(row = 0,column = 0)
        id = ct.CTkTextbox(input,height = 30,width = 200)
        id.bind("<Return>", self.textbox_tab)
        id.bind("<Tab>", self.textbox_tab)
        id.grid(row = 1,column = 0)
        
        self.id = id
        
        ct.CTkLabel(input,text = "Password").grid(row = 2,column = 0)
        
        password = ct.CTkTextbox(input,height = 30,width = 200)
        password.bind("<Return>", lambda x : self.textbox_enter(x,studentlogin))
        password.bind("<Tab>", self.textbox_tab)
        password.grid(row = 3,column = 0,padx = 20)
        
        self.password = password
        
        soc = ct.CTkFrame(input,fg_color="transparent") #soc = Student or Control
        soc.grid(row = 4,column = 0)
        
        studentlogin = button(soc,0,0,"Student login",width = 90,height=30,padx=5,command=lambda: checkpasswrod(id.get("1.0","end").strip(),password.get("1.0","end").strip(),True))    
        controllogin = button(soc,0,1,"Control login",width = 90,height=30,padx=5,command=lambda: checkpasswrod(id.get("1.0","end").strip(),password.get("1.0","end").strip(),False))    
        
        back = button(input,5,0,"exit",width = 215,height=30,pady=(3,20),command = lambda: exit()) 
        back.configure(fg_color="red")
        back.configure(hover_color="darkred")
        

    def goto(self,nextpage):
        if(self.wrongpassword):
            self.wrongpassword.grid_forget()
        self.id.delete("1.0","end")
        self.password.delete("1.0","end")
        
        super().goto(nextpage)
        

#Student Pages--------------------------------------------------------------------
class Student_menu(Page):
    def __init__(self, master, manger, *args, **kwargs):
        super().__init__(master, manger, *args, **kwargs)
        
        self.header = header(self,"Welcome, ")
        
        f = ct.CTkFrame(self)
        f.grid(row=1,column=0)
        
        editcourse = button(f,0,0,"Courses and Group")
        news = button(f,1,0,"News")
        back = button(f,2,0,"login screen",command = lambda:self.goto("Login"))
        back.configure(fg_color = "red",hover_color = "darkred")
    
    def enter(self):
        self.header.configure(text="Welcome, " + self.manger.user.name)
        super().enter()
        
#------------------------------------------------------------------------------------

#Control Pages------------------------------------------------------------------------
class Control_menu(Page):
    def __init__(self, master, manger, *args, **kwargs):
        super().__init__(master, manger, *args, **kwargs)
        
        self.header = header(self,"Welcome, ")
        
        f = ct.CTkFrame(self)
        f.grid(row=1,column=0)
        
        editcourse = button(f,0,0,"Manage Students")
        news = button(f,1,0,"Add News")
        back = button(f,2,0,"login screen",command = lambda:self.goto("Login"))
        back.configure(fg_color = "red",hover_color = "darkred")
    
    def enter(self):
        self.header.configure(text = "Welcome, " + self.manger.user.name)
        
        super().enter()


class PagesManger:
    def __init__(self,master) -> None:
        self.pages = {}
        self.current = None
        self.user = None
        
        for i in [Login, Student_menu, Control_menu]:
            self.pages[i.__name__] = i(master,self)
        
        self.pages["Login"].enter()