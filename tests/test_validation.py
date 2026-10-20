import pytest

from campus_os.validation import get_valid_input, get_valid_marks


@pytest.mark.parametrize(
    ("inputs", "value_type", "positive", "expected"),
    [
        (["nope", "4"], int, False, 4),
        (["0", "3"], int, True, 3),
        (["  ", "Ada Lovelace"], str, False, "Ada Lovelace"),
    ],
)
def test_get_valid_input_retries_until_valid(monkeypatch, capsys, inputs, value_type, positive, expected):
    answers = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    result = get_valid_input("Enter value: ", value_type, positive=positive)

    assert result == expected
    assert capsys.readouterr().out


@pytest.mark.parametrize("value", ["123", "Ada!"])
def test_get_valid_input_rejects_invalid_names(monkeypatch, value):
    answers = iter([value, "Ada Lovelace"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    assert get_valid_input("Enter name: ", str) == "Ada Lovelace"


def test_get_valid_marks_retries_malformed_and_out_of_range(monkeypatch, capsys):
    answers = iter(["Math", "Math,101", "Math,90 Python,85"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    assert get_valid_marks() == {"Math": 90, "Python": 85}
    assert capsys.readouterr().out
