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
        
    
    def enter(self,**args):
        self.grid(row=0,column=0)
        
        self.tkraise()
        
        self.manger.current = self
        
    def goto(self,nextpage,**args):
        
        self.manger.pages[nextpage].enter(**args)
        
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
    
    def enter(self,**args):
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
        btns.grid(row=2,column=0,sticky="we")
        
        
        ct.CTkLabel(btns,text="Group",font=("",16)).grid(row=0,column=0,padx=10,sticky="w")
        
        self.selectedgroup = ct.StringVar(self,value="A")
        self.group = ct.CTkOptionMenu(btns,variable=self.selectedgroup,values = Student.all_groups,font = ("",16),width = 117,height = 50, fg_color=color,button_color=color)
        self.group.grid(row=0,column=1,padx=(0,30),sticky="w")
        
        self.confirm = button(btns,0,2,"Confirm",width=150,height=50,command=self.confirm_popup)
        self.cancel = button(btns,0,3,"Cancel",width=150,height=50,command=lambda: self.confirm_popup(False))
        
        
        self.confirm.configure(fg_color="green",hover_color="darkgreen")
        self.cancel.configure(fg_color="red",hover_color="darkred")

        self.buttons = {}
    
    
    def add_course_button(self,list,id):
        course = ct.CTkButton(list,text = f"{Student.all_courses[id]} ({id})",font = ("",16),width = 400,height = 42,fg_color="transparent",hover_color = "#333333",anchor="w",command=lambda x=id: self.buttonpress(x))
        course.pack(padx = 4,pady = 0,anchor="w")
        self.buttons[id] = course
        return course
    
    def get_button_position(self,id):
        return (id in self.manger.user.courses) ^ (id in self.changed) #True = registered, False = unregistered
    
    def confirm_popup(self,conf = True):
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
        
    
    def buttonpress(self,id):
        self.buttons[id].destroy()
        if self.get_button_position(id):
            self.add_course_button(self.all,id)
        else:
            self.add_course_button(self.registered,id)
        if(id in self.changed):
            self.changed.remove(id)
            self.buttons[id].configure(fg_color="transparent",hover_color="#333333")
        else:
            self.buttons[id].configure(fg_color="#333333",hover_color="#3f3f3f")
            self.changed.append(id)
        
    
    def init_buttons(self):
        self.changed = []
        for i in self.buttons:
            self.buttons[i].destroy()
        self.buttons = {}
        
        self.selectedgroup = ct.StringVar(self,value=self.manger.user.group)
        
        for id in Student.all_courses:
            parent = self.registered if self.get_button_position(id) else self.all
            self.add_course_button(parent,id)
#------------------------------------------------------------------------------------

#Control Pages------------------------------------------------------------------------
class Control_menu(Page):
    def __init__(self, master, manger, *args, **kwargs):
        super().__init__(master, manger, *args, **kwargs)
        
        self.header = header(self,"Welcome, ")
        
        f = ct.CTkFrame(self)
        f.grid(row=1,column=0)
        
        managestudents = button(f,0,0,"Manage Students",command=lambda:self.goto("Student_search"))
        managecourses = button(f,1,0,"Courses and Groups")
        
        news = button(f,2,0,"News")
        back = button(f,3,0,"login screen",command = lambda:self.goto("Login"))
        back.configure(fg_color = "red",hover_color = "darkred")
    
    def enter(self,**args):
        self.header.configure(text = "Welcome, " + self.manger.user.name)
        
        super().enter()

class Student_search(Page):
    def __init__(self, master, manger, *args, **kwargs):
        super().__init__(master, manger, *args, **kwargs)
        
        header(self,"Enter Student ID")
        
        self.idserch = ct.CTkTextbox(self,width=250,height=40,font=("",25))
        self.idserch.grid(row=2,column=0,pady = (50,20))
        self.idserch.bind("<Return>", self.search)
        
        submit = button(self,3,0,"Search",command = self.search,pady=10)
        back = button(self,4,0,"Back",command = lambda:self.goto("Control_menu"),pady=10)
        back.configure(fg_color = "red",hover_color = "darkred")
    
    def search(self):
        self.goto("Student_info",id = self.idserch.get("1.0","end"))
    
    

