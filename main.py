import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
import chess
import random
import chess_ai
import multiplayer
import time


global posible_moves
posible_moves = []


class Game:
    def __init__(self):
        self.board = [
            ["r", "", "", "", "k", "", "R", "r"], #white
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "q", "", "", ""],
            ["", "", "p", "", "R", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "p", "", "q", "", "p", "p"],
            ["P", "P", "P", "P", "", "P", "P", "P"], 
            ["R", "N", "B", "Q", "K", "B", "N", "R"] #black
        ]
        
        self.places = [[Square([row, col], color = "black" if (col +  row) % 2 else "white") for col in range(8)] for row in range(8)] 
        
        self.turn = "white"
        self.move_history = []
        self.en_passant = None
        self.castling = {"white": {"king": True, "Rook-L": True, "Rook-R": True}, "black": {"king": True, "Rook-L": True, "Rook-R": True}}
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
        self.surface = create_example_window('Example - Simple', (600, 500))
        self.selected_color = "random"
        self.menu = pygame_menu.Menu(
            height=400,
            theme=pygame_menu.themes.THEME_BLUE,
            title='Welcome',
            width=400
        )
        
        
    def set_color(self, color_value):
        self.selected_color = color_value
        print(f"Wybrano kolor: {color_value}")
        

    def menu_gui(self):
        global user_name
        user_name = self.menu.add.text_input('Name: ', default='John Doe', maxchar=10)
        
        frame = self.menu.add.frame_h(338, 58)
        white_button = frame.pack(self.menu.add.button('White', self.set_color, 'white'))
        random_button = frame.pack(self.menu.add.button('Random', self.set_color, 'random')) 
        black_button = frame.pack(self.menu.add.button('Black', self.set_color, 'black'))
        random_button.apply()
        
        self.menu.add.button('Play solo', self.start_the_game_singleplayer)
        self.menu.add.button('Play ai', self.start_the_game_against_ia)
        self.menu.add.button('Play multiplayer', self.start_the_game_multiplayer)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu.enable()
        self.menu.center_content()
        self.menu.mainloop(self.surface)
        
        
        
    def start_the_game_singleplayer(self) -> None:
        print(f'{user_name.get_value()}, Do the job here!')
        global two_players
        two_players = False
        self.menu.disable()
        game_interface_var = game_gui()
        game_interface_var.game_interface()
        
    def start_the_game_against_ia(self):
        print(f'{user_name.get_value()}, Do the job here!')
        global two_players
        two_players = True
        self.menu.disable()
        game_interface_var = game_gui()
        game_interface_var.game_interface()
        
    def start_the_game_multiplayer(self) -> None:
        print(f'{user_name.get_value()}, Do the job here!')
        global two_players
        two_players = True
        self.menu.disable()
        game_interface_var = game_gui()
        game_interface_var.game_interface()
        
        
class game_gui(Game,  Menu_gui):
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
        
        chess_moves = chess.piece_moves()
        self.check = chess_moves.check(self.board, my_color)
        for i in range(2):  #this for loop is for drawing the check for the king
            if self.check[i][0]:
                pygame.draw.rect(screen, (255, 0, 0), (((self.check[i][1][1] + 1) *square_size)- (square_size-border_size), ((self.check[i][1][0] +1 ) *square_size)- (square_size-border_size), square_size, square_size))
                
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
        
        
    def show_promotion_menu(self):
        # Pobierz grafiki figur
        queen_img = pygame.image.load("assets/qw.png")
        rook_img = pygame.image.load("assets/rw.png")
        bishop_img = pygame.image.load("assets/bw.png")
        knight_img = pygame.image.load("assets/nw.png")

        # Narysuj tło menu
        pygame.draw.rect(screen, (200, 200, 200), (square_size * 2, square_size * 3.75, square_size * 5, square_size * 1.5))  # Prostokąt
        pygame.draw.rect(screen, (50, 50, 50), (square_size * 2, square_size * 3.75, square_size * 5, square_size * 1.5), 3)   # Ramka

        # Wyświetl ikony
        screen.blit(queen_img, (square_size * 2.3, square_size * 4))
        screen.blit(rook_img, (square_size * 3.4, square_size * 4))
        screen.blit(bishop_img, (square_size * 4.6, square_size * 4))
        screen.blit(knight_img, (square_size * 5.7, square_size * 4))

        pygame.display.update()
        
        
        
