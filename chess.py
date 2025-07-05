class piece_moves:
    global posible_moves
    
    def pawn_moves(board, row, col):#to remake becouse of my bad code
        posible_moves = []
        if board[row][col][0] == "P":
            if row == 6:
                if len(board[row - 1][col]) == 0:
                    posible_moves.append([row - 1, col])
                    
                    if len(board[row - 2][col]) == 0:
                        posible_moves.append([row - 2, col])

            else:
                if len(board[row - 1][col]) <= 0:
                    print("pole na planszy" + board[row - 1][col])
                    posible_moves.append([row - 1, col])
            
            if col + 1 < 8 and len(board[row - 1][col + 1]) > 0 and board[row - 1][col + 1][0].lower() == board[row - 1][col + 1][0]:
                posible_moves.append([row - 1, col + 1])
            
            if col - 1 < 8 and len(board[row - 1][col - 1]) > 0 and board[row - 1][col - 1][0].lower() == board[row - 1][col - 1][0]:
                posible_moves.append([row - 1, col - 1])
        
        else:
            posible_moves = []
                
        return posible_moves
    
        
    def rook_moves(board, row, col): #to remake becouse of my bad code
        posible_moves = []
        #verticle
        if board[row][col][0] == "R":
            for i in range(row - 1, -1, -1): 
                if len(board[i][col]) > 0:
                    if  board[i][col][0].isupper():
                        break
                    else:
                        posible_moves.append([i, col])
                        break
                posible_moves.append([i, col])

            for i in range(row + 1, 8):
                if len(board[i][col]) > 0:
                    if  board[i][col][0].isupper():
                        break
                    else:
                        posible_moves.append([i, col])
                        break
                posible_moves.append([i,col])

            #horizontal
            for i in range(col - 1, -1, -1): 
                if len(board[row][i]) > 0:
                    if  board[row][i][0].isupper():
                        break
                    else:
                        posible_moves.append([row, i])
                        break
                posible_moves.append([row, i])

            for i in range(col + 1, 8): 
                if len(board[row][i]) > 0:
                    if  board[row][i][0].isupper():
                        break
                    else:
                        posible_moves.append([row, i])
                        break
                posible_moves.append([row, i])

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
    
    
    def bishop_moves(board, row, col): #not working
        posible_moves = []
        moves = [
            [(row - i, col - i) for i in range(1, row)],
            [(row - i, col + i) for i in range(row)],
            [(row - i, col + i) for i in range(row + 1, 8)],
            [(row - i, col + i) for i in range()],
        ]
        if(board[row][col][0] == "B"):
            for i in moves:
                for move in i:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        if len(board[move[0]][move[1]]) == 0 or board[move[0]][move[1]][0].islower():
                            posible_moves.append(move)
                        else:
                            break
                    else:
                        break
                
        return posible_moves
        
    
    
    def queen_moves(board, row, col):
        pass
    
    
    def king_moves(board, row, col):
        pass
    
    
    def chec(self):
        if True:
            return True
        else:
            return False    
    
