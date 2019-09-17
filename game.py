import collections
import shelve
import sys

from TicTacToe2players import TwoPlayers
from TicTacTowVsComputer import OnePlayers


def board_example():
    print(str([1, 2, 3]) + "\n" + str([4, 5, 6]) + "\n" + str([7, 8, 9]) + "\n")


play = True


def show_high_scores():
    file = open("high_scores.txt", "r")
    contents = file.read()
    if contents != "":
        print(contents)


def find_the_biggest(numbers):
    biggest = -1
    index = -1
    for j in range(len(numbers)):
        if numbers[j] > biggest:
            biggest = numbers[j]
            index = j
    return index


def write_points(contents, number, name):
    name = name.replace(" ", "_")
    names = []
    scores = []
    end_scores = ""
    if contents != "":
        lines = contents.split("\n")
        for j in range(len(lines)):
            line = lines[j].split(" ")
            names.append(line[0])
            scores.append(int(line[1]))
        if name in names:
            for j in range(len(names)):
                if names[j] == name:
                    scores[j] += number
                    break
        else:
            names.append(name)
            scores.append(number)
        for j in range(len(names)):
            index = find_the_biggest(scores)
            if index != -1:
                end_scores += names[index] + " " + str(scores[index]) + "\n"
                scores[index] = -1
        end_scores = end_scores[:-1]
    else:
        end_scores = name + " " + str(number)
    return end_scores


def give_points(name):
    file = open("high_scores.txt", "r")
    contents = file.read()
    to_write = ""
    if type(name) == tuple:
        if name[1] != "com":
            to_write = write_points(contents, 1, name[0])
            to_write = write_points(to_write, 1, name[1])
        else:
            to_write = write_points(contents, 1, name[0])
    elif type(name) == str:
        to_write = write_points(contents, 2, name)
    file.close()
    file = open("high_scores.txt", "w")
    file.write(to_write)
    file.close()


while play:
    play_or_show = input("Do you wants to:\n "
                         "1. Play a game. \n"
                         "2. Show high scores. ")
    winner = None
    if "play a game" in play_or_show.lower() or play_or_show == "1":
        board_example()
        players = input("How many players?")
        if players == "1":
            winner = OnePlayers.play_game(OnePlayers)
        elif players == "2":
            winner = TwoPlayers.play_game(TwoPlayers)
    elif "Show high scores" in play_or_show or play_or_show == "2":
        show_high_scores()
    else:
        print("Bad input!")
    if winner is not None:
        give_points(winner)

    for i in range(3):
        to_continue = input("Do you wants to Exit? ")
        if to_continue.lower() == "yes" or to_continue.lower() == "y":
            play = False
            print("Thank you and goodbye")
            sys.exit()
        elif to_continue.lower() == "no" or to_continue.lower() == "n":
            print("Lets play again\n\n\n")
            break
        else:
            print("Bad input!\n"
                  "Do you wants to Exit? "
                  "yes(y) or no(n)? ")
