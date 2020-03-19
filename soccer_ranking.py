from collections import defaultdict
from typing import Callable, List, Mapping, NamedTuple, TypeVar

class Ranking(NamedTuple):
    rank: int
    team: str
    league_score: int
    goal_diff: int

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

class Score:
    def __init__(self, league_score=0, goal_diff=0):
        self.league_score = league_score
        self.goal_diff = goal_diff

    def __repr__(self):
        return "Score(league_score={}, goal_diff={})".format(self.league_score, self.goal_diff)

    def __eq__(self, other):
        return self.league_score == other.league_score and self.goal_diff == other.goal_diff

def score_teams(games: List[Game]) -> Mapping[str, Score]:
    scores = defaultdict(Score)

    for game in games:
        team1 = scores[game.team1_name]
        team2 = scores[game.team2_name]

        goal_diff = game.team1_score - game.team2_score
        team1.goal_diff += goal_diff
        team2.goal_diff -= goal_diff

        if goal_diff > 0:
            team1.league_score += 3
            team2.league_score += 0
        elif goal_diff < 0:
            team1.league_score += 0
            team2.league_score += 3
        else:
            team1.league_score += 1
            team2.league_score += 1

    return scores

def rank_teams(teams: Mapping[str, Score]) -> List[Ranking]:
    def get_sort_key(team):
        name, score = team
        return (-score.league_score, -score.goal_diff, name)

    sorted_teams = sorted(teams.items(), key=get_sort_key)

    def get_group_key(team):
        _, score = team
        return score

    i = 1
    result = []

    for tied_teams in group_by(sorted_teams, key=get_group_key):
        for name, score in tied_teams:
            result.append(Ranking(rank=i, team=name, league_score=score.league_score, goal_diff=score.goal_diff))

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
