import pygame
import os
from sys import exit
from random import randint
from player import Player
from meteor import Meteor
from star import Star
from cloud import Cloud
from button import Button

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
FPS = 60





class Game:
    def __init__(self):
        # game object setup
        self._character = 0
        player_sprite = Player(self._character)
        self._player = pygame.sprite.GroupSingle(player_sprite)
        self._meteor = pygame.sprite.Group()
        self._star = pygame.sprite.Group()
        self._cloud = pygame.sprite.Group()

        # game condition and score
        self._game_active = False
        self._pause = False
        self._score = 0
        self._high_score = 0
        self._player_color = (255, 255, 255)
        self._background = 0

    # untuk mendapatkan font
    def get_font(self, size):
        return pygame.font.Font("font/DalekPinpointBold.ttf", size)
        
    # menampilkan score di dalam game
    def display_score(self):
        if self._background == 0:
            score_surf = self.get_font(25).render(f'Score: {self._score}', False, ('Black'))
        else:
            score_surf = self.get_font(25).render(f'Score: {self._score}', False, ('White'))
        score_rect = score_surf.get_rect(center = ((SCREEN_WIDTH/2), 30))
        screen.blit(score_surf, score_rect)

    # mengecek high score dari file highscore.txt
    def high_score_check(self):
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as file:
                # menginisiasi nilai high score dari file high_score.txt
                self._high_score = int(file.read())
        else:
            #membuat file dan menulis highscore = 0
            with open('high_score.txt', 'a') as file:
                file.write(str(0))
    # mengecek apakah terjadi collision antara player dan meteor
    def collision_player(self):
        # jika terjadi collision maka akan mengosongkan semua grup objek
        if pygame.sprite.spritecollide(self._player.sprite, self._meteor, False):
            dead_sound.play()
            self._meteor.empty()
            self._star.empty()
            self._cloud.empty()
            self._player.sprite.indicator_active = False
            return False
        return True


    # main game
    def main_game(self):
        bg_music.play(-1)
        wind_sound.play(-1)
        # game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if self._game_active:
                    # memunculkan objek sesuai timernya
                    if event.type == obstacle_timer:
                        self._meteor.add(Meteor(self._background))
                    if event.type == star_timer:
                        self._star.add(Star())
                    if event.type == cloud_timer:
                        self._cloud.add(Cloud(self._background))

            if self._game_active:
                if self._score > 40:
                    screen.blit(new_bg_surface, (0, 0))
                    self._background = 1
                else:
                    screen.blit(bg_surface, (0, 0))
                self.high_score_check()
                star_hit = pygame.sprite.spritecollide(self._player.sprite, self._star, True)
                # jika terjadi star_hit maka akan menambahkan score
                if star_hit:
                    star_sound.play()
                    self._score+=1

                # menjalankan semua method dari objek
                self._player.draw(screen)
                self._player.update()
                self._meteor.draw(screen)
                self._meteor.update()
                self._star.draw(screen)
                self._star.update()
                self._cloud.draw(screen)
                self._cloud.update()
                # menampilkan indicator dan score
                self.display_score()
                self._game_active = self.collision_player()


            # jika game tidak aktif maka akan menampilkan game over
            else:
                # mengupdate high score
                if self._score > self._high_score:
                    self._high_score = self._score
                    with open('high_score.txt', 'w') as file:
                        file.write(str(self._high_score))

                bg_music.stop()
                wind_sound.stop()
                self.game_over()

            pygame.display.update()
            clock.tick(FPS)

    # menampilkan game over screen
    def game_over(self):
        game_over_music.play()
        # tampilan untuk game over
        game_over_message = self.get_font(45).render('Game Over', True, (203,19,13))
        game_over_message_rect = game_over_message.get_rect(center = ((SCREEN_WIDTH/2), SCREEN_HEIGHT/3-120))
        score_massage = self.get_font(35).render(f'Your score: {self._score}', True, ('White'))
        score_massage_rect = score_massage.get_rect(center = ((SCREEN_WIDTH/2), SCREEN_HEIGHT/3-65))
        high_score_message = self.get_font(25).render(f'High score: {self._high_score}', True, ('White'))
        high_score_message_rect = high_score_message.get_rect(center = ((SCREEN_WIDTH/2), SCREEN_HEIGHT/5-100))
        if self._character == 0 :
            player_dead = pygame.image.load('graphics/player/dead.png').convert_alpha()
            player_dead = pygame.transform.rotozoom(player_dead, 0, 0.45)
        elif self._character == 1:
            player_dead = pygame.image.load('graphics/player/dead_2.png').convert_alpha()
            player_dead = pygame.transform.rotozoom(player_dead, 0, 0.45)
        elif self._character == 2:
            player_dead = pygame.image.load('graphics/player/dead_3.png').convert_alpha()
            player_dead = pygame.transform.rotozoom(player_dead, 0, 0.45)      
        player_dead_rect = player_dead.get_rect(center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2-90)))

        run = True
        while run:
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
                        self._game_active = True
                        game_over_music.stop()
                        self._score = 0
                        self.main_game()
                    if menu_button.check_for_input(menu_mouse_pos):
                        run = False
                        game_over_music.stop()
                        self._score = 0
                        self.main_menu()
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        exit()
           
            # untuk menampilkan ke layar
            screen.blit(game_over_bg, (0, 0))
            screen.blit(game_over_message, game_over_message_rect)
            screen.blit(score_massage, score_massage_rect)
            screen.blit(high_score_message, high_score_message_rect)
            screen.blit(player_dead, player_dead_rect)
            # update button
            for button in [play_button, quit_button,menu_button]:
                button.change_color(menu_mouse_pos)
                button.update(screen)

            pygame.display.update()

    # menampilkan main menu
    def main_menu(self):
        intro_music.play(-1)
        # tampilan untuk main menu
        title_text = self.get_font(45).render('Dragon Meteor Storm', True, ('#cb130d'))
        title_rect = title_text.get_rect(center = (SCREEN_WIDTH/2, 550))
        menu_text = self.get_font(45).render("MAIN MENU", True, "White")
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2, 300))
        name_game = self.get_font(25).render('Kelompok 8', True, 'White')
        name_game_rect = name_game.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-100))
        player_stand = pygame.image.load('graphics/player/naga_1/1.png').convert_alpha()
        player_stand =  pygame.transform.rotozoom(player_stand, 0, 0.35)
        player_stand_rect = player_stand.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
        
        
        run = True
        while run:
            menu_mouse_pos = pygame.mouse.get_pos()
            # menginisiasi button untuk main menu
            play_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2-105, SCREEN_HEIGHT/2+30), 
                                text_input="PLAY", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            quit_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2+105, SCREEN_HEIGHT/2+30), 
                                text_input="QUIT", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            setting_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+130), 
                                text_input="SETTING", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            # Tombol untuk mengganti karakter
            prev_character_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2-250, SCREEN_HEIGHT-550),
                                text_input="<", font=self.get_font(50), base_color="Black", hovering_color="#baf4fc")
            next_character_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2+250, SCREEN_HEIGHT-550),
                                text_input=">", font=self.get_font(50), base_color="Black", hovering_color="#baf4fc")

            # menampilkan ke layar
            screen.blit(intro_bg, (0, 0))
            screen.blit(title_text, title_rect)
            screen.blit(player_stand, player_stand_rect)
            screen.blit(menu_text, menu_rect)
            screen.blit(name_game, name_game_rect)

            # update button
            for button in [play_button, quit_button,next_character_button,prev_character_button,setting_button]:
                button.change_color(menu_mouse_pos)
                button.update(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # untuk mengecek apakah tombol diklik
                    if play_button.check_for_input(menu_mouse_pos):
                        run = False
                        intro_music.stop()
                        self._game_active = True
                        self.main_game()
                    if next_character_button.check_for_input(menu_mouse_pos):
                        self._character = (self._character + 1) % 3
                        self._player.sprite.change_character(self._character)
                        if self._character == 0:
                            player_stand = pygame.image.load('graphics/player/naga_1/1.png').convert_alpha()
                        elif self._character == 1:
                            player_stand = pygame.image.load('graphics/player/naga_2/1.png').convert_alpha()
                        else:
                            player_stand = pygame.image.load('graphics/player/naga_3/1.png').convert_alpha()
                        player_stand = pygame.transform.rotozoom(player_stand, 0, 0.35)
                        player_stand_rect = player_stand.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
                    if prev_character_button.check_for_input(menu_mouse_pos):
                        self._character = (self._character - 1) % 3
                        self._player.sprite.change_character(self._character)
                        if self._character == 0:
                            player_stand = pygame.image.load('graphics/player/naga_1/1.png').convert_alpha()
                        elif self._character == 1:
                            player_stand = pygame.image.load('graphics/player/naga_2/1.png').convert_alpha()
                        else:
                            player_stand = pygame.image.load('graphics/player/naga_3/1.png').convert_alpha()
                        player_stand = pygame.transform.rotozoom(player_stand, 0, 0.35)
                        player_stand_rect = player_stand.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        exit()

            pygame.display.update()
    
    def setting_menu():
        run = True
        while(run):
            exit()
        pass

    # menjalankan game
    def run(self):
        self.main_menu()

# inisiasi game
pygame.init()
pygame.display.set_caption('DRAGON METEOR STORM')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# timer kemunculan objek
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(1000, 1500))
star_timer = pygame.USEREVENT + 2
pygame.time.set_timer(star_timer, randint(1000, 1500))
cloud_timer = pygame.USEREVENT + 3
pygame.time.set_timer(cloud_timer, randint(2000, 2500))

