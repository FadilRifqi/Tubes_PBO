import pygame
import os
import json
from abc import ABC,abstractmethod 

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700 

pygame.init()
pygame.display.set_caption('DRAGON METEOR STORM')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#abstraksi kelas Menu
class Menu(ABC):
    SCREEN_WIDTH = SCREEN_WIDTH
    SCREEN_HEIGHT = SCREEN_HEIGHT 
    intro_music = pygame.mixer.Sound('audio/main_menu.mp3')
    bg_music = pygame.mixer.Sound('audio/game.mp3')
    wind_sound = pygame.mixer.Sound('audio/wind.wav')
    star_sound = pygame.mixer.Sound('audio/star.wav')
    dead_sound = pygame.mixer.Sound('audio/dead.mp3')
    FPS = 60
    def __init__(self):
        pygame.init()
        #enkapsulasi start
        self._screen = screen
        self._clock = pygame.time.Clock()
        #enkapsulasi end

    #abstrak method
    @abstractmethod
    def display(self):
        pass
    
     # untuk mendapatkan font
    def get_font(self, size):
        return pygame.font.Font("font/DalekPinpointBold.ttf", size)


    def volume_check(self,game):
        if os.path.exists('setting.json'):
            with open('setting.json', 'r') as file:
                # menginisiasi nilai high score dari file setting.json
                setting = json.load(file)
                game._settings['volume'] = setting.get('volume')
                game.volume = setting.get('volume')
        else:
            #membuat file dan menulis highscore = 0
            with open('setting.json', 'a') as file:
                json.dump(game._settings, file)
        