class Student_info(Page):
    def __init__(self,master,manger,*args,**kwargs):
        super().__init__(master,manger,*args,**kwargs)
        
        self.id = "0"
        
        header(self,"Student Info",pady=(100,10))
        
        self.card = ct.CTkFrame(self,fg_color="transparent")
        self.card.grid(row=1,column=0,sticky="news")
        # self.card.grid_propagate(False)
        
        self.showinfo = ct.CTkFrame(self,fg_color="#202020")
        self.showinfo.grid(row=1,column=0)
        
        self.showinfo.grid_columnconfigure(0,weight=1)
        
        self.textframe = ct.CTkFrame(self.showinfo,fg_color="transparent")
        self.textframe.grid(row=0,column=0,sticky="ew")
        
        self.textframe.grid_columnconfigure((0,1),weight=1,uniform="column")
        
        pad = (20,35)
        self.name = ct.CTkLabel(self.textframe,text="Name: Student Student Student",font=("",14))
        self.name.grid(row=0,column=0,padx=pad[0],pady=pad[1])
        
        self.password = ct.CTkLabel(self.textframe,text="Password: 917adsf2",font=("",14))
        self.password.grid(row=0,column=1,padx=pad[0],pady=pad[1])
        
        self.idtext = ct.CTkLabel(self.textframe,text="ID: 20132021",font=("",14))
        self.idtext.grid(row=1,column=0,padx=pad[0],pady=pad[1])
    
        self.gpa = ct.CTkLabel(self.textframe,text="GPA: 4.0",font=("",14))
        self.gpa.grid(row=1,column=1,padx=pad[0],pady = pad[1])
        
        self.btns = ct.CTkLabel(self.showinfo)
        self.btns.grid(row=3,column=0)
        
        self.editinfo = button(self.btns,3,0,"Edit Info", command=lambda:self.goto("Student_info_edit",id="123123"))
        self.editinfo.grid(row=0,column=0,padx=10)
    
        self.back = button(self.btns,4,0,"back",command=lambda:self.goto("Student_search"))
        self.back.grid(row=0,column=1)
        self.back.configure(fg_color = "red",hover_color = "darkred")
    
        
        
    def enter(self, **args):
        
        self.grid_propagate(False)
        self.grid(row=0, column=0, stick="nswe",padx=10,pady=10)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        
        self.id = args["id"]
        
        self.idtext.configure(text="ID: " + self.id)
        
        
        return super().enter(**args)
    

class Student_info_edit(Page):
    def __init__(self,master,manger,*args,**kwargs):
        super().__init__(master,manger,*args,**kwargs)
        
        
        header(self,"Edit Student Info",pady=(100,10))
        
        self.card = ct.CTkFrame(self,fg_color="transparent")
        self.card.grid(row=1,column=0,sticky="news")
        # self.card.grid_propagate(False)
        
        self.showinfo = ct.CTkFrame(self,fg_color="#202020")
        self.showinfo.grid(row=1,column=0)
        
        self.showinfo.grid_columnconfigure(0,weight=1)
        
        self.textframe = ct.CTkFrame(self.showinfo,fg_color="transparent")
        self.textframe.grid(row=0,column=0,sticky="ew")
        
        self.textframe.grid_columnconfigure((0,1),weight=1,uniform="column")
        
        pad = (20,35)
        
        self.namecont = ct.CTkFrame(self.textframe,fg_color="transparent")
        self.namecont.grid(row=0,column=0)
        
        self.name = ct.CTkLabel(self.namecont,text="Name:",font=("",14))
        self.name.grid(row=0,column=0,pady=pad[1],padx = (pad[0],0))
        self.editname = ct.CTkTextbox(self.namecont,width=240,height=30,font=("",14))
        self.editname.grid(row=0,column=1,pady=pad[1],padx = (0,pad[0]))
        
        self.passwordcont = ct.CTkFrame(self.textframe,fg_color="transparent")
        self.passwordcont.grid(row=0,column=1)
        
        self.password = ct.CTkLabel(self.passwordcont,text="Password:",font=("",14))
        self.password.grid(row=0,column=0,padx=pad[0],pady=pad[1])
        self.editpassword = ct.CTkTextbox(self.passwordcont,width=170,height=30,font=("",14))
        self.editpassword.grid(row=0,column=1,pady=pad[1],padx = (0,pad[0]))
        
        self.id = ct.CTkLabel(self.textframe,text="ID: 20132021",font=("",21))
        self.id.grid(row=1,column=0,padx=pad[0],pady=pad[1])
    
        self.gpacont = ct.CTkFrame(self.textframe,fg_color="transparent")
        self.gpacont.grid(row=1,column=1)
        
        self.gpa = ct.CTkLabel(self.gpacont,text="GPA:",font=("",14))
        self.gpa.grid(row=0,column=0,padx=pad[0],pady=pad[1])
        self.editgpa = ct.CTkTextbox(self.gpacont,width=70,height=30,font=("",14))
        self.editgpa.grid(row=0,column=1,pady=pad[1],padx = (0,pad[0]))
        
        
        self.btns = ct.CTkLabel(self.showinfo)
        self.btns.grid(row=3,column=0)
        
        self.editinfo = button(self.btns,3,0,"confirm")
        self.editinfo.grid(row=0,column=0,padx=10)
        self.editinfo.configure(fg_color = "green",hover_color = "darkgreen",command=lambda:self.confirm_popup(True))
    
        self.back = button(self.btns,4,0,"cancel",command=lambda:self.confirm_popup(False))
        self.back.grid(row=0,column=1)
        self.back.configure(fg_color = "red",hover_color = "darkred")
    
    def confirm_popup(self,conf = True):
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
            self.goto("Student_info",id="123123")
        
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
#--------------------------------------------------------------------------------


class PagesManger:
    def __init__(self,master) -> None:
        self.pages = {}
        self.current = None
        self.user = Control(0)
        
        for i in [Login, Student_menu, Control_menu, Courses_menu,Student_search,Student_info,Student_info_edit]:
            self.pages[i.__name__] = i(master,self)
        
        self.pages["Student_info_edit"].enter()