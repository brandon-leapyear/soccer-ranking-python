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

    assert teams["Foo"] == Score(1, -1)
    assert teams["Bar"] == Score(3, 0)
    assert teams["Baz"] == Score(4, 1)

def test_rank_teams():
    teams = {
        "D": Score(40, 0),
        "A": Score(40, 0),
        "B": Score(10, 0),
        "C": Score(15, 0),
        "E": Score(15, 10),
    }

    assert rank_teams(teams) == [
        Ranking(1, "A", 40, 0),
        Ranking(1, "D", 40, 0),
        Ranking(3, "E", 15, 10),
        Ranking(4, "C", 15, 0),
        Ranking(5, "B", 10, 0),
    ]

def test_group_by():
    arr = [1, 1, 1, 2, 2, 3, 3, 3]
    assert group_by(arr, key=lambda x: x) == [[1, 1, 1], [2, 2], [3, 3, 3]]

    arr = ['a', 'aardvark', 'avalanche', 'bee', 'car', 'cymbal']
    assert group_by(arr, key=lambda s: s[0]) == [['a', 'aardvark', 'avalanche'], ['bee'], ['car', 'cymbal']]
