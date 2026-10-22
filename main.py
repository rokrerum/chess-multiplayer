import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
import chess
import random
import chess_ai
import multiplayer

global posible_moves
posible_moves = []
BG = (24, 24, 26)
BTN = (45, 45, 50)
GOLD = (255, 215, 0)
TEXT = (230, 230, 230)
MUTED = (150, 150, 155)
DARK = (24, 24, 26)
BTN_W = 300

class Game:
    def __init__(self):
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],  # white
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]  # black
        ]

        self.places = [[Square([row, col], color="black" if (col + row) % 2 else "white") for col in range(8)] for row
                       in range(8)]

        self.turn = "white"
        self.last_move = None
        self.move_history = []
        self.en_passant = [False]
        self.castling = {"white": {"king": True, "Rook-L": True, "Rook-R": True},
                         "black": {"king": True, "Rook-L": True, "Rook-R": True}}
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.check = False
        # self.threefold_repetition = False
        # self.fifty_move_rule = False
        # self.insufficient_material = False
        # self.fivefold_repetition = False

    def reset_to_default(self):
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],  # white
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]  # black
        ]
        self.turn = "white"
        self.move_history = []
        self.en_passant = [False]
        self.castling = {"white": {"king": True, "Rook-L": True, "Rook-R": True},
                         "black": {"king": True, "Rook-L": True, "Rook-R": True}}
        self.check = False



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
        self.surface = create_example_window('Szachy', (700, 650))
        self.selected_color = "random"

        chess_theme = pygame_menu.Theme(
            background_color=(24, 24, 26),
            title_background_color=(18, 110, 65),
            title_font=pygame_menu.font.FONT_8BIT,
            title_font_size=38,
            title_font_color=(255, 215, 0),
            widget_font=pygame_menu.font.FONT_OPEN_SANS_BOLD,
            widget_font_size=24,
            widget_font_color=(230, 230, 230),
            widget_margin=(0, 12),
            selection_color=(255, 215, 0),
        )

        self.menu = pygame_menu.Menu(
            height=650,
            width=700,
            theme=chess_theme,
            title='Szachy'
        )


    def set_color(self, color_value):
        self.selected_color = color_value
        for name, btn in self.color_buttons.items():
            active = name == color_value
            btn.set_background_color(GOLD if active else BTN)
            btn.update_font({'color': DARK if active else TEXT,
                             'selected_color': DARK if active else GOLD})


    def style_button(self, btn, bg=BTN, border=GOLD, padding=(8, 22), primary=False):
        if primary:
            bg, border = GOLD, GOLD
            btn.update_font({'color': DARK, 'selected_color': DARK})
        btn.set_background_color(bg)
        btn.set_border(2, border)
        btn.set_padding(padding)
        return btn


    def equalize_width(self, buttons, width=BTN_W):
        for b in buttons:
            extra = max(0, (width - b.get_width()) // 2)
            b.set_padding((8, 22 + extra))


    def section(self, text):
        self.menu.add.label(text.upper(), font_size=14, font_color=MUTED)

    def menu_gui(self):
        menu.surface = pygame.display.set_mode((700, 650))
        global user_name
        self.menu.clear()
        self.color_buttons = {}

        self.section("Gracz")
        user_name = self.menu.add.text_input('', default='Gracz', maxchar=10)

        self.menu.add.vertical_margin(4)
        self.section("Twój kolor")
        frame = self.menu.add.frame_h(360, 70, margin=(10, 0))
        for key, label in (('white', 'Białe'), ('random', 'Losowo'), ('black', 'Czarne')):
            b = self.style_button(self.menu.add.button(label, self.set_color, key), padding=(4, 16))
            b.set_margin(0, 0)
            frame.pack(b)
            self.color_buttons[key] = b
        self.color_buttons['random'].apply()

        self.menu.add.vertical_margin(10)
        self.section("Tryb gry")
        play = [
            self.style_button(self.menu.add.button('Graj z AI', self.start_the_game_against_ia), primary=True),
            self.style_button(self.menu.add.button('Graj solo', self.start_the_game_singleplayer)),
            self.style_button(self.menu.add.button('Multiplayer', self.start_the_game_multiplayer)),
        ]
        exit_btn = self.style_button(self.menu.add.button('Wyjście', pygame_menu.events.EXIT),
                                     bg=(60, 30, 30), border=(200, 80, 80))
        self.equalize_width(play + [exit_btn])

        self.menu.add.vertical_margin(10)
        self.menu.add.label("v1.0", font_size=12, font_color=(100, 100, 105))

        self.menu.enable()
        self.menu.center_content()
        self.menu.mainloop(self.surface)


    def start_the_game_singleplayer(self) -> None:
        global two_players
        two_players = False
        self.menu.disable()
        game_interface_var = game_gui()
        game_interface_var.game_interface()


    def start_the_game_against_ia(self):
        global two_players
        two_players = True
        self.menu.disable()
        game_interface_var = game_gui()
        game_interface_var.game_interface()


    def start_the_game_multiplayer(self) -> None:
        global two_players
        two_players = True
        self.menu.disable()
        game_interface_var = game_gui()
        game_interface_var.game_interface()


class game_gui(Game, Menu_gui):
    def __init__(self):
        super().__init__()
        self.game = Game()


    def to_screen(self, row, col, my_color):
        if my_color == "white":
            return 7 - row, 7 - col
        return row, col


    def to_board(self, screen_row, screen_col, my_color):
        if my_color == "white":
            return 7 - screen_row, 7 - screen_col
        return screen_row, screen_col


    def game_interface(self, x=900, y=600):
        pygame.init()
        game = Game()
        global screen, square_size, border_size, piece_images
        square_size = int(round(y / 18 * 2))
        border_size = int(round(y / 18))

        screen = pygame.display.set_mode((x, y))

        piece_images = {}
        for piece_char, filename in PIECE_IMAGE_FILES.items():
            image = pygame.image.load(f"assets/{filename}").convert_alpha()
            piece_images[piece_char] = pygame.transform.scale(image, (64, 64))


    def draw_board(self, x=900, y=600):
        game = Game()
        font = pygame.font.Font('freesansbold.ttf', border_size)

        pygame.draw.rect(screen, (50, 50, 50), (0, 0, y, y))  # this creates ther border around the board


        for i in range(1, 9):  # this loop is for writing the numbers on the board
            number = i
            if my_color == "black":
                number = 9 - i
            text = font.render(f"{9 - number}", True, (222, 222, 222), (50, 50, 50))
            screen.blit(text, (border_size / 3, (i * square_size) - (square_size - (border_size * 1.5))))

        alfabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for i in range(1, 9):  # this loop is for writing alfabet on the board
            number = i
            if my_color == "black":
                number = 9 - i
            text = font.render(alfabet[number - 1], True, (222, 222, 222), (50, 50, 50))
            screen.blit(text, ((i * square_size) - (square_size - (border_size * 1.7)), y - border_size))

        # this for loops are for drawing the board
        for i in range(1, 9):
            for j in range(1, 9):
                board_square = game.places[i - 1][j - 1]
                if board_square.color == "white":
                    pygame.draw.rect(screen, (255, 255, 255), ((j * square_size) - (square_size - border_size),
                                                               (i * square_size) - (square_size - border_size), square_size, square_size))  # (rect_x, rect_y, rect_width, rect_height)
                else:
                    pygame.draw.rect(screen, (100, 100, 100), ((j * square_size) - (square_size - border_size),
                                                               (i * square_size) - (square_size - border_size), square_size, square_size))

        pygame.draw.rect(screen, (24, 24, 26), (y, 0, x - y, y))

        if posible_moves != []:  # this if statement is for drawing the posible moves for clicked figure
            for move in posible_moves:
                row, col = self.to_board(move[0], move[1], my_color) #changes the values to be correct with position of what player sees
                if len(self.board[move[0]][move[1]]) > 0:
                    pygame.draw.rect(
                        screen,
                        (255, 0, 0),
                        (
                        ((col + 1) * square_size) - (square_size - border_size),
                        ((row + 1) * square_size) - (square_size - border_size),
                        square_size,
                        square_size
                        )
                    )
                else:
                    pygame.draw.rect(
                        screen,
                        (0, 255, 0),
                        (
                        ((col + 1) * square_size) - (square_size - border_size),
                        ((row + 1) * square_size) - (square_size - border_size),
                        square_size,
                        square_size,
                        ),
                    )

        chess_moves = chess.piece_moves()
        self.check = chess_moves.check(self.board, my_color)
        for i in range(2):  # this for loop is for drawing the check for the king
            if self.check[i][0]:
                row, col = self.to_board(self.check[i][1][0] , self.check[i][1][1] , my_color) #changes the values to be correct with position of what player sees
                pygame.draw.rect(screen, (255, 0, 0),
                                 (((col + 1) * square_size) - (square_size - border_size),
                                  ((row + 1) * square_size) - (square_size - border_size), square_size,
                                  square_size))

        if self.last_move != None:
            for move in self.last_move:
                highlight_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                highlight_surface.fill((255, 215, 0, 90))  # złoty, półprzezroczysty
                if my_color == "white":
                    screen.blit(
                        highlight_surface,
                        (
                            ((abs(move[1] - 7) + 1) * square_size) - (square_size - border_size),
                            ((abs(move[0] - 7) + 1) * square_size) - (square_size - border_size),
                        )
                    )
                else:
                    screen.blit(
                        highlight_surface,
                        (
                            ((move[1] + 1) * square_size) - (square_size - border_size),
                            ((move[0] + 1) * square_size) - (square_size - border_size),
                        )
                    )
        #pygame.display.update()


    def draw_pieces(self):
        for i in range(0, 8):  # this for loops are for drawing pieces on the board
            for j in range(0, 8):
                piece = self.board[i][j]
                if len(piece) == 0:
                    continue

                scaled_image = piece_images[piece]
                row, col = self.to_board(i, j, my_color) #changes the values to be correct with position of what player sees
                if moving_pieces and moving_pieces[1][0] == i and moving_pieces[1][1] == j:  # drawing picked up piece
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    screen.blit(scaled_image, (mouse_x - 32, mouse_y - 32))
                else:
                    screen.blit(scaled_image, (((col + 1) * square_size - border_size, (row + 1) * square_size - border_size)))

        pygame.display.update()

    def show_promotion_menu(self):
        queen_img = pygame.image.load("assets/qw.png")
        rook_img = pygame.image.load("assets/rw.png")
        bishop_img = pygame.image.load("assets/bw.png")
        knight_img = pygame.image.load("assets/nw.png")

        panel_rect = (square_size * 2, square_size * 3.75, square_size * 5, square_size * 1.5)
        pygame.draw.rect(screen, (30, 30, 32), panel_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 215, 0), panel_rect, 3, border_radius=10)

        screen.blit(queen_img, (square_size * 2.3, square_size * 4))
        screen.blit(rook_img, (square_size * 3.4, square_size * 4))
        screen.blit(bishop_img, (square_size * 4.6, square_size * 4))
        screen.blit(knight_img, (square_size * 5.7, square_size * 4))

        pygame.display.update()

    def game_ended(self, what_happend, turn):
        font_win_text = pygame.font.Font('freesansbold.ttf', int(border_size * 1.7))
        font_button = pygame.font.Font('freesansbold.ttf', border_size)

        panel_rect = (square_size * 1, square_size * 2.75, square_size * 7, square_size * 3.5)
        pygame.draw.rect(screen, (24, 24, 26), panel_rect, border_radius=14)
        pygame.draw.rect(screen, (255, 215, 0), panel_rect, 3, border_radius=14)

        if what_happend == "mate":
            text = font_win_text.render(f"{turn.capitalize()} wygrywa!", True, (255, 215, 0))
            text_rect = text.get_rect(center=(square_size * 4.5, square_size * 4.1))
            screen.blit(text, text_rect)

        elif what_happend == "stalemate":
            text = font_win_text.render("Pat", True, (230, 230, 230))
            text_rect = text.get_rect(center=(square_size * 4.5, square_size * 4.1))
            screen.blit(text, text_rect)

        button_rect = (square_size * 3.5, square_size * 5.2, square_size * 2, square_size * 0.75)
        pygame.draw.rect(screen, (45, 45, 50), button_rect, border_radius=8)
        pygame.draw.rect(screen, (255, 215, 0), button_rect, 2, border_radius=8)

        text = font_button.render("Menu", True, (230, 230, 230))
        text_rect = text.get_rect(center=(square_size * 4.5, square_size * 5.575))
        screen.blit(text, text_rect)

        pygame.display.update()


