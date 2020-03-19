import sys

from soccer_ranking import get_rankings

def main():
    if len(sys.argv) != 2:
        raise Exception("Require input file")

    file = sys.argv[1]
    lines = open(file).readlines()

    rankings = get_rankings(lines)
    for ranking in rankings:
        pts = "pt" if ranking.league_score == 1 else "pts"
        print("{}. {}, {} {}, gd: {}".format(ranking.rank, ranking.team, ranking.league_score, pts, ranking.goal_diff))

if __name__ == "__main__":
    main()
