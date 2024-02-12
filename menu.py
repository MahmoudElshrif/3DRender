#---------temporary test functions and classes, replace with the working ones---------
class Student:
    all_courses = ["Course A","Course B","Course C","Course D","Course E"]
    all_groups = ["A","B","C","D"]
    def __init__(self,id):
        self.id = id
        self.name = "Student"
        self.courses = ["Course B","Course C","Course D"]
        self.group = "A"
        self.GPA = 4.0
        pass

    def checkpassword(self,password):
        return (self.id == password) and (self.id == "admin")
    
    def add_course(self,course):
        self.courses.append(course)
    
    def remove_course(self,course):
        self.courses.remove(course)
    def set_group(self,group):
        self.group = group
#------------------------------------------------------------------------------------------

import customtkinter as ct
import time

class App:
    
    def __init__(self,master):
        self.master = master
        self.master.geometry("900x600")
        self.user = Student(0)
        self.pages = {}
        self.current = None
        self.master.grid_rowconfigure(0,weight = 1)
        self.master.grid_columnconfigure(0,weight = 1)
        
        for i in [self.Control_or_Student,self.Student_login,self.Student_menu]:
            self.pages[i] = i()
        
        self.switch_to(self.Control_or_Student)
    
    def main_frame(self):
        frame = ct.CTkFrame(self.master,fg_color="transparent")
        self.master.grid_propagate(False)
        return frame
    
    def switch_to(self,page):
        if(self.current):
            self.current.grid_forget()
        
        frame = self.pages[page]
        frame.grid(row=0,column=0)
        self.current = frame
        pass
    
    def button(self,root,gridx,gridy,text,font_size = 16,width = 200,height = 50,padx = 20,pady = 10,command = lambda : print("test")):
        btn = ct.CTkButton(root,text = text,font = ("",font_size),width = width,height = height,command = command)
        btn.grid(row = gridx,column = gridy,padx = padx,pady = pady)
        return btn   
    def header(self,root,text,gridx = 0,gridy = 0,font_size = 52,pady = (0,100),padx = 20):
        text = ct.CTkLabel(root,text = text,font = ("",font_size))
        text.grid(row = gridx,column = gridy,padx = padx,pady = pady)
        return text
    
    def Control_or_Student(self):
        frame = self.main_frame()
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        self.header(frame,"Sign in as....")
        
        buttons = ct.CTkFrame(frame,bg_color="transparent")
        buttons.grid(row=1,column=0)
        self.button(buttons,0,0,"Student",padx=50,pady=(40,20),command=lambda: self.switch_to(self.Student_login))
        self.button(buttons,1,0,"Control",padx=50,pady=(20,40))
        
        return frame
    
    def textbox_enter(self,event,button):
        button.invoke()
        return ("break")
    
    def textbox_tab(self,event):
        event.widget.tk_focusNext ().focus ()
        return ("break")
    
    #Student menus-------------
    def Student_login(self):
        
        frame = self.main_frame()
        
        self.header(frame,"Student login")
        
        input = ct.CTkFrame(frame)
        input.grid(row=1,column=0)
        
        def checkpasswrod(id, password):
            student = Student(id)
            if(student.checkpassword(password)):
                self.user = student
                self.switch_to(self.Student_menu)
            else:
                ct.CTkLabel(frame,text = "Wrong id or password",text_color="red").grid(row = 2,column = 0)
        
        ct.CTkLabel(input,text = "ID",anchor="w").grid(row = 0,column = 0)
        submit = self.button(input,4,0,"login",width = 150,height=30,command=lambda: checkpasswrod(id.get("1.0","end").strip(),password.get("1.0","end").strip()))    
        id = ct.CTkTextbox(input,height = 30,width = 200)
        id.bind("<Return>", self.textbox_tab)
        id.bind("<Tab>", self.textbox_tab)
        id.grid(row = 1,column = 0)
        ct.CTkLabel(input,text = "Password").grid(row = 2,column = 0)
        password = ct.CTkTextbox(input,height = 30,width = 200)
        password.bind("<Return>", lambda x : self.textbox_enter(x,submit))
        password.bind("<Tab>", self.textbox_tab)
        password.grid(row = 3,column = 0,padx = 20)
        # ct.entry
        # ct.label
        back = self.button(input,5,0,"back",width = 150,height=30,pady=(3,20),command = lambda: self.switch_to(self.Control_or_Student)) 
        back.configure(fg_color="red")
        back.configure(hover_color="darkred")
                
        return frame
    
    
    def Student_menu(self):
        frame = self.main_frame()
        
        self.header(frame,"Welcome, " + self.user.name)
        
        f = ct.CTkFrame(frame)
        f.grid(row=1,column=0)
        
        editcourse = self.button(f,0,0,"Courses and Group")
        news = self.button(f,1,0,"News")
        back = self.button(f,2,0,"login screen",command = lambda:self.switch_to(self.Control_or_Student))
        back.configure(fg_color = "red",hover_color = "darkred")
            
        return frame
    #--------------------------------------------

