import chess

class AI:
    def __init__(self):
        self.best_score = 0
        self.score = 0
        
    
    def ai(self, board, turn, my_color, en_passant, castling):
        move = self.min_max(1, board, my_color, turn, en_passant, castling, None)
        print("ruch ai to:", move)
        return move


    def min_max(self, depht, board, my_color, turn, en_passant, castling, move): #not worikin yet
        if depht == 0 or self.game_ended():
            return move

        if move != None:
            print("ruch to " ,move)
            
        if my_color != turn: #posible ai move
            max_val = -999999999
            pieces = self.all_pieces(board)
            moves = self.all_moves(board, pieces, turn, my_color, en_passant, castling)
            for move_set in range(len(moves)):
                for move in  moves[move_set][1]:
                    board_after_move = self.board_after_move(board, (moves[move_set][0], move))
                    varible = (self.evaluating(board_after_move, self.all_pieces(board_after_move), my_color), (moves[move_set][0], move))
                    print("varible", varible)
                    value = self.min_max(depht - 1, board_after_move, my_color, "white" if turn == "black" else "white", en_passant, castling, varible)
                    valuee = self.evaluating(board_after_move, self.all_pieces(board_after_move), my_color)

                    if max_val < valuee:
                        best_move = (moves[move_set][0], move)
                        print("best move: ", best_move)
                    max_val = max(valuee, max_val)
                        
            max_val = (max_val, best_move)
            return max_val
        
        else: #posible player move
            max_val = -999999999
            pieces = self.all_pieces(board)
            moves = self.all_moves(board, pieces, turn, my_color, en_passant, castling)
            for move_set in range(len(moves)):
                for move in  moves[move_set][1]:
                    board_after_move = self.board_after_move(board, (moves[move_set][0], move))
                    varible = (self.evaluating(board_after_move, self.all_pieces(board_after_move), my_color), (moves[move_set][0], move))
                    print("varible", varible)
                    value = self.min_max(depht - 1, board_after_move, my_color, "white" if turn == "black" else "white", en_passant, castling, varible)
                    valuee = self.evaluating(board_after_move, self.all_pieces(board_after_move), my_color)
                    
                    if max_val < valuee:
                        best_move = (moves[move_set][0], move)
                        print("best move: ", best_move)
                    min_val = min(valuee, min_val)  
            
            min_val = (min_val, best_move)
            return min_val

        

    def all_moves(self, board, pieces, turn, my_color, en_passant, castling):
        chess_moves = chess.piece_moves()
        
        moves = []
        for color in range(2):
            if (color == 0 and turn == "white") or (color == 1 and turn == "black"):
                for r, c in pieces[color]:
                    piece = board[r][c]
                    if piece.lower() == "p":
                        moves.append(((r,c), chess_moves.pawn_moves(board, r, c, turn, my_color, en_passant)))
                        
                    elif piece.lower() == "n":
                        moves.append(((r,c), chess_moves.knight_moves(board, r, c, turn, my_color)))
                    
                    elif piece.lower() == "b":
                        moves.append(((r,c), chess_moves.bishop_moves(board, r, c, turn, my_color)))
                    
                    elif piece.lower() == "r":
                        moves.append(((r,c), chess_moves.rook_moves(board, r, c, turn, my_color)))
                    
                    elif piece.lower() == "q":
                        moves.append(((r,c), chess_moves.king_moves(board, r, c, turn, castling, my_color)))
                    
                    elif piece.lower() == "k":
                        moves.append(((r,c), chess_moves.queen_moves(board, r, c, turn, my_color)))
        return moves
                    
    
    def  all_pieces(self, board):
        pieces =  [[], []]
        for r in range(8):
            for c in range(8):
                if board[r][c]:
                    if board[r][c].islower():
                        pieces[0].append((r, c))
                    
                    else:
                        pieces[1].append((r, c))
        return pieces
    
     
    def evaluating(self, board, pieces, my_color):
        white, black = 0, 0
        points = 0
        for color in range(2):
            for r, c in pieces[color]:
                if board[r][c].lower() == "p":
                    points += 1
                    
                elif board[r][c].lower() == "b":
                    points += 3
                    
                elif board[r][c].lower() == "n":
                    points += 3
                    
                elif board[r][c].lower() == "r":
                    points += 5
                    
                elif board[r][c].lower() == "q":
                    points += 9
                    
                elif board[r][c].lower() == "k":
                    points += 0
                    
            if color == 0:
                white += points
            else:
                black += points
            points = 0
        print(white,"  " , black, pieces)
        
        score = white - black if my_color == "black" else (white - black) * -1
        return score
    
    
    
    def game_ended(self):
        return False
        pass
    
    
    def board_after_move(self, board, move):
        row, col, row_move, col_move = move[0][0], move[0][1], move[1][0], move[1][1]
        board_after_move = [list(row) for row in board]
        board_after_move[row_move][col_move] = board[row][col]
        board_after_move[row][col] = ""
        
        return board_after_move
    
#made by: rokrerum
