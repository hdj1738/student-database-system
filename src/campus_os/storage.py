import csv
from campus_os.students import Student
def save_students(students):
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["id", "name", "age", "course", "marks"])

        for student in students:
            marks = "|".join(
                f"{subject}:{mark}"
                for subject, mark in student.marks.items()
            )

            writer.writerow([
                student.id,
                student.name,
                student.age,
                student.course,
                marks
            ])


def load_students():
    students = []

    try:
        with open("students.csv", "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                marks = {}

                for item in row["marks"].split("|"):
                    subject, mark = item.split(":")
                    marks[subject] = int(mark)

                student = Student(
                    int(row["id"]),
                    row["name"],
                    int(row["age"]),
                    row["course"],
                    marks
                )

                students.append(student)

    except FileNotFoundError:
        print("No student file found. Starting with empty records.")

    return students