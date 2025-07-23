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
    
    
    def if_not_checke_after(self, board_after_move, turn, my_color):
        if self.check(board_after_move, my_color)[0][0] and turn == "white": #if there is check
            return False
        elif self.check(board_after_move, my_color)[1][0] and turn == "black":
            return False

        return True
    

    def pawn_moves(self, board, row, col, turn, my_color): # need to check if there is atack on king after move or before move
        posible_moves = []
        where_to_move = 1 if my_color == turn else -1
        
        if self.turn_checker(turn, board[row][col]): #check if the piece is the same color as the turn
            self.board_after_move = [list(row) for row in board]
            self.board_after_move[row - where_to_move][col] = board[row][col]
            self.board_after_move[row][col] = ""
            if len(board[row - where_to_move][col]) == 0 and self.if_not_checke_after(self.board_after_move, turn, my_color):
                posible_moves.append([row - where_to_move, col])
                
                if 0 <= row - (where_to_move * 2) <= 7:
                    self.board_after_move = [list(row) for row in board]
                    self.board_after_move[row - (where_to_move * 2)][col] = board[row][col]
                    self.board_after_move[row][col] = ""    
                    if len(board[row - (where_to_move * 2)][col]) == 0  and (row == 6 and my_color == turn) or (row == 1 and my_color != turn) and self.if_not_checke_after(self.board_after_move, turn, my_color):
                        posible_moves.append([row - (where_to_move * 2), col])
            
            if col + 1 < 8:
                self.board_after_move = [list(row) for row in board]
                self.board_after_move[row - where_to_move][col + 1] = board[row][col]
                self.board_after_move[row][col] = ""
                if len(board[row - where_to_move][col + 1]) > 0 and self.turn_checker(turn, board[row - where_to_move][col + 1]) == False and self.if_not_checke_after(self.board_after_move, turn, my_color): #check if atacked piece is different color
                    posible_moves.append([row - where_to_move, col + 1])
                    
            if col - 1 >= 0:
                self.board_after_move = [list(row) for row in board]
                self.board_after_move[row - where_to_move][col - 1] = board[row][col]
                self.board_after_move[row][col] = ""
                if col - 1 >= 0 and len(board[row - where_to_move][col - 1]) > 0 and self.turn_checker(turn, board[row - where_to_move][col - 1]) == False and self.if_not_checke_after(self.board_after_move, turn, my_color):
                    posible_moves.append([row - where_to_move, col - 1])
        else:
            posible_moves = []
                
        return posible_moves
    
       
    def rook_moves(self, board, row, col, turn, my_color): 
        posible_moves = []
        moves = [
            [(row - i, col) for i in range(1, row + 1)],
            [(row + i, col) for i in range(1, 8 - row)],
            [(row, col - i) for i in range(1, col + 1)],
            [(row, col + i) for i in range(1, 8 - col)]
            
        ]
        if self.turn_checker(turn, board[row][col]): #check if the piece is the same color as the turn
            for i in moves:
                for move in i:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        self.board_after_move = [list(row) for row in board]
                        self.board_after_move[move[0]][move[1]] = board[row][col]
                        self.board_after_move[row][col] = ""
                        
                        print(move)
                        if len(board[move[0]][move[1]]) == 0: #if the space is empty
                            if self.if_not_checke_after(self.board_after_move, turn, my_color):
                                print("brak szachu przy ruchu wiezy11")
                                posible_moves.append(move)
                            
                        elif self.turn_checker(turn, board[move[0]][move[1]]) == False: #check if the piece is different color
                            print("brak szachu przy ruchu wiezy22")
                            if self.if_not_checke_after(self.board_after_move, turn, my_color):
                                posible_moves.append(move)
                            break
                            
                        else: #if the piece is the same color
                            break
                        
        print("koniec ruchu wiezy")
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
                        self.board_after_move = [list(row) for row in board]
                        self.board_after_move[move[0]][move[1]] = board[row][col]
                        self.board_after_move[row][col] = ""
                        
                        if self.if_not_checke_after(self.board_after_move, turn, my_color):
                            posible_moves.append(move)
            
        return posible_moves
    
    
    def bishop_moves(self, board, row, col, turn, my_color):
        posible_moves = []
        moves = [
            [(row - i, col - i) for i in range(1, row + 1)],
            [(row - i, col + i) for i in range(1, row + 1)],
            [(row + i, col - i) for i in range(1, 8 - row)],
            [(row + i, col + i) for i in range(1, 8 - row)]
        ]
        if self.turn_checker(turn, board[row][col]):
            for i in moves:
                for move in i:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        self.board_after_move = [list(row) for row in board]
                        self.board_after_move[move[0]][move[1]] = board[row][col]
                        self.board_after_move[row][col] = ""
                        
                        if len(board[move[0]][move[1]]) == 0:
                            if self.if_not_checke_after(self.board_after_move, turn, my_color):
                                posible_moves.append(move)
                        elif self.turn_checker(turn, board[move[0]][move[1]]) == False:
                            if self.if_not_checke_after(self.board_after_move, turn, my_color):
                                posible_moves.append(move)
                            break
                        else:
                            break
                    else:
                        break
                
        return posible_moves
        
    
    def queen_moves(self, board, row, col, turn, my_color):
        posible_moves = []
        moves = [
            [(row - i, col) for i in range(1, row + 1)], #rook moves
            [(row + i, col) for i in range(1, 8 - row)],
            [(row, col - i) for i in range(1, col + 1)],
            [(row, col + i) for i in range(1, 8 - col)],
            [(row - i, col - i) for i in range(1, row + 1)], #bishop moves
            [(row - i, col + i) for i in range(1, row + 1)],
            [(row + i, col - i) for i in range(1, 8 - row)],
            [(row + i, col + i) for i in range(1, 8 - row)]
        ]
        
        if self.turn_checker(turn, board[row][col]):
            
            for i in moves:
                for move in i:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        self.board_after_move = [list(row) for row in board]
                        self.board_after_move[move[0]][move[1]] = board[row][col]
                        self.board_after_move[row][col] = ""
                        
                        if len(board[move[0]][move[1]]) == 0:
                            if self.if_not_checke_after(self.board_after_move, turn, my_color):
                                posible_moves.append(move)
                            
                        elif self.turn_checker(turn, board[move[0]][move[1]]) == False:
                            if self.if_not_checke_after(self.board_after_move, turn, my_color):
                                posible_moves.append(move)
                            break
                        
                        else:
                            break
                        
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
        
        if self.turn_checker(turn, board[row][col]):
            print("castling" + str(sum(len(i) for i in board[row][col+1:7])))
            
            if board[row][col] == "k":
                print("castlingw")
                if castling["white"]["king"] and castling["white"]["Rook-L"] and board[row][0] == "r" and sum(len(i) for i in board[row][1:col]) == 0: #need to add checking if ther is check
                    posible_moves.append((row, col - 2, "castling"))
                    
                if castling["white"]["king"] and castling["white"]["Rook-R"] and board[row][0] == "r" and sum(len(i) for i in board[row][col+1:7]) == 0:
                    posible_moves.append((row, col + 2, "castling"))
                    
                
            elif board[row][col] == "K":
                print("castlingb")
                if castling["black"]["king"] and castling["black"]["Rook-L"] and board[row][0] == "R" and sum(len(i) for i in board[row][1:col]) == 0:
                    posible_moves.append((row, col - 2, "castling"))
                    
                if castling["black"]["king"] and castling["black"]["Rook-R"] and board[row][0] == "R" and sum(len(i) for i in board[row][col+1:7]) == 0:
                    posible_moves.append((row, col + 2, "castling"))
        
        
        
        if self.turn_checker(turn, board[row][col]):
            for move in moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if len(board[move[0]][move[1]]) == 0 or self.turn_checker(turn, board[move[0]][move[1]]) == False:
                        self.board_after_move = [list(row) for row in board]
                        self.board_after_move[move[0]][move[1]] = board[row][col]
                        self.board_after_move[row][col] = ""
                        
                        if self.if_not_checke_after(self.board_after_move, turn, my_color):
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
        
        if len(kings[0]) == 0 or len(kings[1]) == 0: #if there is no king this if will pass that both kings are in check so move isn't posible
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
            
            where_to_move = -1 if (my_color == "black" and board[row][col] == "K") or (my_color == "white" and board[row][col] == "k") else 1
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
                            if (board[row][col] == "k" and board[move[0]][move[1]][0].isupper()) or (board[row][col] == "K" and board[move[0]][move[1]][0].islower()):
                                #print("rrook")
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
                        elif board[move[0]][move[1]][0] in ('b', 'q', 'B', "Q") :
                            if (board[row][col] == "k" and board[move[0]][move[1]][0].isupper()) or (board[row][col] == "K" and board[move[0]][move[1]][0].islower()):
                                #print("bishop")
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
                        print("knight:  ", board[row][col] == "k" and board[r][c][0].isupper(), " |  ", board[r][c], board[row][col])
                        if (board[row][col] == "k" and board[r][c].isupper()) or (board[row][col] == "K" and board[r][c][0].islower()):
                            print("knight")
                            posible_checks[king_turn][0] = True
                            posible_checks[king_turn].append((r, c)) 
                            
                    
            for i in posible_ataks_pawn:
                if 0 <= i[0] < 8 and 0 <= i[1] < 8:
                    if len(board[i[0]][i[1]]) == 0:
                        continue
                    elif board[i[0]][i[1]][0] in ('p', 'P'):
                        if (board[row][col] == "k" and board[i[0]][i[1]][0].isupper()) or (board[row][col] == "K" and board[i[0]][i[1]][0].islower()):
                            #print("pawn"+ str(i[0]+i[1]))
                            posible_checks[king_turn][0] = True
                            posible_checks[king_turn].append((i[0], i[1])) 
                    else:
                        break
                    
        print(posible_checks)
        return posible_checks
                

    def check_mate(self, board, my_color, turn, castling): #not working yet
        mate = [False, False]
        posible_moves = []
        check = self.check(board, my_color)
        
        if check[0][0] or check[1][0]:
            for color in range(2):
                for r in range(8):
                    for c in range(8):
                        if (my_color == "white" and color == 0 and board[r][c].islower()) or (my_color == "black" and color == 1 and board[r][c].isupper()):
                            if board[r][c].lower() == "p":
                                posible_moves.append(self.pawn_moves(board, r, c, turn, my_color)) 

                            elif board[r][c].lower() == "n":
                                posible_moves.append(self.knight_moves(board, r, c, turn, my_color))

                            elif board[r][c].lower() == "b":
                                posible_moves.append(self.bishop_moves(board, r, c, turn, my_color))

                            elif board[r][c].lower() == "r":
                                posible_moves.append(self.rook_moves(board, r, c, turn, my_color))

                            elif board[r][c].lower() == "q":
                                posible_moves.append(self.queen_moves(board, r, c, turn, my_color))

                            elif board[r][c].lower() == "k":
                                posible_moves.append(self.king_moves(board, r, c, turn, castling, my_color))

                if len(posible_moves) > 0:
                    mate[color] = True
        
        return mate
        
        
    def is_stalemate():
        pass
    
#made by: rokrerum
