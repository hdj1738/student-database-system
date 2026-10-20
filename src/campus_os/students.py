from abc import ABC, abstractmethod
class StudentRecord(ABC):

    @abstractmethod
    def display_details(self):
        pass    

class Student(StudentRecord):
    def __init__(self,id,name, age, course, marks):
        if not id or not name or id<=0 or not age or age<=0 or not course or not marks:
            raise ValueError("Cannot have null or invalid input")
        if (not any(char.isalpha() for char in name)
                or any(not (char.isalpha() or char.isspace() or char in "-.'") for char in name)):
            raise ValueError("Enter a valid student name.")
        self.id=id
        self.name=name
        self.age=age
        self.course=course
        self.marks=marks
     #whatshdastudentclassbeabletodo?
     #display student details
    def display_details(self):
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Course: {self.course}")
        print(f"Marks: {self.marks}")
        print(f"Average: {self.calculate_average()}")
        print(f"Grade: {self.calculate_grade()}")
        highest_subject, highest_mark = self.highest_mark_subject()
        if highest_subject:
            print(f"Highest Mark Subject: {highest_subject}, Mark: {highest_mark}") 
        
        lowest_subject, lowest_mark = self.lowest_mark_subject()
        if lowest_subject:
            print(f"Lowest Mark Subject: {lowest_subject}, Mark: {lowest_mark}") 

    #watstudentshldowidmarks
    def calculate_average(self):
        total_marks = sum(self.marks.values())
        num_subjects = len(self.marks)
        average = total_marks / num_subjects if num_subjects > 0 else 0
        return average
    
    def calculate_grade(self):
        average = self.calculate_average()
        if average >= 90:
            return "S"
        elif average >= 80:
            return "A"
        elif average >= 70:
            return "B"
        elif average >= 60:
            return "C"
        elif average >= 50:
            return "D"
        else:
            return "F"

    def highest_mark_subject(self):
                if not self.marks:
                    return None, None
                highest_subjects=[]
                highest_mark=max(self.marks.values())
                for k in self.marks.keys():
                    if self.marks[k]==highest_mark:
                        highest_subjects.append(k)
                    
                return ",".join(highest_subjects),highest_mark

    def lowest_mark_subject(self):
            if not self.marks:
                return None, None
            lowest_subjects=[]
            lowest_mark=min(self.marks.values())
            for k in self.marks.keys():
                if self.marks[k]==lowest_mark:
                    lowest_subjects.append(k)
                
            return ",".join(lowest_subjects),lowest_mark
class Password():
    def __init__(self,pw):
        if not pw:
            raise ValueError("Cannot have null or invalid input")
        self.__pw=pw

    @property
    def pw(self):
        return self.__pw
    
    @pw.setter
    def pw(self,pswd):
        if not pswd:
            raise ValueError("Password cannot be empty.")
        self.__pw =pswd
