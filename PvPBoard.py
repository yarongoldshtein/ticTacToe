class PvPBoard:
    board = [["", "", ""],
             ["", "", ""],
             ["", "", ""]]

    def print_board(self):
        for i in range(len(self.board)):
            print(self.board[i])
        print("--")

    def possibilities(self):
        pos = []
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == "":
                    pos.append((row, col))
        return pos

    def choose_place(self, player, pl_map):
        current_loc = self.choose_and_check_place(player)
        for mark, name in pl_map.items():
            if name == player:
                self.board[current_loc[0]][current_loc[1]] = mark

    def choose_and_check_place(self, player):
        selection = input(player + ", enter your selection: ").strip()
        while not self.is_number_valid(selection):
            print("Invalid input, please enter a between 1 and 9 that empty! \n")
            selection = input("Enter your selection: ").strip()
        return self.convert_number_to_position(selection)

    def convert_number_to_position(self, num):
        i, j = 0, -1
        for k in range(int(num)):
            j += 1
            if j > 2:
                i += 1
                j = 0
        return i, j

    def is_number_valid(self, num):
        return num.isdigit() and int(num) in range(1, 10) and self.convert_number_to_position(
            num) in self.possibilities()

    def transpose_board(self):
        transpose_board = []
        for i in range(len(self.board[0])):
            transpose_board.append([x[i] for x in self.board])
        return transpose_board

    def check_win(self, player):
        transpose_board = self.transpose_board()
        return self.check_for_line(player, self.board) or self.check_for_line(player, transpose_board) \
            or self.diag_win(player, self.board) or self.diag_win(player, transpose_board)

    def check_for_line(self, player, board):
        for i in range(len(board)):
            if all(mark == player for mark in board[i]):
                return True
        return False

    def diag_win(self, player, board):
        diag = []
        for x in range(len(board)):
            diag.append(board[x][x])
        if all(mark == player for mark in diag):
            return True
        return False

    def evaluate(self, counter, player):
        winner = 0
        if self.check_win(player):
            winner = player
        if not winner and counter == 9:
            winner = -1
        return winner
