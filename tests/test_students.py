import pytest

from campus_os.students import Password, Student


@pytest.fixture
def student():
    return Student(7, "Ada Lovelace", 20, "computing", {"Math": 92, "History": 84})


def test_student_stores_constructor_values(student):
    assert (student.id, student.name, student.age, student.course) == (
        7, "Ada Lovelace", 20, "computing"
    )
    assert student.marks == {"Math": 92, "History": 84}


@pytest.mark.parametrize(
    "args",
    [
        (0, "Ada", 20, "computing", {"Math": 90}),
        (7, "", 20, "computing", {"Math": 90}),
        (7, "Ada", 0, "computing", {"Math": 90}),
        (7, "Ada", 20, "", {"Math": 90}),
        (7, "Ada", 20, "computing", {}),
    ],
)
def test_student_rejects_missing_or_nonpositive_required_values(args):
    with pytest.raises(ValueError):
        Student(*args)


@pytest.mark.parametrize("name", ["123", "Ada_1", "Ada!"])
def test_student_rejects_invalid_names(name):
    with pytest.raises(ValueError):
        Student(1, name, 20, "computing", {"Math": 90})


@pytest.mark.parametrize(
    ("marks", "average", "grade"),
    [
        ({"Math": 90, "Art": 90}, 90, "S"),
        ({"Math": 85, "Art": 75}, 80, "A"),
        ({"Math": 75, "Art": 65}, 70, "B"),
        ({"Math": 65, "Art": 55}, 60, "C"),
        ({"Math": 55, "Art": 45}, 50, "D"),
        ({"Math": 49, "Art": 49}, 49, "F"),
    ],
)
def test_average_and_grade_calculations(marks, average, grade):
    record = Student(1, "Ada", 20, "computing", marks)

    assert record.calculate_average() == average
    assert record.calculate_grade() == grade


def test_highest_and_lowest_marks_include_tied_subjects(student):
    tied = Student(2, "Grace Hopper", 30, "computing", {"Math": 100, "Art": 20, "CS": 100, "PE": 20})

    assert tied.highest_mark_subject() == ("Math,CS", 100)
    assert tied.lowest_mark_subject() == ("Art,PE", 20)
    assert student.highest_mark_subject() == ("Math", 92)
    assert student.lowest_mark_subject() == ("History", 84)


def test_password_property_can_read_and_update_password():
    password = Password("secret")
    assert password.pw == "secret"

    password.pw = "updated"
    assert password.pw == "updated"


@pytest.mark.parametrize("value", [None, ""])
def test_password_rejects_empty_value(value):
    with pytest.raises(ValueError):
        Password(value)

    password = Password("secret")
    with pytest.raises(ValueError):
        password.pw = value
