import sys

from soccer_ranking import get_rankings

def main():
    if len(sys.argv) != 2:
        raise Exception("Require input file")

    file = sys.argv[1]
    lines = open(file).readlines()

    rankings = get_rankings(lines)
    for ranking in rankings:
        pts = "pt" if ranking.score == 1 else "pts"
        print("{}. {}, {} {}".format(ranking.rank, ranking.team, ranking.score, pts))

if __name__ == "__main__":
    main()
