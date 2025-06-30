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
                if board[row + 1][col] == " ":
                    posible_moves.append([row - 1, col])
            
            if col + 1 < 8 and len(board[row - 1][col + 1]) > 0 and board[row - 1][col + 1][0].lower() == board[row - 1][col + 1][0]:
                posible_moves.append([row - 1, col + 1])
            
            if col - 1 < 8 and len(board[row - 1][col - 1]) > 0 and board[row - 1][col - 1][0].lower() == board[row - 1][col - 1][0]:
                posible_moves.append([row - 1, col - 1])
                
        return posible_moves
    
        
    def rook_moves(board, row, col):
        pass
    
    
    def knight_moves(board, row, col):
        pass
    
    
    def bishop_moves(board, row, col):
        pass
    
    
    def queen_moves(board, row, col):
        pass
    
    
    def king_moves(board, row, col):
        pass
    
    
    def chec(self):
        if True:
            return True
        else:
            return False    
    
