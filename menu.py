import pygame
from abc import ABC,abstractmethod 

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700 

pygame.init()
pygame.display.set_caption('DRAGON METEOR STORM')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Menu():
    SCREEN_WIDTH = SCREEN_WIDTH
    SCREEN_HEIGHT = SCREEN_HEIGHT 
    FPS = 60
    def __init__(self):
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    
    @abstractmethod
     # untuk mendapatkan font
    def get_font(self, size):
        return pygame.font.Font("font/DalekPinpointBold.ttf", size)

    @abstractmethod
    def display(self):
        pass