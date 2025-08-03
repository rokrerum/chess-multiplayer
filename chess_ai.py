import chess

class AI:
    def __init__(self):
        self.best_score = 0
        self.score = 0
        
    
    def ai(self, board, turn, my_color, en_passant, castling):

        return self.min_max(4, my_color, turn)


    def min_max(self, depht, board, my_color, turn, en_passant, castling): #not worikin yet
        if depht == 0:
            return True
        
        if my_color != turn: #posible bots move
            turn = "white" if turn == "black" else "white"
            pieces = self.all_pieces(board)
            moves = self.all_moves(board, pieces, turn, my_color, en_passant, castling)
            self.min_max(depht - 1, board, my_color, turn, en_passant, castling)
            max(1,2)
            
        else: #posible player move
            pass    

    
    def all_moves(self, board, pieces, turn, my_color, en_passant, castling):
        moves = []
        for color in pieces:
            if (color == 0 and turn == "white") or (color == 1 and turn == "black"):
                for r, c in color:
                    piece = board[r][c]
                    if piece.lower() == "p":
                        moves.append(chess.piece_moves.pawn_moves(board, r, c, turn, my_color, en_passant))
                        
                    elif piece.lower() == "n":
                        moves.append(chess.piece_moves.knight_moves(board, r, c, turn, my_color))
                    
                    elif piece.lower() == "b":
                        moves.append(chess.piece_moves.bishop_moves(board, r, c, turn, my_color))
                    
                    elif piece.lower() == "r":
                        moves.append(chess.piece_moves.rook_moves(board, r, c, turn, my_color))
                    
                    elif piece.lower() == "q":
                        moves.append(chess.piece_moves.king_moves(board, r, c, turn, castling, my_color))
                    
                    elif piece.lower() == "k":
                        moves.append(chess.piece_moves.queen_moves(board, r, c, turn, my_color))
                    
    
    def  all_pieces(self, board):
        pieces =  [[], []]
        for r in range(8):
            for c in range(8):
                if board[r][c] and board[r][c].lower() == board[r][c]:
                    pieces[0].append((r, c))
                
                elif board[r][c]:
                    pieces[1].append((r, c))
        
        return pieces
    
     
    def evaluating(self, board, pieces):
        white, black = 0, 0
        points = 0
        for color in pieces:
            for r, c in color:
                if board[r][c].lower() == "p":
                    points = 1
                    
                elif board[r][c].lower() == "b":
                    points = 3
                    
                elif board[r][c].lower() == "n":
                    points = 3
                    
                elif board[r][c].lower() == "r":
                    points = 5
                    
                elif board[r][c].lower() == "q":
                    points = 9
                    
                elif board[r][c].lower() == "k":
                    points = 0
                    
            if color == 0:
                white += points
            else:
                black += points
            
        return white - black