# game additonal setup
bg_surface = pygame.image.load('graphics/background.png').convert_alpha()
bg_surface = pygame.transform.smoothscale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
new_bg_surface = pygame.image.load('graphics/background_2.png').convert_alpha()
new_bg_surface = pygame.transform.smoothscale(new_bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
intro_bg = pygame.image.load('graphics/intro_bg.png').convert_alpha()
intro_bg = pygame.transform.smoothscale(intro_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_bg = pygame.image.load('graphics/game_over_bg.png').convert_alpha()
game_over_bg = pygame.transform.smoothscale(game_over_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# audio setup
bg_music = pygame.mixer.Sound('audio/game.mp3')
bg_music.set_volume(0.5)
intro_music = pygame.mixer.Sound('audio/main_menu.mp3')
intro_music.set_volume(0.5)
game_over_music = pygame.mixer.Sound('audio/game_over.mp3')
game_over_music.set_volume(0.5)
star_sound = pygame.mixer.Sound('audio/star.wav')
star_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound('audio/explosion.flac')
explosion_sound.set_volume(0.5)
dead_sound = pygame.mixer.Sound('audio/dead.mp3')
dead_sound.set_volume(0.5)
wind_sound = pygame.mixer.Sound('audio/wind.wav')
wind_sound.set_volume(0.5)

# game run
game = Game()
game.run()