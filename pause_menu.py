import pygame
import os
import json
from menu import Menu
from button import Button

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700 

class PauseMenu(Menu):
    def __init__(self):
        super().__init__()
        # Inisialisasi atribut khusus Main Menu

    def display(self,game):
        pause_text = self.get_font(45).render('PAUSED', True, (203, 19, 13))
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        
        resume_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 
                            text_input="RESUME", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
        menu_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100), 
                            text_input="MENU", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
        run = True
        while run:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.check_for_input(mouse_pos):
                        run = False
                        game._pause = False
                        return
                    elif menu_button.check_for_input(mouse_pos):
                        game._pause = False
                        game._game_active = False
                        game._meteor.empty()
                        game._star.empty()
                        game._cloud.empty()
                        game.main_game.stop_music()
                        game._setting_active = False
                        game.main_menu.display(game)
                        

            self.screen.blit(bg_surface, (0, 0))  # Tampilkan latar belakang saat game di-pause
        
            # Tampilkan karakter dan objeknya saat game di-pause
            game._player.draw(self.screen)
            game._meteor.draw(self.screen)
            game._star.draw(self.screen)
            game._cloud.draw(self.screen)
            game._magnet.draw(self.screen)
            game.main_game.display_score(game)
            game.main_game.display_magnet_indicator(game)
            
            self.screen.blit(pause_text, pause_rect)
            for button in [resume_button, menu_button]:
                button.update(self.screen)
            pygame.display.update()
            self.clock.tick(self.FPS)

wind_sound = pygame.mixer.Sound('audio/wind.wav')
wind_sound.set_volume(0.5)
bg_surface = pygame.image.load('graphics/background.png').convert_alpha()
bg_surface = pygame.transform.smoothscale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
new_bg_surface = pygame.image.load('graphics/background_2.png').convert_alpha()
new_bg_surface = pygame.transform.smoothscale(new_bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_music = pygame.mixer.Sound('audio/game.mp3')
bg_music.set_volume(0.5)