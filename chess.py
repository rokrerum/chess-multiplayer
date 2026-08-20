class piece_moves:
    def __init__(self):
        self.board_after_move = []
        self.posible_moves = []


    def turn_checker(self, turn, piece):
        if turn == "white" and piece.islower():
            return True
        elif turn == "black" and piece.isupper():
            return True
        return False


    def if_not_checke_after(self, board, turn, my_color, move):  # this thing is creating same board after posible move to check if there is check
        row, col, row_move, col_move = move[0], move[1], move[2], move[3]
        self.board_after_move = [list(row) for row in board]
        self.board_after_move[row_move][col_move] = board[row][col]
        self.board_after_move[row][col] = ""

        if self.check(self.board_after_move, my_color)[0][0] and turn == "white":  # if there is check
            return False
        elif self.check(self.board_after_move, my_color)[1][0] and turn == "black":
            return False

        return True

    def if_king_near(self, board, row, col, turn):
        moves = [
            (row + 1, col - 1),
            (row + 1, col),
            (row + 1, col + 1),
            (row, col - 1),
            (row, col + 1),
            (row - 1, col - 1),
            (row - 1, col),
            (row - 1, col + 1)
        ]

        for move in moves:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7 and board[move[0]][move[1]].lower() == "k" and self.turn_checker(turn, board[move[0]][move[1]]) == False:
                return False
        return True


    def pawn_moves(self, board, row, col, turn, my_color, en_passant):
        posible_moves = []
        where_to_move = 1 if my_color == turn else -1

        if self.turn_checker(turn, board[row][col]):  # check if the piece is the same cpolor as the turn
            if len(board[row - where_to_move][col]) == 0 and self.if_not_checke_after(board, turn, my_color, (row, col, row - where_to_move ,col)):
                posible_moves.append([row - where_to_move, col])

                if 0 <= row - (where_to_move * 2) <= 7:
                    if len(board[row - (where_to_move * 2)][col]) == 0 and ((row == 6 and my_color == turn) or (
                            row == 1 and my_color != turn)) and self.if_not_checke_after(board, turn, my_color,(row, col, row - (where_to_move * 2),col)):

                        if (0 <= col + 1 <= 7 and board[row - (where_to_move * 2)][col + 1].lower() == "p" and
                                board[row - (where_to_move * 2)][col + 1] != board[row][col]) or \
                                (0 <= col - 1 <= 7 and board[row - (where_to_move * 2)][col - 1].lower() == "p" and
                                board[row - (where_to_move * 2)][col - 1] != board[row][col]):  # check if en passant will be posible next move
                            posible_moves.append([row - (where_to_move * 2), col, ("en_passant")])
                        else:
                            posible_moves.append([row - (where_to_move * 2), col])

                            # normal powns ataks
            if col + 1 < 8:
                if (len(board[row - where_to_move][col + 1]) > 0 and self.if_not_checke_after(board, turn, my_color,(row, col, row - where_to_move, col + 1))
                        and self.turn_checker(turn, board[row - where_to_move][col + 1]) == False):  # check if atacked piece is different color
                    posible_moves.append([row - where_to_move, col + 1])

            if col - 1 >= 0:
                if col - 1 >= 0 and len(board[row - where_to_move][col - 1]) > 0 and self.turn_checker(turn, board[
                        row - where_to_move][col - 1]) == False and self.if_not_checke_after(board, turn, my_color, (row, col, row - where_to_move, col - 1)):
                    posible_moves.append([row - where_to_move, col - 1])

            # checks if en passant is posible
            if (en_passant[0] and row == en_passant[1] and ((col + 1) == en_passant[2] and
                    board[en_passant[1] - where_to_move][col + 1] == "") and
                    self.if_not_checke_after(board, turn, my_color, (row, col, en_passant[1] - where_to_move, col + 1))):
                posible_moves.append([row - where_to_move, col + 1, "en_passant_move"])

            elif en_passant[0] and row == en_passant[1] and (
                    (col - 1) == en_passant[2] and board[en_passant[1] - where_to_move][
                col - 1] == "") and self.if_not_checke_after(board, turn, my_color,
                                                             (row, col, en_passant[1] - where_to_move, col - 1)):
                posible_moves.append([row - where_to_move, col - 1, "en_passant_move"])


        else:
            posible_moves = []

        return posible_moves


    def knight_moves(self, board, row, col, turn, my_color):
        posible_moves = []
        moves = [
            (row + 2, col + 1),
            (row + 2, col - 1),
            (row - 2, col + 1),
            (row - 2, col - 1),
            (row + 1, col + 2),
            (row + 1, col - 2),
            (row - 1, col + 2),
            (row - 1, col - 2)
        ]
        if self.turn_checker(turn, board[row][col]):
            for move in moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if len(board[move[0]][move[1]]) == 0 or self.turn_checker(turn, board[move[0]][move[1]]) == False:
                        if self.if_not_checke_after(board, turn, my_color, (row, col, move[0], move[1])):
                            posible_moves.append(move)

        return posible_moves


    def sliding_moves(self, board, row, col, turn, my_color, directions):
        posible_moves = []
        if not self.turn_checker(turn, board[row][col]):
            return posible_moves

        for dr, dc in directions:
            move = row + dr, col + dc
            while 0 <= move[0] < 8 and 0 <= move[1] < 8:
                if len(board[move[0]][move[1]]) == 0:
                    if self.if_not_checke_after(board, turn, my_color, (row, col, move[0], move[1])):
                        posible_moves.append(move)

                elif self.turn_checker(turn, board[move[0]][move[1]]) == False:
                    if self.if_not_checke_after(board, turn, my_color, (row, col, move[0], move[1])):
                        posible_moves.append(move)
                    break
                else:
                    break
                move = move[0] + dr, move[1] + dc
        return posible_moves


    def king_moves(self, board, row, col, turn, castling, my_color):
        posible_moves = []
        moves = [
            (row + 1, col - 1),
            (row + 1, col),
            (row + 1, col + 1),
            (row, col - 1),
            (row, col + 1),
            (row - 1, col - 1),
            (row - 1, col),
            (row - 1, col + 1)
        ]

        if self.turn_checker(turn, board[row][col]):  # this is for checking if castling is posible for both kings
            if board[row][col] == "k":
                if self.check(board, my_color)[0][0] == False:
                    if castling["white"]["king"] and castling["white"]["Rook-L"] and board[row][0] == "r" and sum(
                            len(i) for i in board[row][1:col]) == 0 and self.if_not_checke_after(board, turn, my_color,
                                                                                                 (row, col, row,
                                                                                                  col - 2)):
                        posible_moves.append((row, col - 2, "castling"))

                    if castling["white"]["king"] and castling["white"]["Rook-R"] and board[row][7] == "r" and sum(
                            len(i) for i in board[row][col + 1:7]) == 0 and self.if_not_checke_after(board, turn,
                                                                                                     my_color,
                                                                                                     (row, col, row,
                                                                                                      col + 2)):
                        posible_moves.append((row, col + 2, "castling"))


            elif board[row][col] == "K":
                if self.check(board, my_color)[1][0] == False:
                    if castling["black"]["king"] and castling["black"]["Rook-L"] and board[row][0] == "R" and sum(
                            len(i) for i in board[row][1:col]) == 0 and self.if_not_checke_after(board, turn, my_color,
                                                                                                 (row, col, row,
                                                                                                  col - 2)):
                        posible_moves.append((row, col - 2, "castling"))

                    if castling["black"]["king"] and castling["black"]["Rook-R"] and board[row][7] == "R" and sum(
                            len(i) for i in board[row][col + 1:7]) == 0 and self.if_not_checke_after(board, turn,
                                                                                                     my_color,
                                                                                                     (row, col, row,
                                                                                                      col + 2)):
                        posible_moves.append((row, col + 2, "castling"))

        if self.turn_checker(turn, board[row][col]):  # this adds posible normal king moves
            for move in moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if len(board[move[0]][move[1]]) == 0 or self.turn_checker(turn, board[move[0]][move[1]]) == False:
                        if self.if_not_checke_after(board, turn, my_color,
                                                    (row, col, move[0], move[1])) and self.if_king_near(board, move[0],
                                                                                                        move[1], turn):
                            posible_moves.append(move)

        return posible_moves

    def check(self, board, my_color):
        kings = [[], []]
        for i in range(8):
            for j in range(8):
                if board[i][j] == "k":
                    kings[0] = [i, j]
                elif board[i][j] == "K":
                    kings[1] = [i, j]

        if len(kings[0]) == 0 or len(kings[
                                         1]) == 0:  # if there is no king this if will pass that both kings are in check so move isn't posible
            return [[True], [True]]

        posible_checks = [[False, (kings[0][0], kings[0][1])], [False, (kings[1][0], kings[1][1])]]

        for king_turn in range(2):
            row = kings[king_turn][0]
            col = kings[king_turn][1]

            posible_ataks_rook = [
                [(row - i, col) for i in range(1, row + 1)],
                [(row + i, col) for i in range(1, 8 - row)],
                [(row, col - i) for i in range(1, col + 1)],
                [(row, col + i) for i in range(1, 8 - col)]
            ]
            posible_ataks_bishop = [
                [(row - i, col - i) for i in range(1, row + 1)],
                [(row - i, col + i) for i in range(1, row + 1)],
                [(row + i, col - i) for i in range(1, 8 - row)],
                [(row + i, col + i) for i in range(1, 8 - row)]
            ]
            posible_ataks_knight = [
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row + 1, col + 2),
                (row + 1, col - 2),
                (row - 1, col + 2),
                (row - 1, col - 2)
            ]

            where_to_move = -1 if (my_color == "black" and board[row][col] == "K") or (
                        my_color == "white" and board[row][col] == "k") else 1
            posible_ataks_pawn = [
                (row + where_to_move, col - 1),
                (row + where_to_move, col + 1)
            ]

            for i in posible_ataks_rook:
                for move in i:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        if len(board[move[0]][move[1]]) == 0:
                            continue
                        elif board[move[0]][move[1]][0] in ('r', 'q', 'R', 'Q'):
                            if (board[row][col] == "k" and board[move[0]][move[1]][0].isupper()) or (
                                    board[row][col] == "K" and board[move[0]][move[1]][0].islower()):
                                # print("rrook")
                                posible_checks[king_turn][0] = True
                                posible_checks[king_turn].append((move[0], move[1]))
                            else:
                                break
                        else:
                            break
                    else:
                        break

            for i in posible_ataks_bishop:
                for move in i:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        if len(board[move[0]][move[1]]) == 0:
                            continue
                        elif board[move[0]][move[1]][0] in ('b', 'q', 'B', "Q"):
                            if (board[row][col] == "k" and board[move[0]][move[1]][0].isupper()) or (
                                    board[row][col] == "K" and board[move[0]][move[1]][0].islower()):
                                # print("bishop")
                                posible_checks[king_turn][0] = True
                                posible_checks[king_turn].append((move[0], move[1]))
                            else:
                                break
                        else:
                            break
                    else:
                        break

            for r, c in posible_ataks_knight:
                if 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] in ('n', 'N'):
                        if (board[row][col] == "k" and board[r][c].isupper()) or (
                                board[row][col] == "K" and board[r][c][0].islower()):
                            # print("knight")
                            posible_checks[king_turn][0] = True
                            posible_checks[king_turn].append((r, c))

            for i in posible_ataks_pawn:
                if 0 <= i[0] < 8 and 0 <= i[1] < 8:
                    if len(board[i[0]][i[1]]) == 0:
                        continue
                    elif board[i[0]][i[1]][0] in ('p', 'P'):
                        if (board[row][col] == "k" and board[i[0]][i[1]][0].isupper()) or (
                                board[row][col] == "K" and board[i[0]][i[1]][0].islower()):
                            # print("pawn"+ str(i[0]+i[1]))
                            posible_checks[king_turn][0] = True
                            posible_checks[king_turn].append((i[0], i[1]))
                    else:
                        break

        return posible_checks

    def check_mate(self, board, my_color, castling, en_passant):  # not working yet
        mate = [False, False]
        posible_moves = []
        check = self.check(board, my_color)
        color = ["white", "black"]

        BISHOP_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        ROOK_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        QUEEN_DIRS = ROOK_DIRS + BISHOP_DIRS

        for color_turn in range(2):
            if check[color_turn][0]:
                for r in range(8):
                    for c in range(8):
                        if (color_turn == 0 and board[r][c].islower()) or (color_turn == 1 and board[r][c].isupper()):
                            if board[r][c].lower() == "p":
                                posible_moves.extend(
                                    self.pawn_moves(board, r, c, color[color_turn], my_color, en_passant))

                            elif board[r][c].lower() == "n":
                                posible_moves.extend(self.knight_moves(board, r, c, color[color_turn], my_color))

                            elif board[r][c].lower() == "b":
                                posible_moves.extend(self.sliding_moves(board, r, c, color[color_turn], my_color, BISHOP_DIRS))

                            elif board[r][c].lower() == "r":
                                posible_moves.extend(self.sliding_moves(board, r, c, color[color_turn], my_color, ROOK_DIRS))

                            elif board[r][c].lower() == "q":
                                posible_moves.extend(self.sliding_moves(board, r, c, color[color_turn], my_color, QUEEN_DIRS))

                            elif board[r][c].lower() == "k":
                                posible_moves.extend(
                                    self.king_moves(board, r, c, color[color_turn], castling, my_color))

                moves = sum(len(i) for i in posible_moves) / 2
                if moves == 0:
                    mate[color_turn] = True
                posible_moves = []

        return mate

    def is_stalemate(self, board, my_color, castling, turn, en_passant):
        stalemate = [False, False]
        check = self.check(board, my_color)
        color = ["white", "black"]
        turn = "white" if turn == "black" else "black"

        BISHOP_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        ROOK_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        QUEEN_DIRS = ROOK_DIRS + BISHOP_DIRS

        for color_turn in range(2):
            if check[color_turn][0] == False:
                posible_moves = []
                for r in range(8):
                    for c in range(8):
                        if (color_turn == 0 and board[r][c].islower() and turn == "white") or (
                                color_turn == 1 and board[r][c].isupper() and turn == "black"):
                            if board[r][c].lower() == "p":
                                posible_moves.extend(
                                    self.pawn_moves(board, r, c, color[color_turn], my_color, en_passant))

                            elif board[r][c].lower() == "n":
                                posible_moves.extend(self.knight_moves(board, r, c, color[color_turn], my_color))

                            elif board[r][c].lower() == "b":
                                posible_moves.extend(self.sliding_moves(board, r, c, color[color_turn], my_color, BISHOP_DIRS))

                            elif board[r][c].lower() == "r":
                                posible_moves.extend(self.sliding_moves(board, r, c, color[color_turn], my_color, ROOK_DIRS))

                            elif board[r][c].lower() == "q":
                                posible_moves.extend(self.sliding_moves(board, r, c, color[color_turn], my_color, QUEEN_DIRS))

                            elif board[r][c].lower() == "k":
                                posible_moves.extend(
                                    self.king_moves(board, r, c, color[color_turn], castling, my_color))

                moves = sum(len(i) for i in posible_moves)
                if moves == 0 and ((color_turn == 0 and turn == "white") or (color_turn == 1 and turn == "black")):
                    stalemate[color_turn] = True

        return stalemate

# made by: rokrerum