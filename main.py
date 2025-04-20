import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
import multiplayer
import chess


class game:
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


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Szachy Online")
        
    def start_the_game() -> None:
        global user_name
        print(f'{user_name.get_value()}, Do the job here!')
        
        
class Menu:
    def __init__(self):
        self.surface = create_example_window('Example - Simple', (600, 400))
        self.menu = pygame_menu.Menu(
            height=300,
            theme=pygame_menu.themes.THEME_BLUE,
            title='Welcome',
            width=400
        )

    def menu_creation(self):
        user_name = self.menu.add.text_input('Name: ', default='John Doe', maxchar=10)
        self.menu.add.button('Play', Main.start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu.mainloop(self.surface)



if __name__ == "__main__":
    menu = Menu()
    menu.menu_creation()