if __name__ == "__main__":
    # game runing###########################
    chess_moves = chess.piece_moves()
    chess_bot = chess_ai.AI()
    game = game_gui()
    menu = Menu_gui()

    global selected_piece, turn, my_color, moving_pieces, PIECE_IMAGE_FILES
    turn = "white"
    my_color = "black"
    app_running, game_running = True, True
    dragging = False
    selected_piece = None
    posible_moves = []
    moving_pieces = [] #it will contain what piece it is, position on board
    PIECE_IMAGE_FILES = {
        "p": "pw.png", "P": "pb.png",
        "r": "rw.png", "R": "rb.png",
        "n": "nw.png", "N": "nb.png",
        "b": "bw.png", "B": "bb.png",
        "k": "kw.png", "K": "kb.png",
        "q": "qw.png", "Q": "qb.png",
    }

    menu.menu_gui()

    while app_running:
        game_running = True
        turn = "white"
        posible_moves = []
        moving_pieces = []
        selected_piece = None
        dragging = False
        game.last_move = None
        menu.selected_color = random.choice(("black", "white")) if menu.selected_color == "random" else menu.selected_color  # change color randomly if option random is selected
        game.reset_to_default()

        if menu.selected_color == "white":  # not
            my_color = "white"
        else:
            my_color = "black"

        game.draw_board()
        game.draw_pieces()

        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    app_running = False
                    game_running = False

                if two_players == True and turn == my_color or two_players == False:  # 1 player (client)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_x, mouse_y = event.pos
                            col = (mouse_x - border_size) // square_size
                            row = (mouse_y - border_size) // square_size
                            row, col = game.to_board(row, col, my_color)

                            # this check if you clikced on a piece
                            if row >= 0 and col >= 0 and row <= 7 and col <= 7 and len(game.board[row][col]) > 0:
                                dragging = True
                                offset_x = mouse_x - (col * square_size + square_size // 2)

                                selected_piece = str(game.board[row][col][0])
                                offset_x = mouse_x - (col * square_size + square_size // 2)
                                offset_y = mouse_y - (row * square_size + square_size // 2)

                                ROOK_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                                BISHOP_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                                QUEEN_DIRS = ROOK_DIRS + BISHOP_DIRS

                                if selected_piece.upper() == "P":
                                    posible_moves = chess_moves.pawn_moves(game.board, row, col, turn, my_color, game.en_passant)

                                elif selected_piece.upper() == "R":
                                    posible_moves = chess_moves.sliding_moves(game.board, row, col, turn, my_color, ROOK_DIRS) #Rook

                                elif selected_piece.upper() == "N":
                                    posible_moves = chess_moves.knight_moves(game.board, row, col, turn, my_color)

                                elif selected_piece.upper() == "B":
                                    posible_moves = chess_moves.sliding_moves(game.board, row, col, turn, my_color, BISHOP_DIRS) #Bishop

                                elif selected_piece.upper() == "K":
                                    posible_moves = chess_moves.king_moves(game.board, row, col, turn, game.castling, my_color)

                                elif selected_piece.upper() == "Q":
                                    posible_moves = chess_moves.sliding_moves(game.board, row, col, turn, my_color, QUEEN_DIRS) #Queen

                                moving_pieces = [selected_piece, (row, col)]
                                game.draw_board()
                                game.draw_pieces()

                            else:
                                dragging = False
                                moving_pieces = []
                                selected_piece = None


                    elif (event.type == pygame.MOUSEMOTION) and selected_piece != None:
                        if (turn == "white" and selected_piece.islower()) or (turn == "black" and selected_piece.isupper()):
                            if dragging:
                                game.draw_board()
                                game.draw_pieces()
                        else: #turn of selected piece is in next round
                            moving_pieces = []
                            selected_piece = None
                            dragging = False

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1 and dragging:
                            mouse_x, mouse_y = event.pos
                            new_col = (mouse_x - border_size) // square_size
                            new_row = (mouse_y - border_size) // square_size
                            new_row, new_col = game.to_board(new_row, new_col, my_color)
                            piece_pos = (new_row, new_col)
                            dragging = False
                            moving_pieces = []
                            move_made = False

                            if len(posible_moves) != 0:
                                for i in posible_moves:
                                    if new_row >= 0 and new_col >= 0 and new_row <= 7 and new_col <= 7 and i[0] == new_row and i[1] == new_col:
                                        move_made = True
                                        if game.board[row][col] in ("K", "k", "R", "r"):  # if you move a king or a rook u cant use it for castling
                                            if game.board[row][col] in ("K", "k"):
                                                if game.board[row][col] == "k":
                                                    for state in game.castling["white"]:
                                                        game.castling["white"][state] = False
                                                else:
                                                    for state in game.castling["black"]:
                                                        game.castling["black"][state] = False


                                            elif game.board[row][col] in ("R", "r"):  # this will be activated if rook is moved and castling will not be posible with it
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

                                        if len(i) == 3:  # checking if the move is castling and if it is then it will move the rook ,or checks if it is enpassant
                                            if game.board[row][col].lower() == "k":
                                                if new_col < col:
                                                    game.board[row][new_col + 1] = game.board[row][0]
                                                    game.board[row][0] = ""
                                                else:
                                                    game.board[row][new_col - 1] = game.board[row][7]
                                                    game.board[row][7] = ""

                                            elif game.board[row][col].lower() == "p" and i[2] == "en_passant":
                                                game.en_passant = [True, new_row, new_col]

                                            elif game.board[row][col].lower() == "p" and i[2] == "en_passant_move":
                                                game.en_passant = [False]
                                                game.board[row][new_col] = ""

                                        else:
                                            game.en_passant = [False]

                                        if game.board[row][col] in ("p", "P"):  # if pawn moves to the last row, it will be promoted
                                            if new_row in (0, 7):  # promotion of the client player
                                                if two_players == False or turn == my_color:  # if it is silgle player, the player can choose what piece to promote to

                                                    game.show_promotion_menu()
                                                    waiting = True
                                                    while waiting:
                                                        for event in pygame.event.get():
                                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                                mouse_x, mouse_y = event.pos
                                                                x, y = square_size, square_size

                                                                # this checks if player clicked on the icons of pieces u can promote your pown into
                                                                if x * 2.3 <= mouse_x <= (x * 2.3) + 64 and y * 4 <= mouse_y <= y * 4 + square_size * 0.9:
                                                                    game.board[row][col] = "q" if turn == "white" else "Q"
                                                                    waiting = False

                                                                elif x * 3.4 <= mouse_x <= (x * 3.4) + 64 and y * 4 <= mouse_y <= y * 4 + square_size * 0.9:
                                                                    game.board[row][col] = "r" if turn == "white" else "R"
                                                                    waiting = False

                                                                elif x * 4.6 <= mouse_x <= (x * 4.6) + 64 and y * 4 <= mouse_y <= y * 4 + square_size * 0.9:
                                                                    game.board[row][col] = "b" if turn == "white" else "B"
                                                                    waiting = False

                                                                elif x * 5.7 <= mouse_x <= (x * 5.7) + 64 and y * 4 <= mouse_y <= y * 4 + square_size * 0.9:
                                                                    game.board[row][col] = "n" if turn == "white" else "N"
                                                                    waiting = False


                                        game.board[new_row][new_col] = game.board[row][col]
                                        game.board[row][col] = ""

                                        turn = "white" if turn == "black" else "black"
                                        game_end_state = chess_moves.game_end_chcek(game.board, my_color, game.castling, turn, game.en_passant) # this shows end window after one of the players is mated or stalemated
                                        if game_end_state[2] != None:
                                            who_won = "white" if turn == "black" else "black"
                                            posible_moves = []
                                            game.draw_board()
                                            game.draw_pieces()
                                            game.game_ended(game_end_state[2], who_won)
                                            waiting = True
                                            while waiting:
                                                for event in pygame.event.get():
                                                    if event.type == pygame.QUIT:
                                                        pygame.quit()
                                                        raise SystemExit

                                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                                        mouse_x, mouse_y = event.pos
                                                        x, y = square_size, square_size
                                                        if square_size * 3.5 <= mouse_x <= square_size * 3.5 + (
                                                                square_size * 2) and square_size * 5.2 <= mouse_y <= square_size * 5.2 + (
                                                                square_size * 0.75):
                                                            waiting = False
                                                            # need to add better returnning to menu like reshaping window
                                                            menu.menu_gui()
                                                            game_running = False

                                        posible_moves = []
                                        moving_pieces = []
                                        game.last_move = [(row, col), (new_row, new_col)]
                                        game.draw_board()
                                        game.draw_pieces()
                                        break

                            if not move_made:
                                game.draw_board()
                                game.draw_pieces()


                elif two_players == True and turn != my_color:  # 2 players
                    if True:  # AI turn (against AI)
                        ia_move = chess_bot.ai(game.board, turn, my_color, game.en_passant, game.castling)
                        turn = "white" if turn == "black" else "black"
                        row, col = ia_move[1][0][0], ia_move[1][0][1]

                        if game.board[row][col] in ("K", "k", "R", "r"):  # if you move a king or a rook u cant use it for castling
                            if game.board[row][col] in ("K", "k"):
                                if game.board[row][col] == "k":
                                    for state in game.castling["white"]:
                                        game.castling["white"][state] = False
                                else:
                                    for state in game.castling["black"]:
                                        game.castling["black"][state] = False


                            elif game.board[row][col] in ("R", "r"):  # this will be activated if rook is moved and castling will not be posible with it
                                if game.board[row][col] == "r":
                                    if col == 0 and row == 0:
                                        game.castling["white"]["Rook-L"] = False
                                    elif col == 7 and row == 0:
                                        game.castling["white"]["Rook-R"] = False

                                else:
                                    if col == 0 and row == 7:
                                        game.castling["black"]["Rook-L"] = False
                                    elif col == 7 and row == 7:
                                        game.castling["black"]["Rook-R"] = False

                        row, col, new_row, new_col = ia_move[1][0][0], ia_move[1][0][1], ia_move[1][1][0], ia_move[1][1][1]
                        game.board[new_row][new_col] = game.board[row][col]
                        game.board[row][col] = ""
                        game.last_move = [(row, col), (new_row, new_col)]

                        if game.board[new_row][new_col].lower() == "k" and abs(new_col - col) > 1:
                            if new_col < col:
                                game.board[row][new_col + 1] = game.board[row][0]
                                game.board[row][0] = ""
                            else:
                                game.board[row][new_col - 1] = game.board[row][7]
                                game.board[row][7] = ""


                        move_info = ia_move[1][1]
                        if len(move_info) == 3 and move_info[2] == "en_passant_move":
                            game.board[row][new_col] = ""


                        if game.board[new_row][new_col].lower() == "p" and abs(new_row - row) == 2: # saves that ai used 2 tile move of pawn it is for en passant
                            game.en_passant = [True, new_row, new_col]
                        else:
                            game.en_passant = [False]


                        game_end_state = chess_moves.game_end_chcek(game.board, my_color, game.castling, turn, game.en_passant)  # this shows end window after one of the players is mated or stalemated
                        if game_end_state[2] != None:
                            who_won = "white" if turn == "black" else "black"
                            posible_moves = []
                            game.draw_board()
                            game.draw_pieces()
                            game.game_ended(game_end_state[2], who_won)
                            waiting = True
                            while waiting:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        raise SystemExit

                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mouse_x, mouse_y = event.pos
                                        x, y = square_size, square_size
                                        if square_size * 3.5 <= mouse_x <= square_size * 3.5 + (
                                                square_size * 2) and square_size * 5.2 <= mouse_y <= square_size * 5.2 + (
                                                square_size * 0.75):
                                            waiting = False
                                            # need to add better returnning to menu like reshaping window
                                            menu.menu_gui()
                                            game_running = False

                        game.draw_board()
                        game.draw_pieces()

                    elif True:  # another player turn (against another player online)
                        pass

# made by: rokrerum