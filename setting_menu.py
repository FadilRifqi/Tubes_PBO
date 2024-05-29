import pygame
import json
from menu import Menu
from button import Button
from slider import Slider

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700 

class SettingMenu(Menu):
    def __init__(self):
        super().__init__()
        # Inisialisasi atribut khusus Main Menu

    def display(self,menu,game):
        # tampilan untuk main menu
        volume_slider = Slider(pos=(50, SCREEN_HEIGHT - 400), width=SCREEN_WIDTH-100, height=30, min_value=0, max_value=1,initial_value=game._settings['volume'])
        volume_slider.set_value(game._settings["volume"])
        setting_text = self.get_font(35).render("SETTING", True, "White")
        setting_rect = setting_text.get_rect(center=(SCREEN_WIDTH/2, 50))
        volume_text = self.get_font(25).render('VOLUME', True, 'White')
        volume_text_rect = volume_text.get_rect(center=(SCREEN_WIDTH/2, 240))
        if game.difficulty == 0:
            difficulty_text = self.get_font(25).render("EASY", True, "White")
            difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
        elif game.difficulty == 1:
            difficulty_text = self.get_font(25).render("NORMAL", True, "White")
            difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
        elif game.difficulty == 2:
            difficulty_text = self.get_font(25).render("HARD", True, "White")
            difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
        
        run = True
        dragging = False 
        while run:
            menu.intro_music.set_volume(game._settings['volume'])
            menu_mouse_pos = pygame.mouse.get_pos()
            # menginisiasi button untuk main menu
            about_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2-105, SCREEN_HEIGHT-230), 
                                text_input="ABOUT", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            back_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2+105, SCREEN_HEIGHT-230), 
                                text_input="BACK", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            # Tombol untuk mengganti karakter
            prevdifficulty_button = Button(image=pygame.transform.smoothscale(pygame.image.load("graphics/Button Rect.png"),(60,25)), pos=(SCREEN_WIDTH/2-100, SCREEN_HEIGHT-550),
                                text_input="<", font=self.get_font(25), base_color="Black", hovering_color="#baf4fc")
            nextdifficulty_button = Button(image=pygame.transform.smoothscale(pygame.image.load("graphics/Button Rect.png"),(60,25)), pos=(SCREEN_WIDTH/2+100, SCREEN_HEIGHT-550),
                                text_input=">", font=self.get_font(25), base_color="Black", hovering_color="#baf4fc")

            # menampilkan ke layar
            self._screen.blit(intro_bg, (0, 0))
            self._screen.blit(setting_text, setting_rect)
            self._screen.blit(difficulty_text, difficulty_rect)
            self._screen.blit(volume_text, volume_text_rect)
            volume_slider.draw(self._screen)

            # update button
            for button in [back_button,nextdifficulty_button,prevdifficulty_button,about_button]:
                button.change_color(menu_mouse_pos,self._screen)
                button.update(self._screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # untuk mengecek apakah tombol diklik
                    if nextdifficulty_button.check_for_input(menu_mouse_pos):
                        game.difficulty = (game.difficulty + 1) % 3
                        if game.difficulty == 0:
                            difficulty_text = self.get_font(25).render("Easy", True, "White")
                            game._settings["difficulty"] = "easy"
                        elif game.difficulty == 1:
                            difficulty_text = self.get_font(25).render("Normal", True, "White")
                            game._settings["difficulty"] = "normal"
                        elif game.difficulty == 2:
                            difficulty_text = self.get_font(25).render("Hard", True, "White")
                            game._settings["difficulty"] = "hard"
                        difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))

                    if prevdifficulty_button.check_for_input(menu_mouse_pos):
                        game.difficulty = (game.difficulty - 1) % 3
                        if game.difficulty == 0:
                            difficulty_text = self.get_font(45).render("Easy", True, "White")
                            game._settings["difficulty"] = "easy"
                        elif game.difficulty == 1:
                            difficulty_text = self.get_font(45).render("Normal", True, "White")
                            game._settings["difficulty"] = "normal"
                        elif game.difficulty == 2:
                            difficulty_text = self.get_font(45).render("Hard", True, "White")
                            game._settings["difficulty"] = "hard"
                        difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))

                         
                    if volume_slider.check_for_input(menu_mouse_pos):
                        dragging = True
                        volume_slider.update_value(menu_mouse_pos)
                        game._settings["volume"] = volume_slider.get_value()
                        
                    if about_button.check_for_input(menu_mouse_pos):
                        run = False
                        game.about_menu.display(game)
                    if back_button.check_for_input(menu_mouse_pos):
                        run = False
                        with open('setting.json', 'w') as file:
                            json.dump(game._settings, file) 
                        game.main_menu.display(game)
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False

            if dragging:
                # Ambil posisi x mouse dan sesuaikan nilai volume berdasarkan posisi tersebut
                newvolume = (menu_mouse_pos[0] - volume_slider.rect.left) / volume_slider.rect.width
                # Batasi nilai volume antara 0 dan 1
                newvolume = max(0, min(1, newvolume))
                volume_slider.set_value(newvolume)
                game._settings['volume'] = newvolume

            pygame.display.update()

intro_bg = pygame.image.load('graphics/intro_bg.png').convert_alpha()
intro_bg = pygame.transform.smoothscale(intro_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))