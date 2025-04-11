import pygame
import myltiplayer
import chess


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Szachy Online")
        
a = myltiplayer.Multiplayer()

a.start()