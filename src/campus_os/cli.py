from campus_os.validation import get_valid_marks, get_valid_input
from campus_os.storage import save_students, load_students
from campus_os.students import Student

def main():
    students=load_students()
    while True:
        print("\n---- STUDENT MANAGEMENT MENU ----")
        print("1. Add students")
        print("2. Search student")
        print("3. Update student or marks")
        print("4. Delete student or mark")
        print("5. Display all students")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            n = get_valid_input("Enter number of students: ", int, positive=True)
            for _ in range(n):
                student_id = get_valid_input("Enter student id: ", int, positive=True)
                while any(student.id == student_id for student in students):
                    print("Duplicate student IDs are not allowed.")
                    student_id = get_valid_input("Enter student id: ", int, positive=True)
                age = get_valid_input("Enter student age: ", int, positive=True)
                name = get_valid_input("Enter student name: ", str)
                course = get_valid_input("Enter student course: ", str).lower()
                students.append(Student(student_id, name, age, course, get_valid_marks()))
            save_students(students)
        elif choice == "2":
            search_details(students)
        elif choice == "3":
            update_details(students)
            save_students(students)
        elif choice == "4":
            delete_details(students)
            save_students(students)
        elif choice == "5":
            if students!=[]:
                for student in students:
                    student.display_details()
            else:
                print("No students to display.")
        elif choice == "6":
            save_students(students)
            print("Exiting Student Management System.")
            return
        else:
            print("Invalid choice. Enter a number from 1 to 6.")

def search_details(students):
    found=False
    search = get_valid_input("Enter id that you want to search: ", int, positive=True)
    for student in students:
        if student.id==search:
            found=True
            student.display_details()
            break
    if not found:
        print("Student record with such id doesn't exist.") 

def update_details(students):
    found=False
    attribute_types = {"id": int,"name":str,"age":int,"course":str} 
    while True:
        changename = get_valid_input("Enter the attribute that you want to change: ", str).lower()
        if changename in attribute_types or changename == "marks":
            break
        print("Invalid attribute. Choose id, name, age, course, or marks.")
    changeid = get_valid_input("Enter the id of the student whose value you want to change: ", int , positive=True)
    if changename!="marks":
        newid = get_valid_input(f"Enter {changename} that you want to replace it with: ", attribute_types[changename])
        if changename == "id" and any(student.id == newid for student in students):
            print("Duplicate student IDs are not allowed.")
            return
        for student in students:
            if student.id==changeid:
                found=True
                setattr(student, changename,newid)
                break
        if not found:
            print("Student record with such id doesn't exist.")   
    else:
        for student in students:
            if student.id==changeid:
                found=True
                while True:
                    subject=get_valid_input("Enter subject:",str)
                    if subject in student.marks:
                        break
                    print("Cannot update subject that does not exist.")
                while True:
                    newmark=get_valid_input("Enter mark:",int)
                    if newmark>=0 and newmark<=100:
                        break
                    print("Number can only be between 0 and 100, 0 included.")
                
                student.marks[subject]=newmark
                break
        if not found:
            print("Student record with such id doesn't exist.")  

def delete_details(students):
    while True:
        found=False
        deletename = get_valid_input("Do you want to delete the student or mark: ", str).lower()
        if deletename=="student":
                deleteid = get_valid_input("Enter the id of the student whose value you want to delete: ", int , positive=True)
                for student in students:
                    if student.id==deleteid:
                        found=True
                        students.remove(student)
                        break
                if not found:
                    print("Student record with such id doesn't exist.")
                else:
                    break

        elif deletename=="mark":
            deleteid = get_valid_input("Enter the id of the student whose value you want to delete: ", int , positive=True)
            for student in students:
                if student.id==deleteid:
                    found=True
                    while True:
                        subject=get_valid_input("Enter the subject of the student whose mark you want to delete: ",str)
                        if subject in student.marks:
                            student.marks.pop(subject)
                            break
                        print("Cannot delete subject that does not exist.")
                    break
            if not found:
                print("Student record with such id doesn't exist.")
            else: 
                print("Successfully deleted the mark.")
                break
        else:
            print("Can only delete student or mark.")
    
    