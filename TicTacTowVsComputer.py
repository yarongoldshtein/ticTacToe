import random

from Board import Board


class OnePlayers:
    @staticmethod
    def game():
        board, winner, counter = Board(), 0, 1
        board.reset_board()
        turn = random.randint(0, 1)
        if turn:
            print("You start the game\n")
        else:
            print("The computer starts the game\n")
        while not winner:
            if turn:
                board.player_turn()
            else:
                board.computer_turn(counter)
            print("Board after " + str(counter) + " move:")
            board.print_board()
            winner = board.evaluate(counter, 2 - turn)
            turn = (turn + 1) % 2
            counter += 1
        return winner

    @staticmethod
    def play_game(self):
        player = input("Please enter your name: ")
        while player == "":
            player = input("Please enter your valid name: ")
        print("\n\t" + player + " you are X\n")
        final_winner = self.game()
        if final_winner == -1:
            print("The game ended in a tie")
            return player , "com"
        elif final_winner == 1:
            print("You win!")
            return player
        else:
            print("You lose!")
