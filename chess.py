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
    
    
    def chec(self, board, row, col): #not working
        posible_ataks = [
            [(row - i, col) for i in range(1, row + 1)], #rook moves
            [(row + i, col) for i in range(1, 8 - row)],
            [(row, col - i) for i in range(1, col + 1)],
            [(row, col + i) for i in range(1, 8 - col)],
            [(row - i, col - i) for i in range(1, row + 1)], #bishop moves
            [(row - i, col + i) for i in range(1, row + 1)],
            [(row + i, col - i) for i in range(1, 8 - row)],
            [(row + i, col + i) for i in range(1, 8 - row)],    
            (row + 2, col + 1),
            (row + 2, col - 1),
            (row - 2, col + 1),
            (row - 2, col - 1),
            (row + 1, col + 2),
            (row + 1, col - 2),
            (row - 1, col + 2),
            (row - 1, col - 2)
        ]
        for i in posible_ataks:
            for move in i:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if len(board[move[0]][move[1]]) == 0:
                        pass
                    elif board[move[0]][move[1]][0].islower():
                        pass
                    else:
                        pass
                else:
                    break
            

        
    
