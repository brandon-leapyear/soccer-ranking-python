from collections import defaultdict
from typing import Callable, List, Mapping, NamedTuple, TypeVar

class Ranking(NamedTuple):
    rank: int
    team: str
    score: int

def get_rankings(lines: List[str]) -> List[Ranking]:
    games = [parse_game(line) for line in lines]
    teams = score_teams(games)
    return rank_teams(teams)

class Game(NamedTuple):
    team1_name: str
    team1_score: int
    team2_name: str
    team2_score: int

def parse_game(line: str) -> Game:
    team1, team2 = line.split(", ")
    team1_name, team1_score = team1.rsplit(" ", 1)
    team2_name, team2_score = team2.rsplit(" ", 1)

    return Game(
        team1_name=team1_name,
        team1_score=int(team1_score),
        team2_name=team2_name,
        team2_score=int(team2_score),
    )

def score_teams(games: List[Game]) -> Mapping[str, int]:
    scores = defaultdict(int)

    for game in games:
        if game.team1_score > game.team2_score:
            scores[game.team1_name] += 3
            scores[game.team2_name] += 0
        elif game.team1_score < game.team2_score:
            scores[game.team1_name] += 0
            scores[game.team2_name] += 3
        else:
            scores[game.team1_name] += 1
            scores[game.team2_name] += 1

    return scores

def rank_teams(teams: Mapping[str, int]) -> List[Ranking]:
    def get_sort_key(team):
        name, score = team
        return (-score, name)

    sorted_teams = sorted(teams.items(), key=get_sort_key)

    def get_group_key(team):
        _, score = team
        return score

    i = 1
    result = []

    for tied_teams in group_by(sorted_teams, key=get_group_key):
        for name, score in tied_teams:
            result.append(Ranking(rank=i, team=name, score=score))

        i += len(tied_teams)

    return result

## Helpers ##

T = TypeVar("T")
U = TypeVar("U")

def group_by(arr: List[T], key: Callable[[T], U]) -> List[List[T]]:
    if len(arr) == 0:
        return []

    prev = arr[0]
    buffr = [prev]
    result = []

    for elem in arr[1:]:
        if key(prev) == key(elem):
            buffr.append(elem)
        else:
            result.append(buffr)
            prev = elem
            buffr = [elem]

    result.append(buffr)
    return result
