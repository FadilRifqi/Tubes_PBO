import pygame
import os
import json
from menu import Menu
from button import Button

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700 

class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        # Inisialisasi atribut khusus Main Menu
        

    def display(self,game):
        # Tampilkan elemen-elemen dari Main Menu
        if game._setting_active == False :
            self.intro_music.play(-1)
            self.intro_music.set_volume(game._settings['volume'])
        title_text = self.get_font(45).render('Dragon Meteor Storm', True, ('#cb130d'))
        title_rect = title_text.get_rect(center = (self.SCREEN_WIDTH/2, 550))
        menu_text = self.get_font(45).render("MAIN MENU", True, "White")
        menu_rect = menu_text.get_rect(center=(self.SCREEN_WIDTH/2, 300))
        name_game = self.get_font(25).render('Kelompok 8', True, 'White')
        name_game_rect = name_game.get_rect(center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT-100))
        player_stand = pygame.image.load('graphics/player/naga_1/1.png').convert_alpha()
        player_stand =  pygame.transform.rotozoom(player_stand, 0, 0.35)
        player_stand_rect = player_stand.get_rect(center = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT-550))

        run = True
        while run:
            self.difficulty_check(game)
            self.volume_check(game)
            self.intro_music.set_volume(game._settings['volume'])
            self.bg_music.set_volume(game._settings['volume'])
            self.dead_sound.set_volume(game._settings['volume'])
            self.star_sound.set_volume(game._settings['volume'])
            self.wind_sound.set_volume(game._settings['volume'])
            menu_mouse_pos = pygame.mouse.get_pos()
            # menginisiasi button untuk main menu
            play_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(self.SCREEN_WIDTH/2-105, self.SCREEN_HEIGHT/2+30), 
                                text_input="PLAY", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            quit_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(self.SCREEN_WIDTH/2+105, self.SCREEN_HEIGHT/2+30), 
                                text_input="QUIT", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            setting_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2+130), 
                                text_input="SETTING", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            # Tombol untuk mengganti karakter
            prev_character_button = Button(image=pygame.transform.smoothscale(pygame.image.load("graphics/Button Rect.png"),(120,50)), pos=(self.SCREEN_WIDTH/2-200, self.SCREEN_HEIGHT-550),
                                text_input="<", font=self.get_font(50), base_color="Black", hovering_color="#baf4fc")
            next_character_button = Button(image=pygame.transform.smoothscale(pygame.image.load("graphics/Button Rect.png"),(120,50)), pos=(self.SCREEN_WIDTH/2+200, self.SCREEN_HEIGHT-550),
                                text_input=">", font=self.get_font(50), base_color="Black", hovering_color="#baf4fc")

            # menampilkan ke layar
            self.screen.blit(intro_bg, (0, 0))
            self.screen.blit(title_text, title_rect)
            self.screen.blit(player_stand, player_stand_rect)
            self.screen.blit(menu_text, menu_rect)
            self.screen.blit(name_game, name_game_rect)

            # update button
            for button in [play_button, quit_button,next_character_button,prev_character_button,setting_button]:
                button.change_color(menu_mouse_pos)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # untuk mengecek apakah tombol diklik
                    if play_button.check_for_input(menu_mouse_pos):
                        run = False
                        self.intro_music.stop()
                        if game._pause == False:
                            game._background = 0
                            game._score = 0
                            game._magnet_duration = 0
                        game._pause = False
                        game._game_active = True
                        game.main_game.display(game)
                    if next_character_button.check_for_input(menu_mouse_pos):
                        next_character_button.is_clicked = True
                        # game._character = (game._character + 1) % 3
                        # game._player.sprite.change_character(game._character)
                        # if game._character == 0:
                        #     player_stand = pygame.image.load('graphics/player/naga_1/1.png').convert_alpha()
                        # elif game._character == 1:
                        #     player_stand = pygame.image.load('graphics/player/naga_2/1.png').convert_alpha()
                        # else:
                        #     player_stand = pygame.image.load('graphics/player/naga_3/1.png').convert_alpha()
                        # player_stand = pygame.transform.rotozoom(player_stand, 0, 0.35)
                        # player_stand_rect = player_stand.get_rect(center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT-550))
                    if prev_character_button.check_for_input(menu_mouse_pos):
                        game._character = (game._character - 1) % 3
                        game._player.sprite.change_character(game._character)
                        if game._character == 0:
                            player_stand = pygame.image.load('graphics/player/naga_1/1.png').convert_alpha()
                        elif game._character == 1:
                            player_stand = pygame.image.load('graphics/player/naga_2/1.png').convert_alpha()
                        else:
                            player_stand = pygame.image.load('graphics/player/naga_3/1.png').convert_alpha()
                        player_stand = pygame.transform.rotozoom(player_stand, 0, 0.35)
                        player_stand_rect = player_stand.get_rect(center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT-550))
                    if setting_button.check_for_input(menu_mouse_pos):
                        run = False
                        game._setting_active = True
                        game.setting_menu.display(self,game)
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        exit()
            pygame.display.update()
    def difficulty_check(self,game):
        if os.path.exists('setting.json'):
            with open('setting.json', 'r') as file:
                # menginisiasi nilai high score dari file setting.json
                setting = json.load(file)
                if setting.get('difficulty') == "easy":
                    game._difficulty = 0
                elif setting.get('difficulty') == "normal":
                    game._difficulty = 1
                elif setting.get('difficulty') == "hard" :
                    game._difficulty = 2
                else:
                    print(setting.get('difficulty'))
        else:
            #membuat file dan menulis highscore = 0
            with open('setting.json', 'a') as file:
                json.dump(self._settings, file)

intro_bg = pygame.image.load('graphics/intro_bg.png').convert_alpha()
intro_bg = pygame.transform.smoothscale(intro_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))    