if __name__ == "__main__":
        #game runing###########################
    global selected_piece, turn, my_color
    turn = "white"
    my_color = "black"
    running = True
    dragging = False
    selected_piece = None
    posible_moves = []
    
    menu = Menu_gui()
    menu.menu_gui()

    game = game_gui()
    game.draw_board()
    
    menu.selected_color = random.choice(("black", "white")) if menu.selected_color == "random" else menu.selected_color #change color randomly if option random is selected
    if menu.selected_color == "white": #not
        my_color = "white"
        for i in range(8): #this is for reversing the board if player selected white
            game.board[i].reverse()
        game.board.reverse()
    else:
        my_color = "black"
        
    game.draw_pieces()
    

    print(menu.selected_color)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if two_players == True and turn == my_color or two_players == False:

                if event.type == pygame.MOUSEBUTTONDOWN:
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
                            
                            
                            chess_moves = chess.piece_moves()
                            if selected_piece.upper() == "P": 
                                posible_moves = chess_moves.pawn_moves(game.board, row, col, turn, my_color)

                            elif selected_piece.upper() == "R":
                                posible_moves = chess_moves.rook_moves(game.board, row, col, turn, my_color)

                            elif selected_piece.upper() == "N":
                                posible_moves = chess_moves.knight_moves(game.board, row, col, turn, my_color)

                            elif selected_piece.upper() == "B":
                                posible_moves = chess_moves.bishop_moves(game.board, row, col, turn, my_color)

                            elif selected_piece.upper() == "K":
                                posible_moves = chess_moves.king_moves(game.board, row, col, turn, game.castling, my_color)

                            elif selected_piece.upper() == "Q":
                                posible_moves = chess_moves.queen_moves(game.board, row, col, turn, my_color)

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
                                    
                                    
                                    if game.board[row][col] in ("K", "k", "R", "r"): # if you move a king or a rook u cant use it for castling
                                        if game.board[row][col] in ("K", "k"):
                                            if game.board[row][col] == "k":
                                                for state in game.castling["white"]:
                                                    game.castling["white"][state] = False
                                            else:
                                                for state in game.castling["black"]:
                                                    game.castling["black"][state] = False
                                                
                                            
                                        elif game.board[row][col] in ("R", "r"):
                                            if game.board[row][col] == "r":
                                                if col == 0 and row in (0, 7):
                                                    game.castling["white"]["Rook-L"] = False
                                                elif col == 7 and row in (0, 7):
                                                    game.castling["white"]["Rook-R"] = False
                                                
                                            else:
                                                if col == 0 and row in (0, 7):
                                                    game.castling["black"]["Rook-L"] = False
                                                elif col == 7 and row in (0, 7):
                                                    game.castling["black"]["Rook-R"] = False
                                                    
                                                    
                                    print(game.castling)
                                    if len(i) == 3: #checking if the move is castling and if it is, it will move the rook
                                        if new_col < col:
                                            game.board[row][new_col + 1] = game.board[row][0]
                                            game.board[row][0] = ""
                                        else:
                                            game.board[row][new_col - 1] = game.board[row][0]
                                            game.board[row][7] = ""
                                            
                                            
                                    if game.board[row][col] in ("p", "P"): # if pawn moves to the last row, it will be promoted
                                        if new_row in (0, 7): #promotion of the client player
                                            if two_players == False: # if it is silgle player, the player can choose what piece to promote to

                                                game.show_promotion_menu()
                                                waiting = True
                                                while waiting:
                                                    for event in pygame.event.get():
                                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                            mouse_x, mouse_y = event.pos
                                                            x, y = square_size, square_size
                                                            
                                                            
                                                            # Sprawdź, który przycisk został kliknięty
                                                            if x * 2.3 <= mouse_x <= (x * 2.3) + 64 and y * 4 <= mouse_y <= y * 4 + 100: #the promotion menu is not working correctly the clicking boxes are not set correctly
                                                                game.board[row][col] = "q" if turn == "white" else "Q"
                                                                waiting = False
                                                                
                                                            elif x + 100 <= mouse_x <= x + 200 and y * 4 <= mouse_y <= y * 4 + 100:
                                                                game.board[row][col] = "r" if turn == "white" else "R"
                                                                waiting = False
                                                                
                                                            elif x + 200 <= mouse_x <= x + 300 and y * 4 <= mouse_y <= y * 4 + 100:
                                                                game.board[row][col] = "b" if turn == "white" else "B"
                                                                waiting = False
                                                                
                                                            elif x + 300 <= mouse_x <= x + 400 and y * 4 <= mouse_y <= y * 4 + 100:
                                                                game.board[row][col] = "n" if turn == "white" else "N"
                                                                waiting = False
                                            
                                            else: # if it is multiplayer, the AI or another player will choose what piece to promote to
                                                pass
                                            
                                    game.board[new_row][new_col] = game.board[row][col]
                                    game.board[row][col] = ""

                                    posible_moves = []
                                    game.draw_board()
                                    game.draw_pieces()

                                    turn = "white" if turn == "black" else "black"
                                    
                                    
            elif two_players == True and turn != my_color: # 2 players
                if True: # AI turn (against AI)
                    pass
                elif True: # another player turn (against another player online)
                    pass    
                
#made by: rokrerum
