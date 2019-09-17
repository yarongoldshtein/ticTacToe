import random

from Board import Board


class TwoPlayers:
    @staticmethod
    def game(pl_map):
        board, winner, counter = Board(), 0, 0
        board.reset_board()
        marks_map = {1: "X", 2: "O"}
        turn = random.randint(1, 2)
        while not winner:
            board.choose_place(pl_map[marks_map[turn]], pl_map)
            counter += 1
            print("Board after " + str(counter) + " move:")
            board.print_board()
            winner = board.evaluate(counter, turn)
            if winner:
                break
            turn = (turn % 2) + 1
        if winner == -1:
            return -1
        return marks_map[winner]

    @staticmethod
    def play_game(self):
        player1 = input("Player 1, Please enter your name: ")
        while player1 == "":
            player1 = input("Player 1, Please enter your valid name: ")
        player2 = input("Player 2, Please enter your name: ")
        while player2 == "" or player2 == player1:
            player2 = input("Player 2, Please enter your valid name: ")
        players_map = {"X": player1, "O": player2}
        print("\n\t" + players_map["X"] + " you are X\n\t" + players_map["O"] + " you are Y\n")
        final_winner = self.game(players_map)
        if final_winner != -1:
            print("Winner is: " + players_map[final_winner])
            return players_map[final_winner]
        else:
            print("The game ended in equality")
            return players_map["X"], players_map["O"]
