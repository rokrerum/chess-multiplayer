import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
import multiplayer
import chess
import time


class Game:
    def __init__(self):
        self.board = [
            [["r"],["n"],["b"],["k"],["q"],["b"],["n"],["r"]], #white
            [["p"],["p"],["p"],["p"],["p"],["p"],["p"],["p"]],
            [[ ],[ ],[ ],[ ],[ ],[ ],[ ],[ ]],
            [[ ],[ ],[ ],[ ],[ ],[ ],[ ],[ ]],
            [[ ],[ ],[ ],[ ],[ ],[ ],[ ],[ ]],
            [[ ],[ ],[ ],[ ],[ ],[ ],[ ],[ ]],
            [["P"],["P"],["P"],["P"],["P"],["P"],["P"],["P"]],
            [["R"],["N"],["B"],["K"],["Q"],["B"],["N"],["R"]], #Black
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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    

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
        self.menu.add.button('Play ai', self.start_the_game_singleplayer)
        self.menu.add.button('Play multiplayer', self.start_the_game_multiplayer)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu.enable()
        self.menu.mainloop(self.surface)
        
        
        
    def start_the_game_singleplayer() -> None:
        print(f'{user_name.get_value()}, Do the job here!')
        game_interface_var = game_gui()
        pygame_menu.events.CLOSE
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

        
    def game_interface(self):
        pygame.init()
        screen = pygame.display.set_mode((900, 600))
        game = Game()
        for i in range(1,9): #this for lups are for drawing the board 
            for j in range(1,9):
                board_square = game.places[i-1][j-1]
                if board_square.color == "white":
                    pygame.draw.rect(screen, (255, 255, 255), (j*80, i*80, 80, 80)) #(rect_x, rect_y, rect_width, rect_height)
                else:
                    pygame.draw.rect(screen, (222, 0, 0), (j*80, i*80, 80, 80))
            
        
        pygame.display.update()
        
        for i in range(0,8): #this for lups are for drawing pieces on the board 
            for j in range(0,8):
                
                if str(game.board[i][j]).upper() == "p":
                    if (game.board[i][j]).isupper():
                        pygame.draw.circle(screen, (0, 0, 0), (j*80 + i*80, 40,  40), 30)
                    else:
                        pygame.draw.circle(screen, (255, 255, 255), (j*80 + 40, i*80 + 40), 30)  
                if str(game.board[i][j]).upper() == "r":
                    pygame.draw.circle(screen, (0, 0, 0), (j*80 + 40, i*80 + 40), 30)
                elif str(game.board[i][j]).upper() == "n":
                    pygame.draw.circle(screen, (0, 0, 0), (j*80 + 40, i*80 + 40), 30)
                elif str(game.board[i][j]).upper() == "b":
                    pygame.draw.circle(screen, (0, 0, 0), (j*80 + 40, i*80 + 40), 30)
                elif str(game.board[i][j]).upper() == "k":
                    pygame.draw.circle(screen, (0, 0, 0), (j*80 + 40, i*80 + 40), 30)
                elif str(game.board[i][j]).upper() == "q":
                    pygame.draw.circle(screen, (0, 0, 0), (j*80 + 40, i*80 + 40), 30)
                        
        pygame.display.update()
        
        #game runing###########################
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        col = mouse_x // 80
                        row = mouse_y // 80
                        
                        print(f"Kliknięto na pole ({col}, {row})")

                        # Sprawdź czy kliknięto na figurę
                        #if (row, col) == piece_pos:
                        #    dragging = True
                        #    offset_x = mouse_x - (col * SQUARE_SIZE + SQUARE_SIZE // 2)

if __name__ == "__main__":
    menu = Menu_gui()
    menu.menu_gui()
