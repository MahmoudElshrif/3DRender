#---------temporary test functions and classes, replace with the working ones---------
import os
import json

dict_file="main_data"
def load_dict():
    if os.path.exists(dict_file):
        with open(dict_file,'r') as f:
            return json.load(f)
    else:
        return {}
def save_dict(dict):
    with open(dict_file,'w') as f:
        return json.dump(dict,f,indent=2)






id_file="id_list"
def load_id():
    if os.path.exists(id_file):
        with open(id_file,'r') as f:
            return json.load(f)
    else:
        return []

def save_id(id):
    with open(id_file,'w') as f:
        return json.dump(id,f,indent=2)







allgroup=["A","B","C","D"]
courses_file="courses"
def load_courses():
    if os.path.exists(courses_file):
        with open(courses_file,'r') as f:
            return json.load(f)
    else:
        return []

def save_course(course):
    with open(courses_file,'w') as f:
        return json.dump(course,f,indent=2)

allcourses=load_courses()
allcourses=["math","logic","oop"]
save_course(allcourses)
courses_list=[]



class Student:
    def __init__(self) :
        pass
    @staticmethod
    def register_course(id):
        allcourses=load_courses()
        u=Controller.id_checker2(id)
        students_dict=load_dict()
        for i , k in students_dict.items():
            for l , j in k.items():
                if u == j:
                    name=iذ

        for i in range(1):#this is to enter courses for student
            y=list(students_dict[name]["courses"])
            

            courses=[]
            while True:
                user=input("enter  course name ")

                while True:#checker for courses
                    if user in allcourses:
                        if user in courses:

                            user=input("you have entered this before")
                        if user in y:
                            user=input("you have this course")
                                
                        else:
                            courses.append(user)
                            y.append(user)
                            break




                    else:
                        user=input("enter valid course")
                    


                
                if len(courses)==3: #this for choose courses this condition is temprorary you can chage it محمود فتحي
                    break

            students_dict[name]["courses"]=y
            save_dict(students_dict)
    @staticmethod
    def Remove_course(id):
        students_dict=load_dict()
        u=Controller.id_checker2(id)
        for i , k in students_dict.items():
            for l , j in k.items():
                if u == j:
                    name=i
        y=list(students_dict[name]["courses"])
        while True:
            user=input("enter the course you want to remove")
            if user in y:
                y.remove(user)
                students_dict[name]["courses"]=y
                save_dict(students_dict)

                break
            else:
                print("this course doesnt exist")
    @staticmethod
    def choose_group(id):
        students_dict=load_dict()
        u=Controller.id_checker2(id)
        for i , k in students_dict.items():
            for l , j in k.items():
                if u == j:
                    name=i
        group=input(f"choose from available groups {allgroup}")
        group=Controller.group_checker(group)
        students_dict[name]["group"]=group
        save_dict(students_dict)
        



