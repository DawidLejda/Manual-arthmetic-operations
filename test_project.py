from project import (
    input_to_list,
    string_modification,
    multi_addition,
    subtracting_division,
)
import pytest


def test_invalid_input():
    with pytest.raises(ValueError):
        assert input_to_list("10+/5")
        assert input_to_list("52+!63")
        assert input_to_list("10-50")
        assert input_to_list("63")
        assert input_to_list("+63")
        assert input_to_list("-63")
        assert input_to_list("")
        assert input_to_list("0")


def test_input_to_list():
    assert input_to_list("1525+70") == ([1, 5, 2, 5], [7, 0], "+", 2, 6)


def test_string_modification():
    assert string_modification([" ", 5, 1, 2, 5], [0, 1, 0, 0, 0]) == [
        " ",
        "̶5",
        1,
        2,
        5,
    ]


def test_multi_addition():
    assert multi_addition([" ", 0, 3, 6, 9], [" ", 2, 4, 6, " "], 5) == [
        " ",
        2,
        8,
        2,
        9,
    ]
    assert multi_addition([" ", 2, 8, 2, 9], [1, 2, 3, " ", " "], 5) == [1, 5, 1, 2, 9]


def test_subtracting_division():
    assert subtracting_division([6, 7, 3, 2], [5, 9, 7, 1], 4) == [" ", 7, 6, 1]
