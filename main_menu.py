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
        self.character = True
        self.is_coin_enough = True
        

    def display(self,game):
        # Tampilkan elemen-elemen dari Main Menu
        if game.setting_active == False :
            self.intro_music.play(-1)
            self.intro_music.set_volume(game._settings['volume'])
        title_text = self.get_font(45).render('Dragon Meteor Storm', True, ('#cb130d'))
        title_rect = title_text.get_rect(center = (self.SCREEN_WIDTH/2, 550))
        unlocked_text = self.get_font(30).render('Locked', True, ('White'))
        unlocked_rect = unlocked_text.get_rect(center = (self.SCREEN_WIDTH/2, 50))
        is_coin_text = self.get_font(30).render('Coin Not Enough', True, ('White'))
        is_coin_rect = is_coin_text.get_rect(center = (self.SCREEN_WIDTH/2, 50))
        menu_text = self.get_font(45).render("MAIN MENU", True, "White")
        menu_rect = menu_text.get_rect(center=(self.SCREEN_WIDTH/2, 300))
        name_game = self.get_font(25).render('Kelompok 8', True, 'White')
        name_game_rect = name_game.get_rect(center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT-100))
        coin_image = pygame.image.load('graphics/star/2.png').convert_alpha()
        coin_image = pygame.transform.rotozoom(coin_image, 0, 0.25)
        coin_image_rect = coin_image.get_rect(center = (50, 50))
        
        run = True
        while run:  
            if game._character == 0:
                player_stand = pygame.image.load('graphics/player/naga_1/1.png').convert_alpha()
            elif game._character == 1:
                if game._settings['character']['2'] == "locked":
                    player_stand = pygame.image.load('graphics/player/naga_2/locked.png').convert_alpha()
                else:
                    player_stand = pygame.image.load('graphics/player/naga_2/1.png').convert_alpha()
            else:
                if game._settings['character']['3'] == "locked":
                    player_stand = pygame.image.load('graphics/player/naga_3/locked.png').convert_alpha()
                else:
                    player_stand = pygame.image.load('graphics/player/naga_3/1.png').convert_alpha()
            player_stand = pygame.transform.rotozoom(player_stand, 0, 0.35)
            player_stand_rect = player_stand.get_rect(center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT-550))
            self.check_character(game)
            self.check_coin(game)  
            coin_text = self.get_font(25).render(str(game.coin), True, ("White"))
            coin_rect = coin_text.get_rect(center = (100, 50))
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
            unlock_button = Button(image=None, pos=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT-490),
                                    text_input="Unlock", font=self.get_font(15), base_color="White", hovering_color="#baf4fc")

            # menampilkan ke layar
            self._screen.blit(intro_bg, (0, 0))
            self._screen.blit(title_text, title_rect)
            self._screen.blit(player_stand, player_stand_rect)
            self._screen.blit(menu_text, menu_rect)
            self._screen.blit(name_game, name_game_rect)
            self._screen.blit(coin_text, coin_rect)
            self._screen.blit(coin_image, coin_image_rect)
            if self.character == False:
                self._screen.blit(unlocked_text, unlocked_rect)
            if self.is_coin_enough == False:
                self._screen.blit(is_coin_text, is_coin_rect)

            # update button
            if game._settings['character']['2'] == "locked" and game._character == 1:
                unlock_button.update(self._screen)
            if game._settings['character']['3'] == "locked" and game._character == 2:
                unlock_button.update(self._screen)

            for button in [play_button, quit_button,next_character_button,prev_character_button,setting_button]:
                button.change_color(menu_mouse_pos,self._screen)
                button.update(self._screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # untuk mengecek apakah tombol diklik
                    if play_button.check_for_input(menu_mouse_pos):
                        if game._character == 1 and game._settings['character']['2'] == "locked":
                            self.is_coin_enough = True
                            self.character = False
                        if game._character == 2 and game._settings['character']['3'] == "locked":
                            self.is_coin_enough = True
                            self.character = False
                        if game._character == 0 or self.character == True: 
                            run = False
                            self.intro_music.stop()
                            self.is_coin_enough = True
                            self.character = True
                            if game.pause == False:
                                game.background = 0
                                game.score = 0
                                game.magnet_duration = 0
                            game.pause = False
                            game.game_active = True
                            game.main_game.display(game)

                    if next_character_button.check_for_input(menu_mouse_pos):
                        self.is_coin_enough = True
                        self.character = True
                        next_character_button.is_clicked = True
                        game._character = (game._character + 1) % 3
                        game._player.sprite.change_character(game._character)
                        if game._character == 0:
                            player_stand = pygame.image.load('graphics/player/naga_1/1.png').convert_alpha()
                        elif game._character == 1:
                            if game._settings['character']['2'] == "locked":
                                player_stand = pygame.image.load('graphics/player/naga_2/locked.png').convert_alpha()
                            else:
                                player_stand = pygame.image.load('graphics/player/naga_2/1.png').convert_alpha()
                        else:
                            if game._settings['character']['3'] == "locked":
                                player_stand = pygame.image.load('graphics/player/naga_3/locked.png').convert_alpha()
                            else:
                                player_stand = pygame.image.load('graphics/player/naga_3/1.png').convert_alpha()
                        player_stand = pygame.transform.rotozoom(player_stand, 0, 0.35)
                        player_stand_rect = player_stand.get_rect(center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT-550))
                    if prev_character_button.check_for_input(menu_mouse_pos):
                        self.is_coin_enough = True
                        self.character = True
                        game._character = (game._character - 1) % 3
                        game._player.sprite.change_character(game._character)
                        if game._character == 0:
                            player_stand = pygame.image.load('graphics/player/naga_1/1.png').convert_alpha()
                        elif game._character == 1:
                            if game._settings['character']['2'] == "locked":
                                player_stand = pygame.image.load('graphics/player/naga_2/locked.png').convert_alpha()
                            else:
                                player_stand = pygame.image.load('graphics/player/naga_2/1.png').convert_alpha()
                        else:
                            if game._settings['character']['3'] == "locked":
                                player_stand = pygame.image.load('graphics/player/naga_3/locked.png').convert_alpha()
                            else:
                                player_stand = pygame.image.load('graphics/player/naga_3/1.png').convert_alpha()
                        player_stand = pygame.transform.rotozoom(player_stand, 0, 0.35)
                        player_stand_rect = player_stand.get_rect(center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT-550))
                    if setting_button.check_for_input(menu_mouse_pos):
                        run = False
                        game.setting_active = True
                        game.setting_menu.display(self,game)
                    if unlock_button.check_for_input(menu_mouse_pos):
                        if game._character == 1:
                            self.unlock_character(game,1)
                        elif game._character == 2:
                            self.unlock_character(game,2)
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        exit()
            pygame.display.update()

    def unlock_character(self,game,character):
        if character == 1:
            if game.coin >= 50:
                game.coin -= 50
                game._settings['character']['2'] = "unlocked"
                with open('coin.txt', 'w') as file:
                    file.write(str(game.coin))
            else:
                self.character = True
                self.is_coin_enough = False
        elif character == 2:
            if game.coin >= 50:
                game.coin -= 50
                game._settings['character']['3'] = "unlocked"
                with open('coin.txt', 'w') as file:
                    file.write(str(game.coin))
            else:
               self.character = True
               self.is_coin_enough = False
        with open('setting.json', 'w') as file:
                json.dump(game._settings, file)

    def check_character(self,game):
        if os.path.exists('setting.json'):
            with open('setting.json', 'r') as file:
                character = json.load(file)
                game._settings['character']['2'] = character.get('character').get('2')
                game._settings['character']['3'] = character.get('character').get('3')
        else:
             with open('setting.json', 'a') as file:
                json.dump(game._settings, file)

    def check_coin(self,game):
        if os.path.exists('coin.txt'):
            with open('coin.txt','r') as file:
                game.coin = int(file.read())
        else:
           with open('coin.txt', 'a') as file:
                file.write(str(0))
                 
    def difficulty_check(self,game):
        if os.path.exists('setting.json'):
            with open('setting.json', 'r') as file:
                # menginisiasi nilai high score dari file setting.json
                setting = json.load(file)
                if setting.get('difficulty') == "easy":
                    game.difficulty = 0
                elif setting.get('difficulty') == "normal":
                    game.difficulty = 1
                elif setting.get('difficulty') == "hard" :
                    game.difficulty = 2
                else:
                    print(setting.get('difficulty'))
        else:
            #membuat file dan menulis highscore = 0
            with open('setting.json', 'a') as file:
                json.dump(game._settings, file)

intro_bg = pygame.image.load('graphics/intro_bg.png').convert_alpha()
intro_bg = pygame.transform.smoothscale(intro_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))    


