from time import sleep
from inputdata import start, rounds, G
import random
import os, sys

N = len(start)
leaderboard = []


def main():
    os.system('echo "\033]0;%s\007"' % "Fantasy Football v1.0.0")
    cls()
    header = "\033[1mFantasy Football\033[0m v1.0.0"
    print(header)

    try:
        iter = int(sys.argv[1])
    except:
        iter = 100000

    stats = {}
    for team in start:
        stats[team[0]] = [0]*N

    try:
        from progress.bar import IncrementalBar
        bar = IncrementalBar("Computing...", max=iter)
    except:
        bar = None

    try:
        if not bar: print("Computing...")

        for _ in range(iter):
            board = [team[:] for team in start]
            updateBoard(board)
            updateStats(stats, board, iter)
            if bar: bar.next()

        if bar: bar.finish()
        cls()
        print(header)
        if iter != 1:
            print(f"Simulation completed ({iter} iterations)\n")
            print(f"{''.ljust(20)}{''.join([str(i + 1).rjust(7) for i in range(N)])}")

            for key in stats:
                stats[key] = [round(x / iter * 100, 2) for x in stats[key]]
                print(f"{key.ljust(20)}{''.join([str(x).rjust(7) for x in stats[key]])}")

        else:
            print(f"Single simulation completed\n")
            i = 1
            for team in leaderboard:
                print(i, team[0].ljust(20), str(team[1]).ljust(7), str(team[2]).ljust(7))
                i += 1

        print("\n\033[33mPress Ctrl-C to quit\033[0m")   

        while 1:
            sleep(1)

    except KeyboardInterrupt:
        cls()
        sys.exit()


def updateStats(stats, board: list, iter: int):
    for i in range(N):
        best = max(board, key=lambda x: (x[1], x[2]))
        stats[best[0]][i] += 1
        board.remove(best)
        if iter == 1:
            leaderboard.append(best)


def updateBoard(board):
    for i in range(G):
        for round in rounds[i % (N - 1)]:
            board[round[0]], board[round[1]] = game(board[round[0]], board[round[1]])
    return board


def game(team1, team2):
    points1 = int(random.gauss(141, 15)) / 2
    points2 = int(random.gauss(141, 15)) / 2
    team1[2] += points1
    team2[2] += points2

    goals1, goals2 = 0, 0

    while points1 >= 66:
        goals1 += 1
        points1 -= 5
    
    while points2 >= 66:
        goals2 += 1
        points2 -= 5

    if goals1 > goals2:
        team1[1] += 3
    elif goals2 > goals1:
        team2[1] += 3
    else:
        team1[1] += 1
        team2[1] += 1

    return team1, team2


def cls():
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    main()
