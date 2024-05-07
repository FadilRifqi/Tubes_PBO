import pygame
import json
from menu import Menu
from button import Button

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700 

class SettingMenu(Menu):
    def __init__(self):
        super().__init__()
        # Inisialisasi atribut khusus Main Menu

    def display(self,game):
        # tampilan untuk main menu
        setting_text = self.get_font(45).render("Setting", True, "White")
        setting_rect = setting_text.get_rect(center=(SCREEN_WIDTH/2, 50))
        name_game = self.get_font(25).render('Kelompok 8', True, 'White')
        name_game_rect = name_game.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-100))
        if game._difficulty == 0:
            difficulty_text = self.get_font(45).render("Easy", True, "White")
            difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
        elif game._difficulty == 1:
            difficulty_text = self.get_font(45).render("Normal", True, "White")
            difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
        elif game._difficulty == 2:
            difficulty_text = self.get_font(45).render("Hard", True, "White")
            difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
        
        run = True
        while run:

            menu_mouse_pos = pygame.mouse.get_pos()
            # menginisiasi button untuk main menu
            back_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT-200), 
                                text_input="BACK", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            # Tombol untuk mengganti karakter
            prev_difficulty_button = Button(image=pygame.transform.smoothscale(pygame.image.load("graphics/Button Rect.png"),(120,50)), pos=(SCREEN_WIDTH/2-150, SCREEN_HEIGHT-550),
                                text_input="<", font=self.get_font(50), base_color="Black", hovering_color="#baf4fc")
            next_difficulty_button = Button(image=pygame.transform.smoothscale(pygame.image.load("graphics/Button Rect.png"),(120,50)), pos=(SCREEN_WIDTH/2+150, SCREEN_HEIGHT-550),
                                text_input=">", font=self.get_font(50), base_color="Black", hovering_color="#baf4fc")

            # menampilkan ke layar
            self.screen.blit(intro_bg, (0, 0))
            self.screen.blit(setting_text, setting_rect)
            self.screen.blit(difficulty_text, difficulty_rect)
            self.screen.blit(name_game, name_game_rect)

            # update button
            for button in [back_button,next_difficulty_button,prev_difficulty_button]:
                button.change_color(menu_mouse_pos)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(game._difficulty,game._settings["difficulty"])
                    # untuk mengecek apakah tombol diklik
                    if next_difficulty_button.check_for_input(menu_mouse_pos):
                        game._difficulty = (game._difficulty + 1) % 3
                        if game._difficulty == 0:
                            difficulty_text = self.get_font(45).render("Easy", True, "White")
                            game._settings["difficulty"] = "easy"
                        elif game._difficulty == 1:
                            difficulty_text = self.get_font(45).render("Normal", True, "White")
                            game._settings["difficulty"] = "normal"
                        elif game._difficulty == 2:
                            difficulty_text = self.get_font(45).render("Hard", True, "White")
                            game._settings["difficulty"] = "hard"
                        difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))

                    if prev_difficulty_button.check_for_input(menu_mouse_pos):
                        game._difficulty = (game._difficulty - 1) % 3
                        if game._difficulty == 0:
                            difficulty_text = self.get_font(45).render("Easy", True, "White")
                            game._settings["difficulty"] = "easy"
                        elif game._difficulty == 1:
                            difficulty_text = self.get_font(45).render("Normal", True, "White")
                            game._settings["difficulty"] = "normal"
                        elif game._difficulty == 2:
                            difficulty_text = self.get_font(45).render("Hard", True, "White")
                            game._settings["difficulty"] = "hard"
                        difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))

                    if back_button.check_for_input(menu_mouse_pos):
                        run = False
                        with open('setting.json', 'w') as file:
                            json.dump(game._settings, file) 
                        game.main_menu.display(game)

            pygame.display.update()

intro_bg = pygame.image.load('graphics/intro_bg.png').convert_alpha()
intro_bg = pygame.transform.smoothscale(intro_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))