import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
import multiplayer
import chess
import time

global posible_moves
posible_moves = []


class Game:
    def __init__(self):
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "q", "", "", ""],
            ["", "", "p", "", "R", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "q", "", "p", "p"],
            ["P", "P", "P", "P", "", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        
        self.places = [[Square([row, col], color = "black" if (col +  row) % 2 else "white") for col in range(8)] for row in range(8)] 
        
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
    


class Square:
    def __init__(self, position, color):
        self.position = position
        self.color = color
    
    def __repr__(self):
        piece_info = f", piece={self.piece}" if self.piece else ""
        return f"Square({self.position}, {self.color}{piece_info})"


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Szachy Online")
        
        
class Menu_gui:
    def __init__(self):
        self.surface = create_example_window('Example - Simple', (600, 400))
        self.menu = pygame_menu.Menu(
            height=300,
            theme=pygame_menu.themes.THEME_BLUE,
            title='Welcome',
            width=400
        )

    def menu_gui(self):
        global user_name
        user_name = self.menu.add.text_input('Name: ', default='John Doe', maxchar=10)
        self.menu.add.button('Play solo', self.start_the_game_singleplayer)
        self.menu.add.button('Play ai', self.start_the_game_singleplayer)
        self.menu.add.button('Play multiplayer', self.start_the_game_multiplayer)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu.enable()
        self.menu.mainloop(self.surface)
        
        
        
    def start_the_game_singleplayer(self) -> None:
        print(f'{user_name.get_value()}, Do the job here!')
        self.menu.disable()
        game_interface_var = game_gui()
        game_interface_var.game_interface()
        
    def start_the_game_multiplayer(self) -> None:
        print(f'{user_name.get_value()}, Do the job here!')
        self.menu.disable()
        game_interface_var = game_gui()
        game_interface_var.game_interface()
        
        
class game_gui(Game):
    def __init__(self):
        super().__init__()
        self.game = Game()

        
    def game_interface(self, x = 900, y = 600):
        pygame.init()
        game = Game()
        global screen, square_size, border_size;
        square_size = int(round(y / 18 * 2))
        border_size = int(round(y / 18)) 

        screen = pygame.display.set_mode((x, y))
        
    
    def draw_board(self, x = 900, y = 600):
        game = Game()
        font = pygame.font.Font('freesansbold.ttf', border_size)
        
        pygame.draw.rect(screen, (22, 200, 100), (0, 0, y, y)) #this creates ther border around the board
        
        for i in range(1,9): #this loop is for writing the numbers on the board
            text = font.render(f"{9 - i}", True, (220, 0, 133), (22, 200, 100))
            screen.blit(text, (border_size / 3, (i*square_size)- (square_size - (border_size *1.5))))
        
        alfabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for i in range(1,9): #this loop is for writing alfabet on the board
            text = font.render(alfabet[i-1], True, (220, 0, 133), (22, 200, 100))
            screen.blit(text, ((i*square_size)- (square_size-(border_size * 1.7)), y - border_size )) 
        
        #this for loops are for drawing the board
        for i in range(1,9):  
            for j in range(1,9):
                board_square = game.places[i-1][j-1]
                if board_square.color == "white":
                    pygame.draw.rect(screen, (255, 255, 255), ((j*square_size)- (square_size-border_size), (i*square_size)- (square_size-border_size), square_size, square_size)) #(rect_x, rect_y, rect_width, rect_height)
                else:
                    pygame.draw.rect(screen, (100, 100, 100), ((j*square_size)- (square_size-border_size), (i*square_size)- (square_size-border_size), square_size, square_size))
        
        pygame.draw.rect(screen, (102, 0, 100), (y, 0, x - y, y)) 
        
        
        if posible_moves != []: #this if statement is for drawing the posible moves for clicked figure
            for move in posible_moves:
                if len(self.board[move[0]][move[1]]) > 0:
                    pygame.draw.rect(screen, (255, 0, 0), (((move[1]+1) *square_size)- (square_size-border_size), ((move[0]+1) *square_size)- (square_size-border_size), square_size, square_size))
                else:
                    pygame.draw.rect(screen, (0, 255, 0), (((move[1]+1) *square_size)- (square_size-border_size), ((move[0]+1) *square_size)- (square_size-border_size), square_size, square_size))
        
        self.check = chess.piece_moves.check(self.board)
        if self.check:
            print("white wins")
        if self.check:
            for i in range(0,8):
                for j in range(0,8):
                    if self.board[i][j] == "K":
                        pygame.draw.rect(screen, (255, 0, 0), (((j+1) *square_size)- (square_size-border_size), ((i+1) *square_size)- (square_size-border_size), square_size, square_size))
        pygame.display.update()
        
        
    def draw_pieces(self):
        for i in range(0,8): #this for loops are for drawing pieces on the board 
            for j in range(0,8):
                piece = self.board[i][j]
                if len(piece) == 0:
                    continue
                
                else:
                    if piece[0].upper() == "P":
                        if piece[0].isupper():
                            image_path = "assets/pb.png" 
                        else:
                            image_path = "assets/pw.png"   #white
 
                    elif piece[0].upper() == "R":
                        if piece[0].isupper():
                            image_path = "assets/rb.png" 
                        else:
                            image_path = "assets/rw.png"

                    elif piece[0].upper() == "N":
                        if piece[0].isupper():
                            image_path = "assets/nb.png" 
                        else:
                            image_path = "assets/nw.png"

                    elif piece[0].upper() == "B":
                        if piece[0].isupper():
                            image_path = "assets/bb.png" 
                        else:
                            image_path = "assets/bw.png" 

                    elif piece[0].upper() == "K":
                        if piece[0].isupper():
                            image_path = "assets/kb.png" 
                        else:
                            image_path = "assets/kw.png"

                    elif piece[0].upper() == "Q":
                        if piece[0].isupper():
                            image_path = "assets/qb.png" 
                        else:
                            image_path = "assets/qw.png"
                            
                    image = pygame.image.load(image_path)
                    scaled_image = pygame.transform.scale(image, (64, 64))
                    screen.blit(scaled_image, (((j + 1)*square_size - border_size, (i + 1)*square_size - border_size))) 
                
        pygame.display.update()
        
        
        
if __name__ == "__main__":
    menu = Menu_gui()
    menu.menu_gui()
    game = game_gui()
    
    game.draw_board()
    game.draw_pieces()
    
    #game runing###########################
    global selected_piece
    running = True
    dragging = False
    selected_piece = None
    posible_moves = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    col = (mouse_x - border_size) // square_size
                    row = (mouse_y - border_size) // square_size
                    
                    # this check if you clikced on a piece
                    if row >=0 and col >=0 and row <= 7 and col <= 7 and len(game.board[row][col]) > 0:
                        dragging = True
                        offset_x = mouse_x - (col * square_size + square_size // 2)

                        selected_piece = str(game.board[row][col][0])
                        offset_x = mouse_x - (col * square_size + square_size // 2)
                        offset_y = mouse_y - (row * square_size + square_size // 2)

                        if selected_piece.upper() == "P": 
                            posible_moves = chess.piece_moves.pawn_moves(game.board, row, col)

                        elif selected_piece.upper() == "R":
                            posible_moves = chess.piece_moves.rook_moves(game.board, row, col)

                        elif selected_piece.upper() == "N":
                            posible_moves = chess.piece_moves.knight_moves(game.board, row, col)

                        elif selected_piece.upper() == "B":
                            posible_moves = chess.piece_moves.bishop_moves(game.board, row, col)

                        elif selected_piece.upper() == "K":
                            posible_moves = chess.piece_moves.king_moves(game.board, row, col)

                        elif selected_piece.upper() == "Q":
                            posible_moves = chess.piece_moves.queen_moves(game.board, row, col)

                        game.draw_board()
                        game.draw_pieces()
                        
                    else:
                        dragging = False
                        selected_piece = None
                        
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging:
                    mouse_x, mouse_y = event.pos
                    new_col = (mouse_x - border_size) // square_size
                    new_row = (mouse_y - border_size) // square_size
                    piece_pos = (new_row, new_col)
                    dragging = False

                    if len(posible_moves) != 0:
                        for i in posible_moves:
                            if new_row >=0 and new_col >=0 and new_row <= 7 and new_col <= 7 and i[0] == new_row and i[1] == new_col:

                                game.board[new_row][new_col] = game.board[row][col]
                                game.board[row][col] = ""

                                posible_moves = []
                                game.draw_board()
                                game.draw_pieces()
