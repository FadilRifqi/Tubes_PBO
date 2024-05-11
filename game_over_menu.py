import pygame
from menu import Menu
from button import Button

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700 


class GameOverMenu(Menu):
    def __init__(self):
        super().__init__()

    def display(self,game):
        game_over_music.play()
        # tampilan untuk game over
        game_over_message = self.get_font(45).render('Game Over', True, (203,19,13))
        game_over_message_rect = game_over_message.get_rect(center = ((SCREEN_WIDTH/2), SCREEN_HEIGHT/3-120))
        score_massage = self.get_font(35).render(f'Your score: {game._score}', True, ('White'))
        score_massage_rect = score_massage.get_rect(center = ((SCREEN_WIDTH/2), SCREEN_HEIGHT/3-65))
        high_score_message = self.get_font(25).render(f'High score: {game._high_score}', True, ('White'))
        high_score_message_rect = high_score_message.get_rect(center = ((SCREEN_WIDTH/2), SCREEN_HEIGHT/5-100))
        if game._character == 0 :
            player_dead = pygame.image.load('graphics/player/dead.png').convert_alpha()
            player_dead = pygame.transform.rotozoom(player_dead, 0, 0.45)
        elif game._character == 1:
            player_dead = pygame.image.load('graphics/player/dead_2.png').convert_alpha()
            player_dead = pygame.transform.rotozoom(player_dead, 0, 0.45)
        elif game._character == 2:
            player_dead = pygame.image.load('graphics/player/dead_3.png').convert_alpha()
            player_dead = pygame.transform.rotozoom(player_dead, 0, 0.45)      
        player_dead_rect = player_dead.get_rect(center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2-90)))

        run = True
        while run:
            game_over_music.set_volume(game._settings['volume'])
            menu_mouse_pos = pygame.mouse.get_pos()
            # menginisiasi button untuk Game Over
            play_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT-300), 
                                text_input="PLAY", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            menu_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT-200), 
                                text_input="MENU", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            quit_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT-100), 
                                text_input="QUIT", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            
            for event in pygame.event.get():    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.check_for_input(menu_mouse_pos):
                        run = False
                        if game._pause == False:
                            game._background = 0
                            game._score = 0
                            game._magnet_duration = 0
                        game._pause = False
                        game._game_active = True
                        game_over_music.stop()
                        game.main_game.display(game)
                    if menu_button.check_for_input(menu_mouse_pos):
                        run = False
                        game_over_music.stop()
                        game._score = 0
                        game._background = 0
                        game._setting_active = False
                        game.main_menu.display(game)
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        exit()
           
            # untuk menampilkan ke layar
            self.screen.blit(game_over_bg, (0, 0))
            self.screen.blit(game_over_message, game_over_message_rect)
            self.screen.blit(score_massage, score_massage_rect)
            self.screen.blit(high_score_message, high_score_message_rect)
            self.screen.blit(player_dead, player_dead_rect)
            # update button
            for button in [play_button, quit_button,menu_button]:
                button.change_color(menu_mouse_pos,self.screen)
                button.update(self.screen)

            pygame.display.update()

game_over_bg = pygame.image.load('graphics/game_over_bg.png').convert_alpha()
game_over_bg = pygame.transform.smoothscale(game_over_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_music = pygame.mixer.Sound('audio/game_over.mp3')
