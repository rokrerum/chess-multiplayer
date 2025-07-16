class piece_moves:
    global posible_moves, turn_checker
    
    def turn_checker(turn, piece):
        print(turn)
        if turn == "white" and piece.islower():
            return True

        elif turn == "black" and piece.isupper():
            return True
        
        return False
        
    
    def pawn_moves(board, row, col, turn, my_color): #pawns aren't working for white
        posible_moves = []
        where_to_move = 1 if my_color == turn else -1
        
        if turn_checker(turn, board[row][col]): #check if the piece is the same color as the turn
            if row == 6 and my_color == turn or row == 1 and my_color != turn:
                if len(board[row - where_to_move][col]) == 0:
                    posible_moves.append([row - where_to_move, col])
                    
                    if len(board[row - (where_to_move * 2)][col]) == 0:
                        posible_moves.append([row - (where_to_move * 2), col])

            else:
                if len(board[row - where_to_move][col]) <= 0:
                    posible_moves.append([row - where_to_move, col])
            
            if col + 1 < 8 and len(board[row - where_to_move][col + 1]) > 0 and turn_checker(turn, board[row - where_to_move][col + 1]) == False:
                posible_moves.append([row - where_to_move, col + 1])
            
            if col - 1 >= 0 and len(board[row - where_to_move][col - 1]) > 0 and turn_checker(turn, board[row - where_to_move][col - 1]) == False:
                posible_moves.append([row - where_to_move, col - 1])
        
        else:
            posible_moves = []
                
        return posible_moves
    
        
    def rook_moves(board, row, col, turn): 
        posible_moves = []
        moves = [
            [(row - i, col) for i in range(1, row + 1)],
            [(row + i, col) for i in range(1, 8 - row)],
            [(row, col - i) for i in range(1, col + 1)],
            [(row, col + i) for i in range(1, 8 - col)]
            
        ]
        if turn_checker(turn, board[row][col]): #check if the piece is the same color as the turn
            for i in moves:
                for move in i:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        if len(board[move[0]][move[1]]) == 0:
                            posible_moves.append(move)
                            
                        elif turn_checker(turn, board[move[0]][move[1]]) == False: #check if the piece is different color
                            posible_moves.append(move)
                            break
                        
                        else:
                            break

        return posible_moves
    
    
    def knight_moves(board, row, col, turn):
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
        if turn_checker(turn, board[row][col]):
            for move in moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if len(board[move[0]][move[1]]) == 0 or turn_checker(turn, board[move[0]][move[1]]) == False:
                        posible_moves.append(move)
            
        return posible_moves
    
    
    def bishop_moves(board, row, col, turn):
        posible_moves = []
        moves = [
            [(row - i, col - i) for i in range(1, row + 1)],
            [(row - i, col + i) for i in range(1, row + 1)],
            [(row + i, col - i) for i in range(1, 8 - row)],
            [(row + i, col + i) for i in range(1, 8 - row)]
        ]
        if turn_checker(turn, board[row][col]):
            for i in moves:
                for move in i:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        if len(board[move[0]][move[1]]) == 0:
                            posible_moves.append(move)
                        elif turn_checker(turn, board[move[0]][move[1]]) == False:
                            posible_moves.append(move)
                            break
                        else:
                            break
                    else:
                        break
                
        return posible_moves
        
    
    def queen_moves(board, row, col, turn):
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
        
        if turn_checker(turn, board[row][col]):
            
            for i in moves:
                for move in i:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        if len(board[move[0]][move[1]]) == 0:
                            posible_moves.append(move)
                            
                        elif turn_checker(turn, board[move[0]][move[1]]) == False:
                            posible_moves.append(move)
                            break
                        
                        else:
                            break
                        
        return posible_moves
    
    
    def king_moves(board, row, col, turn):
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
        
        if turn_checker(turn, board[row][col]):
            for move in moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if len(board[move[0]][move[1]]) == 0 or turn_checker(turn, board[move[0]][move[1]]) == False:
                        posible_moves.append(move)
    
        return posible_moves
    
    
    def check(board, turn, my_color): #not working correctlyd
        kings = []
        for i in range(8):
            for j in range(8):
                if board[i][j] in ("K", "k"):
                    kings.append((i, j))

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
                                print("rrook")
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
                                print("bishop")
                                posible_checks[king_turn][0] = True
                                posible_checks[king_turn].append((move[0], move[1])) 
                            else:
                                break
                        else:
                            break
                    else:
                        break
                    
                    
            for i in posible_ataks_knight:
                if 0 <= i[0] < 8 and 0 <= i[1] < 8:
                    if len(board[i[0]][i[1]]) == 0:
                        continue
                    elif board[i[0]][i[1]] in ('n', 'N'):
                        if (board[row][col] == "k" and board[i[0]][i[1]][0].isupper()) or (board[row][col] == "K" and board[i[0]][i[1]][0].islower()):
                            print("knight")
                            posible_checks[king_turn][0] = True
                            posible_checks[king_turn].append((i[0], i[1])) 

                    
            for i in posible_ataks_pawn:
                if 0 <= i[0] < 8 and 0 <= i[1] < 8:
                    if len(board[i[0]][i[1]]) == 0:
                        continue
                    elif board[i[0]][i[1]][0] in ('p', 'P'):
                        if (board[row][col] == "k" and board[i[0]][i[1]][0].isupper()) or (board[row][col] == "K" and board[i[0]][i[1]][0].islower()):
                            print("pawn"+ str(i[0]+i[1]))
                            posible_checks[king_turn][0] = True
                            posible_checks[king_turn].append((i[0], i[1])) 
                    else:
                        break
                    
        print(posible_checks)
        return posible_checks
                

    def check_mate(self, board, row, col): #NOT WORKING
        posible_moves = []
        posible_moves.extend(self.pawn_moves(board, row, col))
        posible_moves.extend(self.rook_moves(board, row, col))
        posible_moves.extend(self.bishop_moves(board, row, col))
        posible_moves.extend(self.knight_moves(board, row, col))
        posible_moves.extend(self.queen_moves(board, row, col))
        posible_moves.extend(self.king_moves(board, row, col))

        if len(posible_moves) == 0:
            return True
        else:
            return False
        
        
    def is_stalemate():
        pass
