import pytest

from soccer_ranking import *

def test_parse_game():
    assert parse_game("Team Foo 10, Bar 20") == Game("Team Foo", 10, "Bar", 20)

def test_score_teams():
    teams = score_teams([
        Game("Foo", 1, "Bar", 2),
        Game("Foo", 1, "Baz", 1),
        Game("Bar", 1, "Baz", 2),
    ])

    assert teams["Foo"] == 1
    assert teams["Bar"] == 3
    assert teams["Baz"] == 4

def test_rank_teams():
    teams = {
        "D": 40,
        "A": 40,
        "B": 10,
        "C": 15,
    }

    assert rank_teams(teams) == [
        Ranking(1, "A", 40),
        Ranking(1, "D", 40),
        Ranking(3, "C", 15),
        Ranking(4, "B", 10),
    ]

def test_group_by():
    arr = [1, 1, 1, 2, 2, 3, 3, 3]
    assert group_by(arr, key=lambda x: x) == [[1, 1, 1], [2, 2], [3, 3, 3]]

    arr = ['a', 'aardvark', 'avalanche', 'bee', 'car', 'cymbal']
    assert group_by(arr, key=lambda s: s[0]) == [['a', 'aardvark', 'avalanche'], ['bee'], ['car', 'cymbal']]
