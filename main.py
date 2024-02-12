from prototype import *
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
        
        PagesManger(self.master)

    
    # def switch_to(self,page):
    #     if(self.current):
    #         self.current.grid_forget()
        
    #     frame = self.pages[page]
    #     frame.grid(row=0,column=0)
    #     self.current = frame
    #     pass
    
    
    
    
    
    
    def login(self):
        
        frame = self.main_frame()
        
        self.header(frame,"Sign in...")
        
        input = ct.CTkFrame(frame)
        input.grid(row=1,column=0)
        
        def checkpasswrod(id, password,student):
            if(student):
                user = Student(id)
            else:
                user = Control(id)
            if(user.checkpassword(password)):
                self.user = user
                if(student):
                    self.switch_to(self.Student_menu)
                else:
                    self.switch_to(self.Control_menu)
            else:
                ct.CTkLabel(frame,text = "Wrong id or password",text_color="red").grid(row = 2,column = 0)
        
        
        ct.CTkLabel(input,text = "ID",anchor="w").grid(row = 0,column = 0)
        id = ct.CTkTextbox(input,height = 30,width = 200)
        id.bind("<Return>", self.textbox_tab)
        id.bind("<Tab>", self.textbox_tab)
        id.grid(row = 1,column = 0)
        ct.CTkLabel(input,text = "Password").grid(row = 2,column = 0)
        
        password = ct.CTkTextbox(input,height = 30,width = 200)
        password.bind("<Return>", lambda x : self.textbox_enter(x,studentlogin))
        password.bind("<Tab>", self.textbox_tab)
        password.grid(row = 3,column = 0,padx = 20)
        
        soc = ct.CTkFrame(input,fg_color="transparent") #soc = Student or Control
        soc.grid(row = 4,column = 0)
        
        studentlogin = self.button(soc,0,0,"Student login",width = 90,height=30,padx=5,command=lambda: checkpasswrod(id.get("1.0","end").strip(),password.get("1.0","end").strip(),True))    
        controllogin = self.button(soc,0,1,"Control login",width = 90,height=30,padx=5,command=lambda: checkpasswrod(id.get("1.0","end").strip(),password.get("1.0","end").strip(),False))    
        
        back = self.button(input,5,0,"back",width = 215,height=30,pady=(3,20),command = lambda: self.switch_to(self.Control_or_Student)) 
        back.configure(fg_color="red")
        back.configure(hover_color="darkred")
                
        return frame
    
    
    #Student menus-------------------------------
    def Student_menu(self):
        frame = self.main_frame()
        
        self.header(frame,"Welcome, " + self.user.name)
        
        f = ct.CTkFrame(frame)
        f.grid(row=1,column=0)
        
        editcourse = self.button(f,0,0,"Courses and Group")
        news = self.button(f,1,0,"News")
        back = self.button(f,2,0,"login screen",command = lambda:self.switch_to(self.login))
        back.configure(fg_color = "red",hover_color = "darkred")
            
        return frame
    #--------------------------------------------
    
    #Control menus-------------------------------
    def Control_menu(self):
        frame = self.main_frame()
        
        self.header(frame,"Welcome, " + self.user.name)
        
        f = ct.CTkFrame(frame)
        f.grid(row=1,column=0)
        
        editcourse = self.button(f,0,0,"Manage Students")
        news = self.button(f,1,0,"Add News")
        back = self.button(f,2,0,"login screen",command = lambda:self.switch_to(self.login))
        back.configure(fg_color = "red",hover_color = "darkred")
            
        return frame

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