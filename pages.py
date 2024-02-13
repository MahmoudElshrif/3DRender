import customtkinter as ct
from testclasses import *

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
        
        editcourse = button(f,0,0,"Courses and Group",command=lambda:self.goto("Courses_menu"))
        news = button(f,1,0,"News")
        back = button(f,2,0,"login screen",command = lambda:self.goto("Login"))
        back.configure(fg_color = "red",hover_color = "darkred")
    
    def enter(self):
        self.header.configure(text="Welcome, " + self.manger.user.name)
        
        self.manger.pages["Courses_menu"].init_buttons()
        
        super().enter()
        
class Courses_menu(Page):
    def __init__(self, master, manger, *args, **kwargs):
        super().__init__(master, manger, *args, **kwargs)
        
        
        size = [350]
        color = "#" + "1c" *3
        
        coursesframe = ct.CTkFrame(self,fg_color="transparent")
        coursesframe.grid(row=0,column=0)
        
        self.all = ct.CTkScrollableFrame(coursesframe,width=size[0],height=size[-1],fg_color=color)
        self.all.grid(row=1,column=0,padx = 20)
        # self.all.grid_propagate(False)
        ct.CTkLabel(coursesframe,text="Unregistered Courses",font=("",16)).grid(row=0,column=0)
        
        self.registered = ct.CTkScrollableFrame(coursesframe,width=size[0],height=size[-1],fg_color=color)
        self.registered.grid(row=1,column=1)
        ct.CTkLabel(coursesframe,text="Registered Courses",font=("",16)).grid(row=0,column=1)

        btns = ct.CTkFrame(self,fg_color="transparent")
        btns.grid(row=2,column=0)
        
        self.confirm = button(btns,2,0,"Confirm",width=150,height=50,command=self.comfirm_popup)
        self.cancel = button(btns,2,1,"Cancel",width=150,height=50,command=lambda: self.comfirm_popup(False))
        
        self.confirm.configure(fg_color="green",hover_color="darkgreen")
        self.cancel.configure(fg_color="red",hover_color="darkred")

        self.buttons = {}
    
    
    def add_course_button(self,list,id):
        course = ct.CTkButton(list,text = f"{Student.all_courses[id]} ({id})",font = ("",16),width = 400,height = 42,fg_color="transparent",hover_color = "#333333",anchor="w",command=lambda x=id: self.buttonpress(x))
        course.pack(padx = 4,pady = 0,anchor="w")
        self.buttons[id] = course
        return course
    
    def comfirm_popup(self,conf = True):
        self.confirmpop = ct.CTkFrame(self.master,fg_color="transparent")
        self.confirmpop.grid(row=0,column=0,sticky="nsew")
        self.confirmpop.grid_columnconfigure(0,weight=1)
        self.confirmpop.grid_rowconfigure(0,weight=1)
        
        f = ct.CTkFrame(self.confirmpop,fg_color="#202020",width = 450,height = 250)
        f.grid_propagate(False)
        f.grid(row=0,column=0)
        f.grid_columnconfigure(0,weight=1)
        f.grid_rowconfigure(0,weight=1)
        f.grid_rowconfigure(1,weight=1)
        
        header(f,"Confirm changes?" if conf else "Ignore changes?",0,0,font_size=32,pady=10).configure(height=50)
        
        btns = ct.CTkFrame(f,fg_color="transparent")
        btns.grid(row=1,column=0)
        
        def back(conf):
            self.confirmpop.destroy()
            self.goto("Student_menu")
        
        if(conf):
            yes = button(btns,0,0,"Confirm",width = 100,command = lambda:back(True))
            yes.configure(fg_color="green",hover_color="darkgreen")
            no = button(btns,0,1,"Cancel",width=100,command = lambda:self.confirmpop.destroy())
            no.configure(fg_color="red",hover_color="darkred")
        else:
            yes = button(btns,0,0,"Ignore",width = 100,command = lambda:back(False))
            yes.configure(fg_color="red",hover_color="darkred")
            no = button(btns,0,1,"Cancel",width=100,command = lambda:self.confirmpop.destroy())
            no.configure(fg_color="green",hover_color="darkgreen")
        
        # ct.CTkLabel(self.confirmpop,text="Are you sure?",font = ("",16)).grid(row=0,column=0)
        
    
    def buttonpress(self,id):
        self.buttons[id].destroy()
        if id in self.manger.user.courses:
            self.manger.user.remove_course(id)
            self.add_course_button(self.all,id)
        else:
            self.manger.user.add_course(id)
            self.add_course_button(self.registered,id)
            # self.buttons.pop(id)
            # self.all.remove(self.buttons[id])
            # self.registered.add(self.buttons[id])
        
    
    def init_buttons(self):
        for i in self.buttons:
            self.buttons[i].destroy()
        self.buttons = {}
        
        for id in Student.all_courses:
            parent = self.registered if id in self.manger.user.courses else self.all
            self.add_course_button(parent,id)
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
        self.user = Student(0)
        
        for i in [Login, Student_menu, Control_menu, Courses_menu]:
            self.pages[i.__name__] = i(master,self)
        
        self.pages["Login"].enter()