

class Chess:
    def __init__(self):
        self.board = [
            [r],[h],[b],[k],[q],[b],[h],[r],
            [p],[p],[p],[p],[p],[p],[p],[p],
            [ ],[ ],[ ],[ ],[ ],[ ],[ ],[ ],
            [ ],[ ],[ ],[ ],[ ],[ ],[ ],[ ],
            [ ],[ ],[ ],[ ],[ ],[ ],[ ],[ ],
            [ ],[ ],[ ],[ ],[ ],[ ],[ ],[ ],
            [P],[P],[P],[P],[P],[P],[P],[P],
            [R],[H],[B],[K],[Q],[B],[H],[R],
        ]
        self.turn = "white"
        self.move_history = []
        self.en_passant = None
        self.castling = {"white": {"king": True, "queen": True}, "black": {"king": True, "queen": True}}
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.check = False
        self.checkmate = False
        self.draw = False
        self.threefold_repetition = False
        self.fifty_move_rule = False
        self.insufficient_material = False
        self.fivefold_repetition = False
        



class piece_moves:
    def pawn_moves(self):
        pass
    def rook_moves(self):
        pass
    def knight_moves(self):
        pass
    def bishop_moves(self):
        pass
    def queen_moves(self):
        pass
    def king_moves(self):
        pass
    
