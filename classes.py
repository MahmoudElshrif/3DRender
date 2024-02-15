import json,os

#---------temporary test functions and classes, replace with the working ones---------
def get_student_dict(name,password,group,courses,gpa,level):
    return {"name":name,"password":password,"group":group,"courses":courses,"gpa":gpa,"level":level}

class Student:
    all_courses = {}
    all_groups = ["A","B","C"]
    all_students = {}
    
    def __init__(self,id):
        self.id = id
    
    @staticmethod
    def Add_Student(id,name,password,group,courses,gpa,level):
        Student.all_students[id] = get_student_dict(name,password,group,courses,gpa,level)
        
        with open("data/students.json","w") as f:
            json.dump(Student.all_students,f)
    
    @staticmethod
    def checkpassword(id,password):
        if(id not in Student.all_students):
            return False
        return Student.all_students[id]["password"] == password
    
    def add_course(self,course):
        self.courses.append(course)
    
    def remove_course(self,course):
        self.courses.remove(course)

    def set_group(self,group):
        self.group = group
        
    @staticmethod
    def register_course(course_name,course_id):
        Student.all_courses.append(course_name)
    
    @staticmethod
    def delete_course():
        pass

class Control:
    def __init__(self,id):
        self.id = id
        self.name = "Control"

    @staticmethod
    def checkpassword(id,password):
        return (id == password) and (id == "admin")

#------------------------------------------------------------------------------------------

if os.path.exists("data/students.json"):
    with open("data/students.json","r") as f:
        Student.all_students = json.load(f)
else:
    os.mkdir("data")
if os.path.exists("data/courses.json"):
    with open("data/courses.json","r") as f:
        Student.all_courses = json.load(f)