class Controller(Student):
    mydict=[]
    def __init__(self,password,id):
        self.id = id
        self.password=password
    @staticmethod
    def password_checker(password):
        while True:
            if len(password)>8:
                return password
                
            
            else:
                password=input("password must be 8 character long")
    @staticmethod
    def id_checker(id):
        while True:
            id_list=load_id()
            if id in id_list:
                id=input("this id  existed before")


            else:
                return id
    @staticmethod
    def id_checker2(id):
        while True:
            id_list=load_id()
            if id in id_list:
                return id
            else:
                id=input("this id doesnt exit")

    @staticmethod
    def group_checker(group):
        while True:
            if group in allgroup:
                return group
            else:
                group=input("this group doesnt exist")
    @staticmethod
    def gpa_checker(gpa):

        while True:
            try:
                int(gpa)
                break
            except ValueError:                           
                try:
                    float(gpa)
                    break

                except ValueError:
                    gpa=input ("This is not a number")
        while True:
            if float(gpa)>4:
                gpa=input("You have entered gpa bigger than 4")
            else:
                return gpa




    @staticmethod
    def Add_student():
        allcourses=load_courses()
        name=input("enter name")

        password=input("enter student password")
        password=Controller.password_checker(password)
        id=input("enter student id")

        id=Controller.id_checker(id)
        id_list=load_id()
        id_list.append(id)
        save_id(id_list)

        # id_list.append(id)
        

        gpa=input("enter student GPA")
        gpa=Controller.gpa_checker(gpa)

        

        for i in range(1):#this is to enter courses for student
            courses_list.clear()
            courses=[]
            while True:
                user=input("enter  course name ")

                while True:#checker for courses
                    if user in allcourses:
                        if user in courses:
                            user=input("you have entered this before")
                        else:
                            courses.append(user)
                            break




                    else:
                        user=input("enter valid course")
                    


                
                if len(courses)==1: #this for choose courses this condition is temprorary you can chage it محمود فتحي
                    break


            courses_list.extend(courses)

        return name,password,id,gpa
        

    @staticmethod
    def Remove_student(id):
        students_dict=load_dict()
        u=Controller.id_checker2(id)
        for i,k in students_dict.items():
            for l , j in k.items():
                if u == j:
                    name=i
        students_dict.pop(name)
        save_dict(students_dict)

    @staticmethod
    def See_information(id):
        students_dict=load_dict()
        u=Controller.id_checker2(id)
        for i , k in students_dict.items():
            for l , j in k.items():
                if u == j:
                    name=i

            
        print(f"name: {name}")
        print(f"Password: {students_dict[name]["password"]}")
        print(f"Courses: {students_dict[name]["courses"]}")
        print(f"GPA: {students_dict[name]["gpa"]}")
        print(f"Group : {students_dict[name]["group"]}")

    @staticmethod
    def Add_general_course(name):
        allcourses=load_courses()
        if name in allcourses:
            print("This course was added before")
        else:
            allcourses.append(name)
            save_course(allcourses)
    @staticmethod
    def Remove_general_course(name):
        allcourses=load_courses()
        while True:
            if name in allcourses:
                allcourses.remove(name)
                save_course(allcourses)
                break
            else:
                name=input("there is no course with this name")
        
    @staticmethod 
    def Edit_information(id):
        id_list=load_id()
        students_dict=load_dict()
        u=Controller.id_checker2(id)
        for i , k in students_dict.items():
            for l , j in k.items():
                if u == j:
                    name=i
        
        y=input(""" what do you want to change?
                a)id
                b)name
                c)password
                d)GPA
                """).lower()
        while True:
            if y =="a":
                new_id=input("enter the new id")

                while True:

                    if new_id in id_list:
                        new_id=input("you have this id before")

                    else:
                        students_dict[name]["id"]=new_id
                        save_dict(students_dict)
                        id_list.remove(u)
                        id_list.append(new_id)
                        save_id(id_list)
                        break
                break
            elif y =="b":
                new_name=input("enter new name")
                students_dict[new_name]=students_dict.pop(name)
                save_dict(students_dict)
                break
            elif y=="c":
                new_password=input("enter the new password")
                
                
                students_dict[name]["password"]=Controller.password_checker(new_password)
                save_dict(students_dict)
                break
            elif y=="d":
                new_GPA=input("enter new GPA")
                while True:
                    if float(new_GPA)>4:
                        new_GPA=input("You have entered gpa bigger than 4")
                    else:
                        students_dict[name]["gpa"]=new_GPA
                        save_dict(students_dict)
                        break
                break

            else:
                u=input("enter valid choice")
#------------------------------------------------------------------------------------------


def student_login():
    while True:
        user=input(""" what do you want to do?
                A)register course
                B)remove course
                C)Choose group
                D)change group
                E)exit

                """).capitalize()
        if user == "A":
            Student.register_course("20")#محمود فتحي put the id in the parameter that the student enter
        elif user =="B":
            Student.Remove_course("20")#محمود فتحي put the id in the parameter that the student enter
        elif user == "C":
            Student.choose_group("20")#محمود فتحي put the id in the parameter that the student enter
        elif user =="D":
            Student.choose_group("20")#محمود فتحي put the id in the parameter that the student enter 
        elif user == "E":
            break
        else:
            print("enter valid choice")
            student_login()
def control_login():
    while True:
        user=input(""" what do you want to do
                   A)add Student
                   B)remove student
                   C)see information
                   D)add course
                   E)remove course
                   F)edit information
                   G)exit
                   """).capitalize()
        if user=="A":
            students_dict=load_dict()
            u,v,x,o=Controller.Add_student()
            students_dict[u]={
                "id":x,
                "password":v ,
                "courses":courses_list,
                "group":"A",
                "gpa":o
 
            }
            save_dict(students_dict)

        elif user=="B":
            Controller.Remove_student(input("enter student id "))
        elif user=="C":

            Controller.See_information(input("enter student id"))
        elif user=="D":
            Controller.Add_general_course(input("enter course name"))
        elif user=="E":
            Controller.Remove_general_course("enter course name")
        elif user=="F":
            Controller.Edit_information("enter student id")
        elif user=="G":
            break
        
        



#working code
def student_or_control():
    while True:
        print("\nSign in as....\n")
        print("A) Student")
        print("B) Control")
        print("C) Exit")
        i = input().lower()
        if(i == "c"):
            exit()
        elif(i == "a"):
            student_login()
        elif(i == "b"):
            control_login()
        else:
            print()
            print("********Please input a valid input********")
            print()
            student_or_control()

# students_dict=load_dict()
# id_list=load_id()
# students_dict.clear()
# allcourses.clear()
# id_list.clear()
# save_course(allcourses)
# save_dict(students_dict)
# save_id(id_list)      
student_or_control()