root = ct.CTk()
root.title("Control")
app = App(root)
root.mainloop()

if(False):
    def print_header(header):
        print()
        print("********" + header + "********")
        print()

    def print_warning(warning):
        print()
        print("--------" + warning + "--------")
        print()
        
    def print_options(options):
        for i in range(len(options)):
            print(f"{i+1}) {options[i]}")
        print("0) Exit")

    #working code
    def student_or_control():
        while True:
            print_header("Student or Control")
            print_options(["Student", "Control"])
            i = input().lower()
            if(i == "0"):
                exit()
            elif(i == "1"):
                student_login()
            elif(i == "2"):
                control_login()
            else:
                print()
                print("********Please input a valid input********")
                print()
                student_or_control()

    #Student menus-----------------------------------------------------------
    def student_login():
        print_header("Student login")
        id = input("Enter your id (type 'exit' to return to the main menu): ")
        if(id == "exit"):
            return

        student = Student(id)
        password = input("Enter your password: ")
        
        #replace with the password checking function
        if(student.checkpassword(password)):
            student_menu(student)
        else:
            print()
            print("-------Wrong id or password-------")
            student_login()
    
        
    def student_menu(student):
        while True:
            print_header("\n\nWelcome " + student.name + 
                        "\n|  GPA: " + str(student.GPA) + "\n\n")
            
            print_options(["Courses and Groups", "News"])

            i = input().lower()
            if(i == "0"):
                return
            elif(i == "1"):
                print("********Courses and Groups********")
                print()
                print("Registered Courses:")
                for i in student.courses:
                    print("| " + i)
                print("---------------------------------")
                print("Group: " + student.group)
                print()
                
                while True:
                    print("1) Edit Courses")
                    print("2) Change group")
                    print("0) back")
                    option = input().lower()
                    if(option == "0"):
                        break
                    elif(option == "1"):
                        edit_courses(student)
                    elif(option == "2"):
                        edit_group(student)
            elif(i == "2"):pass
            elif(i == "3"):pass
            else:
                print()
                print("-------Please input a valid input-------")
                print()

    def edit_courses(student):
        while True:
            print("********Add or remove Course********")
            print()
            for i in range(len(Student.all_courses)):
                print(f"{i+1}) [{"*" if Student.all_courses[i] in student.courses else " "}]{Student.all_courses[i]}")
            i = input("insert course number ('exit' to go back): ")
            if(i == "exit"):
                return
            if(not i.isdigit() or int(i) < 1 or int(i) > len(Student.all_courses)):
                print()
                print("-------Please input a valid number-------")
                print()
                continue
            i = int(i) - 1
            if(Student.all_courses[i] in student.courses):
                student.remove_course(Student.all_courses[i])
            else:
                student.add_course(Student.all_courses[i])
            print()


    def edit_group(student):
        while True:
            print("********Edit Group********")
            print()
            for i in range(len(Student.all_groups)):
                print(f"{i+1}) [{"x" if Student.all_groups[i] == student.group else " "}]{Student.all_groups[i]}")
            i = input("Select group ('exit' to go back): ")
            if(i == "exit"):
                return
            if(not i.isdigit() or int(i) < 1 or int(i) > len(Student.all_groups)):
                print()
                print("-------Please input a valid number-------")
                print()
                continue
            i = int(i) - 1
            student.set_group(Student.all_groups[i])
            print()

    #-------------------------------------------------------------------------------

    student_or_control()