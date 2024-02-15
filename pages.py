import customtkinter as ct
from classes import *

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

def textbox_enter(event,button):
        button.invoke()
        return ("break")
    
def textbox_tab(event):
    event.widget.tk_focusNext ().focus ()
    return ("break")

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
    def __init__(self,master,manger,*args,**kwargs):
        super().__init__(master,manger,*args,**kwargs)
            
        self.manger = manger
        header(self,"Sign in...")
        
        input = ct.CTkFrame(self)
        input.grid(row=1,column=0)
        
        self.wrongpassword = None
        def checkpasswrod(id, password,student):

            if(student and Student.checkpassword(id,password)):
                self.manger.user = Student(id)
                self.goto("Student_menu")
            elif(not student and Control.checkpassword(id,password)):
                self.manger.user = Control(id)
                self.goto("Control_menu")
            else:
                self.wrongpassword = ct.CTkLabel(self,text = "Wrong id or password",text_color="red")
                self.wrongpassword.grid(row = 2,column = 0)
        
        
        ct.CTkLabel(input,text = "ID",anchor="w").grid(row = 0,column = 0)
        id = ct.CTkEntry(input,height = 30,width = 200)
        id.bind("<Return>", textbox_tab)
        id.bind("<Tab>", textbox_tab)
        id.grid(row = 1,column = 0)
        
        self.id = id
        ct.CTkLabel(input,text = "Password").grid(row = 2,column = 0)
        
        # password = ct.CTkTextbox(input,height = 30,width = 200)
        password = ct.CTkEntry(input,show="*",width = 200,height=30)
        password.bind("<Return>", lambda x : textbox_enter(x,studentlogin))
        password.bind("<Tab>", textbox_tab)
        password.grid(row = 3,column = 0,padx = 20)
        
        self.password = password
        
        soc = ct.CTkFrame(input,fg_color="transparent") #soc = Student or Control
        soc.grid(row = 4,column = 0)
        
        studentlogin = button(soc,0,0,"Student login",width = 90,height=30,padx=5,command=lambda: checkpasswrod(id.get().strip(),password.get().strip(),True))    
        controllogin = button(soc,0,1,"Control login",width = 90,height=30,padx=5,command=lambda: checkpasswrod(id.get().strip(),password.get().strip(),False))    
        
        back = button(input,5,0,"exit",width = 215,height=30,pady=(3,20),command = lambda: exit()) 
        back.configure(fg_color="red")
        back.configure(hover_color="darkred")
        

    def goto(self,nextpage):
        if(self.wrongpassword):
            self.wrongpassword.grid_forget()
        # self.id.delete("1.0","end")
        self.password.delete(0,len(self.password.get()) + 1)
        
        super().goto(nextpage)
        

#Student Pages--------------------------------------------------------------------
class Student_menu(Page):
    def __init__(self, master, manger, *args, **kwargs):
        super().__init__(master, manger, *args, **kwargs)
        
        self.header = header(self,"Welcome, ")
        
        f = ct.CTkFrame(self)
        f.grid(row=1,column=0)
        
        info = button(f,0,0,"Info",command=lambda:self.goto("Student_info",user=self.manger.user,mode=False))
        editcourse = button(f,1,0,"Courses and Group",command=lambda:self.goto("Courses_menu"))
        back = button(f,2,0,"login screen",command = lambda:self.goto("Login"))
        back.configure(fg_color = "red",hover_color = "darkred")
    
    def enter(self,**args):
        self.header.configure(text="Welcome, " + Student.all_students[self.manger.user.id]["name"].split(" ")[0])
        
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
        return (id in Student.all_students[self.manger.user.id]["courses"]) ^ (id in self.changed) #True = registered, False = unregistered
    
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
        
        def save():
            
            courses = []
            for i in Student.all_courses:
                if(self.get_button_position(i)):
                    courses.append(i)
            Student.all_students[self.manger.user.id]["courses"] = courses
            Student.all_students[self.manger.user.id]["group"] = self.group.get()
            
            with open("students.json","w") as f:
                json.dump(Student.all_students,f)
                
            back(True)
        
        if(conf):
            yes = button(btns,0,0,"Confirm",width = 100,command = save)
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
        
        self.selectedgroup = ct.StringVar(self,value=Student.all_students[self.manger.user.id]["group"])
        
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
        managecourses = button(f,1,0,"Manage Courses",command=lambda:self.goto("Edit_Courses"))
        
        # news = button(f,2,0,"News")
        back = button(f,3,0,"login screen",command = lambda:self.goto("Login"))
        back.configure(fg_color = "red",hover_color = "darkred")
    
    def enter(self,**args):
        self.header.configure(text = "Control Menu")
        
        super().enter()

