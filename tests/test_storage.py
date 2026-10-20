import pytest

from campus_os import storage
from campus_os.students import Student


@pytest.fixture
def records():
    return [Student(1, "Ada Lovelace", 20, "computing", {"Math": 90, "Art": 85})]


def test_save_and_load_students_round_trip(tmp_path, monkeypatch, records):
    monkeypatch.chdir(tmp_path)

    storage.save_students(records)
    loaded = storage.load_students()

    assert [(s.id, s.name, s.age, s.course, s.marks) for s in loaded] == [
        (1, "Ada Lovelace", 20, "computing", {"Math": 90, "Art": 85})
    ]


def test_load_missing_file_returns_empty_list(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert storage.load_students() == []
    assert "No student file found" in capsys.readouterr().out


@pytest.mark.parametrize(
    "contents",
    [
        "id,name,age,course,marks\n1,Ada,20,computing,Math:broken\n",
        "id,name,age,course,marks\n1,Ada,twenty,computing,Math:90\n",
        "id,name,age,course\n1,Ada,20,computing\n",
    ],
)
def test_load_malformed_csv_surfaces_parse_error(tmp_path, monkeypatch, contents):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "students.csv").write_text(contents, encoding="utf-8")

    with pytest.raises((ValueError, KeyError)):
        storage.load_students()


def test_load_csv_preserves_duplicate_ids(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "students.csv").write_text(
        "id,name,age,course,marks\n1,Ada,20,computing,Math:90\n1,Grace,30,computing,Math:85\n",
        encoding="utf-8",
    )

    loaded = storage.load_students()

    assert [student.id for student in loaded] == [1, 1]
