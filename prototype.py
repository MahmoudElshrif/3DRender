#---------temporary test functions and classes, replace with the working ones---------
class Student:
    all_courses = ["Course A","Course B","Course C","Course D","Course E"]
    all_courses = {i[0] + i[-1] : i for i in all_courses}
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
        
    @staticmethod
    def Register_course(course_name,course_id):
        Student.all_courses.append(course_name)
    
    @staticmethod
    def remove_course():
        pass
    
    @staticmethod
    def add_group():
        pass
    
    @staticmethod
    def remove_group():
        pass

class Control:
    def __init__(self,id):
        self.id = id
        self.name = "Control"

    def checkpassword(self,password):
        return (self.id == password) and (self.id == "admin")

#------------------------------------------------------------------------------------------