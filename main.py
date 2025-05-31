import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
import multiplayer
import chess


class Game:
    def __init__(self):
        self.board = [
            ["r"],["h"],["b"],["k"],["q"],["b"],["h"],["r"], #white
            ["p"],["p"],["p"],["p"],["p"],["p"],["p"],["p"],
            [ ],[ ],[ ],[ ],[ ],[ ],[ ],[ ],
            [ ],[ ],[ ],[ ],[ ],[ ],[ ],[ ],
            [ ],[ ],[ ],[ ],[ ],[ ],[ ],[ ],
            [ ],[ ],[ ],[ ],[ ],[ ],[ ],[ ],
            ["P"],["P"],["P"],["P"],["P"],["P"],["P"],["P"],
            ["R"],["H"],["B"],["K"],["Q"],["B"],["H"],["R"], #Black
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
        self.menu.add.button('Play ai', Menu_gui.start_the_game_singleplayer)
        self.menu.add.button('Play multiplayer', Menu_gui.start_the_game_multiplayer)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu.mainloop(self.surface)
        
        
    def start_the_game_singleplayer() -> None:
        print(f'{user_name.get_value()}, Do the job here!')
        game_interface_var = game_gui()
        game_interface_var.game_interface()
        
    def start_the_game_multiplayer() -> None:
        print(f'{user_name.get_value()}, Do the job here!')
        game_interface_var = game_gui()
        game_interface_var.game_interface()
        
        
class game_gui:
    def __init__(self):
        self.game = Game()
        #self.board = chess.Board(self.game.board)
        
    def game_interface(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))


if __name__ == "__main__":
    menu = Menu_gui()
    menu.menu_gui()
    
    gamee = game_gui()
    gamee.game_gui()
