class Controller:
    def __init__(self,password,id):#this for controller to login 
        self.__id = id
        # self.__name=name
        # self.__level=level
        # self.__GPA=GPA
        self.__password=password
    @staticmethod
    def Add_student(id,name=0,password=0,level=0,GPA=0,group=0):
        pass
    @staticmethod
    def Remove_student(id):
        pass
    @staticmethod
    def Edit_information(newid,newname,newpassword,newlevel,newGPA,newGroup):
        pass
    @staticmethod
    def Add_course(course_name,course_id):
        pass
    def Remove_course(course_id):
        pass



class Student:
    def __init__(self,name,id) :
        pass

    @staticmethod
    def Register_course(course_name,course_id):
        pass
    def Edit_course():
        pass
    def Choose_group():
        pass



