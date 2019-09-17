class Board:
    board = [["", "", ""],
             ["", "", ""],
             ["", "", ""]]

    def reset_board(self):
        self.board = [["", "", ""],
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
        if pl_map:
            for mark, name in pl_map.items():
                if name == player:
                    self.board[current_loc[0]][current_loc[1]] = mark
        else:
            self.board[current_loc[0]][current_loc[1]] = "X"

    def choose_and_check_place(self, player):
        selection = input(player + " Enter your selection: ").strip()
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
        return num.isdigit() and int(num) in range(1, 10) and self.convert_number_to_position(num) in self.possibilities()

    def transpose_board(self):
        """transposing the board for easier review of the columns"""
        transpose_board = []
        for i in range(len(self.board[0])):
            transpose_board.append([x[i] for x in self.board])
        return transpose_board

    def check_win(self, player):
        transpose_board = self.transpose_board()
        return self.check_for_line(player, self.board) or self.check_for_line(player, transpose_board) \
               or self.diag1_win(player) or self.diag2_win(player)

    def check_for_line(self, player, board):
        for i in range(len(board)):
            if all(mark == player for mark in board[i]):
                return True
        return False

    def diag1_win(self, player):
        diag = []
        for x in range(len(self.board)):
            diag.append(self.board[x][x])
        if all(mark == player for mark in diag):
            return True
        return False

    def diag2_win(self, player):
        diag = [self.board[0][2], self.board[1][1], self.board[2][0]]
        if all(mark == player for mark in diag):
            return True
        return False

    def evaluate(self, counter, player):
        winner = 0
        if player == 1:
            mark = "X"
        else:
            mark = "O"
        if self.check_win(mark):
            winner = player
        if not winner and counter == 9:
            winner = -1
        return winner

    def player_turn(self):
        self.choose_place("", None)

    def computer_turn(self, counter):
        self.computer_choose_place(counter)

    def computer_choose_place(self, counter):
        com_mark = "O"
        play_mark = "X"
        if counter < 3 and self.board[1][1] == "":
            self.board[1][1] = com_mark
        else:
            one_away = self.is_one_away(com_mark)
            if one_away:
                self.board[one_away[0]][one_away[1]] = com_mark
                return
            rival_one_away = self.is_one_away(play_mark)
            if rival_one_away:
                self.board[rival_one_away[0]][rival_one_away[1]] = com_mark
                return
            fork = self.fork(com_mark)
            if fork:
                self.board[fork[0]][fork[1]] = com_mark
                return
            rival_fork = self.fork(play_mark)
            if rival_fork:
                self.board[rival_fork[0]][rival_fork[1]] = com_mark
                return
            opposite_corner = self.opposite_corner(play_mark)
            if opposite_corner:
                self.board[opposite_corner[0]][opposite_corner[1]] = com_mark
                return
            empty_corner = self.empty_corner()
            if empty_corner:
                self.board[empty_corner[0]][empty_corner[1]] = com_mark
                return
            empty_side = self.empty_side()
            if empty_side:
                self.board[empty_side[0]][empty_side[1]] = com_mark
                return
            # Should never get to here
            raise ValueError("the computer didn't find a move to do!")

    def is_one_away(self, mark):
        row = self.is_line_one_away(mark, self.board)
        if row:
            return row
        col = self.is_line_one_away(mark, self.transpose_board())
        if col:
            return col[1], col[0]
        diag1 = self.is_diag1_one_away(mark)
        if diag1:
            return diag1
        diag2 = self.is_diag2_one_away(mark)
        if diag2:
            return diag2

    def is_line_one_away(self, mark, board):
        for i in range(len(board)):
            line = list(filter(lambda x: x != "", board[i]))
            if len(line) == 2 and all(p == mark for p in line):
                for j in range(len(board[i])):
                    if board[i][j] == "":
                        return i, j

    def is_diag1_one_away(self, mark):
        diag = []
        for i in range(len(self.board)):
            diag.append(self.board[i][i])
        diag_marks = list(filter(lambda x: x != "", diag))
        if len(diag_marks) == 2 and all(p == mark for p in diag_marks):
            for i in range(len(self.board)):
                if self.board[i][i] == "":
                    return i, i

    def is_diag2_one_away(self, mark):
        diag = [self.board[0][2], self.board[1][1], self.board[2][0]]
        diag_marks = list(filter(lambda x: x != "", diag))
        if len(diag_marks) == 2 and all(p == mark for p in diag_marks):
            for i in range(len(diag)):
                if diag[i] == "":
                    if not i:
                        return 0, 2
                    elif i == 1:
                        return 1, 1
                    return 2, 0

    def fork(self, mark):
        list_rows_op, list_columns_op, diag1 = self.find_rows_cols_to_fork(mark)
        diag2 = [self.board[0][2], self.board[1][1], self.board[2][0]]
        list_diags_op = self.find_diags_to_fork(mark, diag1, diag2)

        # from here it is check if there is possibilities to fork
        cross_row_diag = self.cross_row_diag(list_rows_op, list_diags_op)
        if cross_row_diag:
            return cross_row_diag
        cross_col_diag = self.cross_col_diag(list_columns_op, list_diags_op)
        if cross_col_diag:
            return cross_col_diag
        cross_row_col = self.cross_row_col(list_rows_op, list_columns_op)
        if cross_row_col:
            return cross_row_col

    def cross_row_col(self, rows, cols):
        for i in range(len(rows)):
            for j in range(len(cols)):
                if self.board[rows[i]][cols[j]] == "":
                    return rows[i], cols[j]

    def cross_row_diag(self, rows, diags):
        for i in range(len(rows)):
            for j in range(len(diags)):
                if diags[j] == 1:
                    if self.board[rows[i]][rows[i]] == "":
                        return rows[i], rows[i]
                else:
                    if self.board[rows[i]][2 - rows[i]] == "":
                        return rows[i], 2 - rows[i]

    def cross_col_diag(self, cols, diags):
        for i in range(len(cols)):
            for j in range(len(diags)):
                if diags[j] == 1:
                    if self.board[cols[i]][cols[i]] == "":
                        return cols[i], cols[i]
                else:
                    if self.board[2 - cols[i]][cols[i]] == "":
                        return 2 - cols[i], cols[i]

    def find_rows_cols_to_fork(self, mark):
        """Returns the rows and columns that are possible for fork and by the way returns diagonal number 1"""
        transpose_board = self.transpose_board()
        rows = []
        cols = []
        diag1 = []
        for i in range(len(self.board)):
            if len(list(filter(lambda x: x == "", self.board[i]))) == 2 and mark in self.board[i]:
                rows.append(i)
            if len(list(filter(lambda x: x == "", transpose_board[i]))) == 2 and mark in self.board[i]:
                cols.append(i)
            diag1.append(self.board[i][i])
        return rows, cols, diag1

    def find_diags_to_fork(self, mark, d1, d2):
        diags = []
        if len(list(filter(lambda x: x == "", d1))) == 2 and mark in d1:
            diags.append(1)
        if len(list(filter(lambda x: x == "", d2))) == 2 and mark in d2:
            diags.append(2)
        return diags

    def opposite_corner(self, opposite_mark):
        corners = (1, 3, 7, 9)
        for i in corners:
            land = self.convert_number_to_position(i)
            if i + 2 in corners:
                opposite_land = self.convert_number_to_position(i + 2)
            else:
                opposite_land = self.convert_number_to_position(i - 2)
            if self.board[land[0]][land[1]] == opposite_mark:
                if self.board[opposite_land[0]][opposite_land[1]] == "":
                    return opposite_land[0], opposite_land[1]

    def empty_corner(self):
        for i in (1, 3, 7, 9):
            corner = self.convert_number_to_position(i)
            if self.board[corner[0]][corner[1]] == "":
                return corner

    def empty_side(self):
        for i in range(2, 10, 2):
            side = self.convert_number_to_position(i)
            if self.board[side[0]][side[1]] == "":
                return side
