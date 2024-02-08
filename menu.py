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


#working code
def student_or_control():
    while True:
        print("\nSign in as....\n")
        print("1) Student")
        print("2) Control")
        print("0) Exit")
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

#Student menus
def student_login():
    print()
    print("********Student login********")
    print()
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
    print("********Welcome " + student.name + " ********")
    print("Please select an action")
    print()
    while True:
        print()
        print("1) Courses and Groups")
        print("2) GPA")
        print("3) News")
        print("0) main menu")

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

student_or_control()