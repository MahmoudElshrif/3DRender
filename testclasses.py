#---------temporary test functions and classes, replace with the working ones---------
class Student:
    all_courses_names = ["Course {:02d}".format(i) for i in range(10)]
    all_courses = {(i[:2].upper() + "1" + i[-2:]) : i for i in all_courses_names}
    all_groups = ["A","B","C","D"]
    def __init__(self,id):
        self.id = id
        self.name = "Student"
        self.password = "Password"
        self.courses = list(self.all_courses.keys())[:5]
        self.group = "A"
        self.GPA = 4.0
        self.level = 1
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
    def register_course(course_name,course_id):
        Student.all_courses.append(course_name)
    
    @staticmethod
    def delete_course():
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