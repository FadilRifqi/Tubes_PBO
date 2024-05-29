import pygame
from player import Player
from main_menu import MainMenu
from main_game import MainGame
from game_over_menu import GameOverMenu
from setting_menu import SettingMenu
from pause_menu import PauseMenu
from about_menu import AboutMenu


SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
FPS = 60

class Game:
    def __init__(self):
        self._character = 0
        self._settings = {"difficulty": "normal", "volume": 0.5,"character":{"2":"locked","3":"locked"}}
        # game object setup
        self._player = pygame.sprite.GroupSingle(Player(self._character))
        self._meteor = pygame.sprite.Group()
        self._star = pygame.sprite.Group()
        self._cloud = pygame.sprite.Group()
        self._magnet = pygame.sprite.Group()
        self.main_menu = MainMenu()
        self.main_game = MainGame()
        self.game_over = GameOverMenu()
        self.setting_menu = SettingMenu()
        self.pause_menu = PauseMenu()
        self.about_menu = AboutMenu()
        # game condition and score
        self.x_pos = self._player.sprite.rect.x
        self.y_pos = self._player.sprite.rect.y
        self.game_active = False
        self.setting_active = False
        self.pause = False
        self.is_magnet_active = False
        self.score = 0
        self.high_score = 0
        self.background = 0
        self.magnet_duration = 0
        self.difficulty = 1
        self.volume = 1
        self.coin = 0

    # menjalankan game
    def run(self):
        self.main_menu.display(self)

# game run
game = Game()
game.run()