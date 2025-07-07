class piece_moves:
    global posible_moves
    
    def pawn_moves(board, row, col):
        posible_moves = []
        if board[row][col][0] == "P":
            if row == 6:
                if len(board[row - 1][col]) == 0:
                    posible_moves.append([row - 1, col])
                    
                    if len(board[row - 2][col]) == 0:
                        posible_moves.append([row - 2, col])

            else:
                if len(board[row - 1][col]) <= 0:
                    posible_moves.append([row - 1, col])
            
            if col + 1 < 8 and len(board[row - 1][col + 1]) > 0 and board[row - 1][col + 1][0].lower() == board[row - 1][col + 1][0]:
                posible_moves.append([row - 1, col + 1])
            
            if col - 1 < 8 and len(board[row - 1][col - 1]) > 0 and board[row - 1][col - 1][0].lower() == board[row - 1][col - 1][0]:
                posible_moves.append([row - 1, col - 1])
        
        else:
            posible_moves = []
                
        return posible_moves
    
        
    def rook_moves(board, row, col): 
        posible_moves = []
        moves = [
            [(row - i, col) for i in range(1, row + 1)],
            [(row + i, col) for i in range(1, 8 - row)],
            [(row, col - i) for i in range(1, col + 1)],
            [(row, col + i) for i in range(1, 8 - col)]
            
        ]
        if board[row][col][0] == "R":
            for i in moves:
                for move in i:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        if len(board[move[0]][move[1]]) == 0:
                            posible_moves.append(move)
                            
                        elif board[move[0]][move[1]][0].islower():
                            posible_moves.append(move)
                            break
                        
                        else:
                            break

        return posible_moves
    
    
    def knight_moves(board, row, col):
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
        if board[row][col][0] == "N":
            for move in moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if len(board[move[0]][move[1]]) == 0 or board[move[0]][move[1]][0].islower():
                        posible_moves.append(move)
            
        return posible_moves
    
    
    def bishop_moves(board, row, col):
        posible_moves = []
        moves = [
            [(row - i, col - i) for i in range(1, row + 1)],
            [(row - i, col + i) for i in range(1, row + 1)],
            [(row + i, col - i) for i in range(1, 8 - row)],
            [(row + i, col + i) for i in range(1, 8 - row)]
        ]
        if(board[row][col][0] == "B"):
            for i in moves:
                for move in i:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        if len(board[move[0]][move[1]]) == 0:
                            posible_moves.append(move)
                        elif board[move[0]][move[1]][0].islower():
                            posible_moves.append(move)
                            break
                        else:
                            break
                    else:
                        break
                
        return posible_moves
        
    
    def queen_moves(board, row, col):
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
        
        if board[row][col][0] == "Q":
            
            for i in moves:
                for move in i:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        if len(board[move[0]][move[1]]) == 0:
                            posible_moves.append(move)
                            
                        elif board[move[0]][move[1]][0].islower():
                            posible_moves.append(move)
                            break
                        
                        else:
                            break
                        
        return posible_moves
    
    
    def king_moves(board, row, col):
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
        
        if board[row][col][0] == "K":
            for move in moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if len(board[move[0]][move[1]]) == 0 or board[move[0]][move[1]][0].islower():
                        posible_moves.append(move)
    
        return posible_moves
    
    
    def check(board):
        for i in range(8):
            for j in range(8):
                if board[i][j] == "K":
                    row = i
                    col = j
                    break
        
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
        posible_ataks_pawn = [
            (row + 1, col - 1),
            (row + 1, col + 1)
        ]
        

        for i in posible_ataks_rook:
            for move in i:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if len(board[move[0]][move[1]]) == 0:
                        continue
                    elif board[move[0]][move[1]][0].islower() and board[move[0]][move[1]][0] == "r" or board[move[0]][move[1]][0] == "q":
                        print("rrook")
                        return True
                    else:
                        break
                else:
                    break
                
        for i in posible_ataks_bishop:
            for move in i:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if len(board[move[0]][move[1]]) == 0:
                        continue
                    elif board[move[0]][move[1]][0].islower() and board[move[0]][move[1]][0] == "b" or board[move[0]][move[1]][0] == "q":
                        print("bishop")
                        return True
                    else:
                        break
                else:
                    break
                
        for i in posible_ataks_knight:
            if 0 <= i[0] < 8 and 0 <= i[1] < 8:
                if len(board[i[0]][i[1]]) == 0:
                    continue
                elif board[i[0]][i[1]][0].islower() and board[i[0]][i[1]][0] == "n":
                    print("knight")
                    return True
                else:
                    break
                
        for i in posible_ataks_pawn:
            if 0 <= i[0] < 8 and 0 <= i[1] < 8:
                if len(board[i[0]][i[1]]) == 0:
                    continue
                elif board[i[0]][i[1]][0].islower() and board[i[0]][i[1]][0] == "p":
                    print("pawn")
                    return True
                else:
                    break
                
        return False
                

    def check_mate(self, board, row, col):
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
            

        
    