class Student_search(Page):
    def __init__(self, master, manger, *args, **kwargs):
        super().__init__(master, manger, *args, **kwargs)
        
        header(self,"Enter Student ID")
        
        self.idsearch = ct.CTkEntry(self,width=250,height=40,font=("",25))
        self.idsearch.grid(row=2,column=0,pady = (50,20))
        self.idsearch.bind("<Return>", lambda x : self.search())
        
        submit = button(self,3,0,"Search",command = self.search,pady=10)
        Add = button(self,4,0,"Add Student",command = self.add,pady=10)
        back = button(self,5,0,"Back",command = lambda:self.goto("Control_menu"),pady=10)
        back.configure(fg_color = "red",hover_color = "darkred")
    
    def search(self):
        if(self.idsearch.get().strip() not in Student.all_students):
            self.warning = ct.CTkLabel(self,text="Student doesn't exists",text_color="red")
            self.warning.grid(row=6,column=0)
            return
        self.goto("Student_info",user = Student(self.idsearch.get().strip()),add=False,mode = True)
        
    def add(self):
        if(self.idsearch.get().strip() == ""):
            self.warning = ct.CTkLabel(self,text="Please enter a valid ID",text_color="red")
            self.warning.grid(row=6,column=0)
            return
        elif(self.idsearch.get().strip() in Student.all_students):
            self.warning = ct.CTkLabel(self,text="Student already exists",text_color="red")
            self.warning.grid(row=6,column=0)
            return
        self.goto("Student_info_edit",user = Student(self.idsearch.get("1.0","end").strip()),add=True)
    
    

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
        
        # self.textframe.grid_rowconfigure((0,1),weight=1,uniform="row")
        # self.textframe.grid_propagate(False)
        
        pad = (20,35)
        
        
        
        self.name = ct.CTkLabel(self.textframe,text="Name: Student Student Student",font=("",15))
        self.name.grid(row=0,column=0,padx=pad[0],pady=pad[1])
        
        self.password = ct.CTkLabel(self.textframe,text="Password: 917adsf2",font=("",15))
        self.password.grid(row=0,column=1,padx=pad[0],pady=pad[1])
        
        self.idtext = ct.CTkLabel(self.textframe,text="ID: ",font=("",15))
        self.idtext.grid(row=1,column=0,padx=pad[0],pady=pad[1])
    
        self.level = ct.CTkLabel(self.textframe,text="Level: 1",font=("",15))
        self.level.grid(row=1,column=1,pady=pad[1])
        
        self.gpa = ct.CTkLabel(self.textframe,text="GPA: 4.0",font=("",15))
        self.gpa.grid(row=1,column=2,padx=pad[0],pady = pad[1])
        
        
        self.btns = ct.CTkFrame(self.showinfo,fg_color="transparent")
        self.btns.grid(row=3,column=0)
        
        self.editinfo = button(self.btns,3,0,"Edit Info", command=self.checkStudent)
        self.editinfo.grid(row=0,column=0,padx=10)
    
        self.back = button(self.btns,4,0,"back",command=lambda:self.goto("Student_search" if self.mode else "Student_menu"))
        self.back.grid(row=0,column=1)
        self.back.configure(fg_color = "red",hover_color = "darkred")
    
    
    def checkStudent(self):
        if(self.id not in Student.all_students):
            self.warning = ct.CTkLabel(self,text="Student does not exist",text_color="red")
            self.warning.grid(row=3,column=0)
            return False
        else:
            self.user = Student(self.id)
            self.goto("Student_info_edit",user=self.user,add=False)
        
    def enter(self, **args):
        
        self.grid_propagate(False)
        self.grid(row=0, column=0, stick="nswe",padx=10,pady=10)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        
        self.mode = args["mode"]
        
        self.user = args["user"]
        
        self.id = self.user.id
        
        self.idtext.configure(text="ID: " + self.id)
        
        if(self.mode):
            self.editinfo.grid(row=0,column=0,padx=10)
        else:
            self.editinfo.destroy()
            self.password.grid_forget()
            self.showpass = button(self.textframe,0,1,"Show Password",command=lambda:show())
            self.showpass.configure(fg_color="#313131",hover_color="#2f2f2f")
            def show():
                self.showpass.grid_forget()
                self.password.grid(row=0,column=1,padx=20,pady=35)
                
        
        self.name.configure(text="Name: " + Student.all_students[self.id]["name"])
        self.password.configure(text="Password: " + Student.all_students[self.id]["password"])
        self.level.configure(text="Level: " + str(Student.all_students[self.id]["level"]))
        self.gpa.configure(text="GPA: " + str(Student.all_students[self.id]["gpa"]))
        
        return super().enter(**args)
    

