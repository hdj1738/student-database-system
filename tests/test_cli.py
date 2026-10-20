from campus_os import cli
from campus_os.students import Student


def test_main_rejects_duplicate_id_when_adding_student(monkeypatch, capsys):
    existing = Student(1, "Ada", 20, "computing", {"Math": 90})
    monkeypatch.setattr(cli, "load_students", lambda: [existing])
    monkeypatch.setattr(cli, "save_students", lambda _students: None)
    values = iter([1, 1, 2, 18, "Nia", "computing"])
    monkeypatch.setattr(cli, "get_valid_input", lambda *_args, **_kwargs: next(values))
    monkeypatch.setattr(cli, "get_valid_marks", lambda: {"Math": 80})
    choices = iter(["1", "6"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(choices))

    cli.main()

    output = capsys.readouterr().out
    assert "Duplicate student IDs are not allowed." in output
    assert "Exiting Student Management System." in output


def test_search_details_reports_missing_student(monkeypatch, capsys):
    monkeypatch.setattr(cli, "get_valid_input", lambda *_args, **_kwargs: 99)

    cli.search_details([Student(1, "Ada", 20, "computing", {"Math": 90})])

    assert "Student record with such id doesn't exist." in capsys.readouterr().out


def test_auth_retries_wrong_password_then_enters_cli(monkeypatch):
    from campus_os import validation

    answers = iter(["wrong", "hiralissocool"])
    entered = []
    monkeypatch.setattr(validation, "get_valid_input", lambda *_args, **_kwargs: next(answers))
    monkeypatch.setattr(cli, "main", lambda: entered.append(True))

    import runpy

    runpy.run_module("campus_os.auth", run_name="__main__")

    assert entered == [True]


def test_main_exit(monkeypatch, capsys):
    monkeypatch.setattr(cli, "load_students", lambda: [])

    saved = []
    monkeypatch.setattr(
        cli, "save_students",
        lambda students: saved.append(list(students))
    )

    inputs = iter(["6"])
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(inputs)
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Exiting Student Management System." in output
    assert saved == [[]]


def test_main_invalid_choice(monkeypatch, capsys):
    monkeypatch.setattr(cli, "load_students", lambda: [])
    monkeypatch.setattr(cli, "save_students", lambda students: None)

    inputs = iter(["9", "6"])
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(inputs)
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Invalid choice." in output
    assert "Exiting Student Management System." in output


def test_main_adds_student_and_saves(monkeypatch):
    from campus_os import cli

    saved = []
    monkeypatch.setattr(cli, "load_students", lambda: [])
    monkeypatch.setattr(
        cli, "save_students",
        lambda students: saved.append(list(students))
    )

    values = iter([1, 1, 20, "Ada", "Computer Science"])
    monkeypatch.setattr(
        cli, "get_valid_input",
        lambda *_args, **_kwargs: next(values)
    )
    monkeypatch.setattr(
        cli, "get_valid_marks",
        lambda: {"Math": 90}
    )

    choices = iter(["1", "6"])
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(choices)
    )

    cli.main()

    assert len(saved[-1]) == 1
    student = saved[-1][0]
    assert student.id == 1
    assert student.name == "Ada"
    assert student.age == 20
    assert student.marks == {"Math": 90}


def test_update_details_changes_student_name(monkeypatch):
    from campus_os import cli
    from campus_os.students import Student

    student = Student(1, "Ada", 20, "computing", {"Math": 90})

    values = iter(["name", 1, "Grace"])
    monkeypatch.setattr(
        cli, "get_valid_input",
        lambda *_args, **_kwargs: next(values)
    )

    cli.update_details([student])

    assert student.name == "Grace"


def test_update_details_changes_mark(monkeypatch):
    from campus_os import cli
    from campus_os.students import Student

    student = Student(1, "Ada", 20, "computing", {"Math": 90})

    values = iter(["marks", 1, "Math", 75])
    monkeypatch.setattr(
        cli, "get_valid_input",
        lambda *_args, **_kwargs: next(values)
    )

    cli.update_details([student])

    assert student.marks["Math"] == 75


def test_update_details_rejects_duplicate_id(monkeypatch, capsys):
    from campus_os import cli
    from campus_os.students import Student

    first = Student(1, "Ada", 20, "computing", {"Math": 90})
    second = Student(2, "Grace", 21, "computing", {"Math": 85})

    values = iter(["id", 1, 2])
    monkeypatch.setattr(
        cli, "get_valid_input",
        lambda *_args, **_kwargs: next(values)
    )

    cli.update_details([first, second])

    output = capsys.readouterr().out

    assert "Duplicate student IDs are not allowed." in output
    assert first.id == 1
    assert second.id == 2


def test_delete_details_removes_student(monkeypatch):
    from campus_os import cli
    from campus_os.students import Student

    student = Student(1, "Ada", 20, "computing", {"Math": 90})
    students = [student]

    values = iter(["student", 1])
    monkeypatch.setattr(
        cli, "get_valid_input",
        lambda *_args, **_kwargs: next(values)
    )

    cli.delete_details(students)

    assert students == []


def test_delete_details_removes_mark(monkeypatch):
    from campus_os import cli
    from campus_os.students import Student

    student = Student(
        1, "Ada", 20, "computing",
        {"Math": 90, "Physics": 85}
    )
    students = [student]

    values = iter(["mark", 1, "Math"])
    monkeypatch.setattr(
        cli, "get_valid_input",
        lambda *_args, **_kwargs: next(values)
    )

    cli.delete_details(students)

    assert "Math" not in student.marks
    assert student.marks["Physics"] == 85