class Student_info_edit(Page):
    def __init__(self,master,manger,*args,**kwargs):
        super().__init__(master,manger,*args,**kwargs)
        
        
        self.header = header(self,"Edit Student Info",pady=(100,10))
        
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
        
        self.idlabel = ct.CTkLabel(self.textframe,text="ID: ",font=("",21))
        self.idlabel.grid(row=1,column=0,padx=pad[0],pady=pad[1])
    
        self.levelcont = ct.CTkFrame(self.textframe,fg_color="transparent")
        self.levelcont.grid(row=1,column=1)
        
        self.level = ct.CTkLabel(self.levelcont,text="Level:",font=("",14))
        self.level.grid(row=0,column=0,padx=pad[0],pady=pad[1])
        self.editlevel = ct.CTkOptionMenu(self.levelcont,values=["1","2","3","4"],font=("",14))
        self.editlevel.grid(row=0,column=1,pady=pad[1],padx = (0,pad[0]))
        
        self.gpacont = ct.CTkFrame(self.textframe,fg_color="transparent")
        self.gpacont.grid(row=1,column=2)
        
        self.gpa = ct.CTkLabel(self.gpacont,text="GPA:",font=("",14))
        self.gpa.grid(row=0,column=0,padx=pad[0],pady=pad[1])
        self.editgpa = ct.CTkTextbox(self.gpacont,width=70,height=30,font=("",14))
        self.editgpa.grid(row=0,column=1,pady=pad[1],padx = (0,pad[0]))
        
        
    
        
        self.btns = ct.CTkLabel(self.showinfo)
        self.btns.grid(row=3,column=0)
        
        self.editinfo = button(self.btns,3,0,"confirm")
        self.editinfo.grid(row=0,column=0,padx=10)
        self.editinfo.configure(fg_color = "green",hover_color = "darkgreen",command=lambda:self.confirm_popup(True))

        self.editname.bind("<Tab>", textbox_tab)
        self.editname.bind("<Return>", textbox_tab)
        self.editpassword.bind("<Tab>", textbox_tab)
        self.editpassword.bind("<Return>", textbox_tab)
        self.editgpa.bind("<Tab>", textbox_tab)
        self.editgpa.bind("<Return>", lambda x: textbox_enter(x,self.editinfo))
        
        self.back = button(self.btns,4,0,"cancel",command=lambda:self.confirm_popup(False))
        self.back.grid(row=0,column=1)
        self.back.configure(fg_color = "red",hover_color = "darkred")
    
    def enter(self,**args):
        self.isadding = args["add"]
        self.user = args["user"]
        self.id = self.user.id
        
        if(self.isadding):
            self.header.configure(text="Add New Student")
        else:
            self.header.configure(text="Edit Student Info")
            
            self.editname.delete("1.0","end")
            self.editpassword.delete("1.0","end")
            self.editgpa.delete("1.0","end")
            
            self.editname.insert("1.0",Student.all_students[self.id]["name"])
            self.editpassword.insert("1.0",Student.all_students[self.id]["password"])
            self.editgpa.insert("1.0",Student.all_students[self.id]["gpa"])
        self.idlabel.configure(text="ID: " + self.user.id)
        self.warning = ct.CTkLabel(self.showinfo,text="GPA must be a number between 0 and 4",font=("",10),text_color="red")
        
            
            
        return super().enter(**args)
    
    def confirm_popup(self,conf = True):
        try:
            if(conf):
                if(len(self.editname.get("1.0","end").strip()) < 3):
                    self.warning.configure(text="Name must be at least 3 characters long")
                    self.warning.grid_forget()
                    self.warning.grid(row=1,column=0,pady=0)
                    return
                if(len(self.editpassword.get("1.0","end").strip()) < 7):
                    self.warning.configure(text="Password must be at least 7 characters long")
                    self.warning.grid_forget()
                    self.warning.grid(row=1,column=0,pady=0)
                    return
                g = float(self.editgpa.get("1.0","end").strip())
                if(g < 0 or g > 4):
                    self.warning.configure(text="GPA must be a number between 0 and 4")
                    self.warning.grid_forget()
                    self.warning.grid(row=1,column=0,pady=0)
                    return
                    
            
            
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
                if(not self.isadding):
                    self.goto("Student_info",user=self.user,mode=True)
                else:
                    self.goto("Student_search")
            
            def savestudent():
                Student.Add_Student(
                    id = self.id,
                    name = self.editname.get("1.0","end").strip(),
                    password = self.editpassword.get("1.0","end").strip(),
                    group = "A",
                    courses = [],
                    gpa = self.editgpa.get("1.0","end").strip(),
                    level = self.editlevel.get().strip()
                )
                self.confirmpop.destroy()
                self.user = Student(self.id)
                self.goto("Student_info",user=self.user,mode=True)
            
            if(conf):
                yes = button(btns,0,0,"Confirm",width = 100,command=savestudent)
                yes.configure(fg_color="green",hover_color="darkgreen")
                no = button(btns,0,1,"Cancel",width=100,command = lambda:self.confirmpop.destroy())
                no.configure(fg_color="red",hover_color="darkred")
            else:
                yes = button(btns,0,0,"Ignore",width = 100,command = lambda:back(False))
                yes.configure(fg_color="red",hover_color="darkred")
                no = button(btns,0,1,"Cancel",width=100,command = lambda:self.confirmpop.destroy())
                no.configure(fg_color="green",hover_color="darkgreen")
        except:
            self.warning.configure(text="GPA must be a number between 0 and 4")
            self.warning.grid_forget()
            self.warning.grid(row=1,column=0,pady=0)

class Edit_Courses(Page):
    def __init__(self, master, manger, *args, **kwargs):
        super().__init__(master, manger, *args, **kwargs)
        
        
        self.header = header(self,"Edit courses",pady=20)
        self.header.configure(font=("",25))
        self.header.grid(row=0,column=0,sticky = "new")
        
        self.cont = ct.CTkFrame(self,fg_color="transparent")
        self.cont.grid(row=1,column=0)
        
        
        self.coursesframe = ct.CTkScrollableFrame(self.cont,fg_color="#202020",width = 350,height = 320)
        self.coursesframe.grid(row=1,column=0,padx=(30,10))
        
        self.inputcont = ct.CTkFrame(self.cont,fg_color="transparent")
        self.inputcont.grid(row=2,column=0,sticky="new",padx=(10,40))
        
        
        
        ct.CTkLabel(self.inputcont,text="Course name:",font=("",12)).grid(row=0,column=0,padx = (20,0),sticky="w")
        self.coursename = ct.CTkTextbox(self.inputcont,height=40,width=200,font=("",16))
        self.coursename.grid(row=0,column=1,padx = (0,10),sticky="w")
        
        ct.CTkLabel(self.inputcont,text="id:",font=("",12)).grid(row=0,column=2,sticky="w")
        self.courseid = ct.CTkTextbox(self.inputcont,height=40,width=80,font=("",16))
        self.courseid.grid(row=0,column=3,padx = (0,10),sticky="w")
        
        
        self.buttonscont = ct.CTkFrame(self.cont,fg_color="transparent")
        self.buttonscont.grid(row=4,column=0,padx=(20,0))
        
        self.addcourse = button(self.buttonscont,0,0,"Add Course",width=100,command=lambda: self.AddCourse(self.coursename.get("1.0","end-1c"),self.courseid.get("1.0","end-1c").upper()))
        
        self.removecourse = button(self.buttonscont,0,1,"Delete Course",width=100,command=lambda: self.delete(self.selected))
        self.removecourse.configure(fg_color="#5a2020",hover_color="red")
        self.removecourse.configure(state="disabled")
        
        self.confcont = ct.CTkFrame(self,fg_color="transparent")
        self.confcont.grid(row=5,column=0,pady=20)
        
        self.confirmpop = button(self.confcont,0,0,"Confirm")
        self.confirmpop.configure(fg_color="green",hover_color="darkgreen",command = lambda:self.confirm_popup(True))
        
        self.cancelpop = button(self.confcont,0,1,"Cancel")
        self.cancelpop.configure(fg_color="red",hover_color="darkred",command = lambda:self.confirm_popup(False))
        
        self.warning = ct.CTkLabel(self.cont,text = "Name cant be empty and id must be excatlly 5 characters",text_color="red",anchor="w",font=("",16),height=35)    

        self.coursename.bind("<Return>",textbox_tab)
        self.coursename.bind("<Tab>",textbox_tab)
        self.courseid.bind("<Return>",textbox_tab)
        self.courseid.bind("<Tab>",textbox_tab)
        
        self.courses = {}
        self.groups = {}
        
        self.todelete = []
        self.toadd = {}
        self.toedit = {}
        
        self.selected = None
        
  
    
    def getnormalcolor(self,id):
        if(id in self.todelete):
            return ("red","darkred")
        elif(id in self.toadd):
            return ("green","darkgreen")
        else:
            return ("transparent","#333333")
    
    def delete(self,id):
        if(id in self.todelete):
            self.todelete.remove(id)
            clr = self.getnormalcolor(self.selected)
            self.courses[self.selected].configure(fg_color=clr[0],hover_color=clr[1])
        elif(id in self.toedit):
            self.toedit.pop(id)
            self.courses[id].configure(fg_color="transparent",hover_color="#333333",text=f"({id}) {Student.all_courses[id]}")
        else:
            if(id in self.toadd):
                self.toadd.pop(id)
                self.courses[id].destroy()
                self.courses.pop(id)
            else:
                self.todelete.append(id)
                clr = self.getnormalcolor(self.selected)
                self.courses[self.selected].configure(fg_color=clr[0],hover_color=clr[1])
                
        self.selected = None
        self.removecourse.configure(fg_color="#5a2020",hover_color="red",text="DeleteCourse")
        self.removecourse.configure(state="disabled")
                
    
    def enter(self,**args):
        self.grid(row=0,column=0,sticky="nsew")
        self.grid_propagate(False)
        self.grid_columnconfigure(0,weight=1)
        
        self.todelete = []
        self.toadd = {}
        self.toedit = {}
        self.selected = None
        
        for i in self.coursesframe.winfo_children():
            i.destroy()
        
        for i in Student.all_courses:
            self.Add_Course_button(i)
        super().enter(**args)

    def select(self,id):
        if(self.selected):
            clr = self.getnormalcolor(self.selected)
            self.courses[self.selected].configure(fg_color=clr[0],hover_color=clr[1])
        
        tex = ""
        if(id in self.todelete):
            tex = "Undo Delete"
        elif(id in self.toedit):
            tex = "Undo Edit"
        else:
            tex = "Delete Course"
        self.removecourse.configure(state="normal",fg_color="red",text=tex)
        
        if(not (id in self.todelete or id in self.toadd or id in self.toedit)):
            self.courses[id].configure(fg_color="#3f3f3f",hover_color="#4e4e4e")
        self.selected = id
    
    def AddCourse(self,name,id):
        if(len(id) != 5):
            self.warning.configure(text = "Name cant be empty and id must be excatlly 5 characters")
            self.warning.grid(row=3,column=0,pady=0)
            return
        
        already = id in self.courses
        
        if(already):
            self.courses[id].configure(fg_color="blue",hover_color="darkblue",text=f"({id}) {name}")
            self.toedit[id] = name
            if(id in self.todelete):
                self.todelete.remove(id)
        else:
            self.toadd[id] = name
            btn = self.Add_Course_button(id)
            self.courses[id].configure(fg_color="green",hover_color="darkgreen")
        self.warning.grid_forget()
        
    
    def Add_Course_button(self,id):
        name = Student.all_courses[id] if id in Student.all_courses else self.toadd[id]
        button = ct.CTkButton(self.coursesframe,text = f"({id}) {name}",fg_color="transparent",hover_color="#333333",anchor="w",font=("",16),height=35)
        button.configure(command = lambda:self.select(id))
        button.pack(expand=True,fill="both")
        
        self.courses[id] = button
        
        return button

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
            self.goto("Control_menu")
        
        def saveCourses():
            
            for i in self.todelete:
                Student.all_courses.pop(i)
                for s in Student.all_students:
                    if i in Student.all_students[s]["courses"]:
                        Student.all_students[s]["courses"].remove(i)
            for i in self.toadd:
                Student.all_courses[i] = self.toadd[i]
            for i in self.toedit:
                Student.all_courses[i] = self.toedit[i]
            
            
            
            with open("courses.json","w") as f:
                json.dump(Student.all_courses,f)
            
            back(True)
        
        if(conf):
            yes = button(btns,0,0,"Confirm",width = 100,command = saveCourses)
            yes.configure(fg_color="green",hover_color="darkgreen")
            no = button(btns,0,1,"Cancel",width=100,command = lambda:self.confirmpop.destroy())
            no.configure(fg_color="red",hover_color="darkred")
        else:
            yes = button(btns,0,0,"Ignore",width = 100,command = lambda:back(False))
            yes.configure(fg_color="red",hover_color="darkred")
            no = button(btns,0,1,"Cancel",width=100,command = lambda:self.confirmpop.destroy())
            no.configure(fg_color="green",hover_color="darkgreen")
        
        

class News(Page):
    def __init__(self,master,manger,*args,**kwargs):
        super().__init__(master,manger,*args,**kwargs)
        
                        
        

#--------------------------------------------------------------------------------


class PagesManger:
    def __init__(self,master) -> None:
        self.pages = {}
        self.current = None
        self.user = Control(0)
        
        for i in [Login, Student_menu, Control_menu, Courses_menu,Student_search,Student_info,Student_info_edit,Edit_Courses]:
            self.pages[i.__name__] = i(master,self)
        
        self.pages["Login"].enter()