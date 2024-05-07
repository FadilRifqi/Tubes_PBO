import pygame
import os
import math
from sys import exit
from random import randint
from player import Player
from meteor import Meteor
from star import Star
from cloud import Cloud
from button import Button
from magnet import Magnet

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
        self._magnet = pygame.sprite.Group()
        self.x_pos = self._player.sprite.rect.x
        self.y_pos = self._player.sprite.rect.y
        # game condition and score
        self._game_active = False
        self._setting_active = False
        self._pause = False
        self._is_magnet_active = False
        self._score = 0
        self._high_score = 0
        self._background = 0
        self._magnet_duration = 0
        self._difficulty = 1
        

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
    def difficulty_check(self):
        if os.path.exists('setting.txt'):
            with open('setting.txt', 'r') as file:
                # menginisiasi nilai high score dari file setting.txt
                setting = file.read().strip()
                if str(setting) == "easy":
                    self._difficulty = 0
                elif str(setting) == "normal":
                    self._difficulty = 1
                elif str(setting) == "hard" :
                    self._difficulty = 2
                else:
                    print(setting)
        else:
            #membuat file dan menulis highscore = 0
            with open('setting.txt', 'a') as file:
                file.write(str(1))
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
        if self._pause == False:
            bg_music.play(-1)
            wind_sound.play(-1)

        # game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    self._pause = True
                if self._game_active:
                    # memunculkan objek sesuai timernya
                    if not self._pause:
                        if event.type == obstacle_timer:
                            self._meteor.add(Meteor(self._background,self._difficulty))
                        if event.type == star_timer:
                            self._star.add(Star(self.x_pos,self.y_pos))
                        if event.type == cloud_timer:
                            self._cloud.add(Cloud(self._background))
                        if event.type == magnet_timer:
                            self._magnet.add(Magnet())

            if self._game_active and self._pause == False:
                # buat ability magnet hanya selama 10 detik
                if self._magnet_duration > 0:
                    self._is_magnet_active = True
                    self._magnet_duration -= 1  
                else:
                    self._is_magnet_active = False
                    self._magnet_duration = 0
                # menampilkan background sunset ketika score < 40 dan malam ketika score > 40
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
                # jika terjadi maget_hit  maka akan menarik star
                if self._is_magnet_active == True:
                    self.magnet_active()
                magnet_hit = pygame.sprite.spritecollide(self._player.sprite, self._magnet, True)
                if magnet_hit:
                    self._is_magnet_active = True
                    self._magnet_duration = 600
                    star_sound.play()
                # menjalankan semua method dari objek
                self._player.draw(screen)
                self._player.update()
                self._meteor.draw(screen)
                self._meteor.update()
                self._star.draw(screen)
                self._star.update()
                self._cloud.draw(screen)
                self._cloud.update()
                self._magnet.draw(screen)
                self._magnet.update()
                # menampilkan indicator dan score
                self.display_score()
                self.display_magnet_indicator()
                self._game_active = self.collision_player()

            elif self._game_active and self._pause:
                self.pause()
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

    def magnet_active(self):
        for star in self._star:
            # Menghitung vektor antara posisi bintang dan posisi pemain
            direction_x = self._player.sprite.rect.x - star.rect.x
            direction_y = self._player.sprite.rect.y - star.rect.y
            # Menghitung jarak antara posisi bintang dan posisi pemain
            distance_x = abs(star.rect.x - self._player.sprite.rect.x)
            distance_y = abs(star.rect.y - self._player.sprite.rect.y)

            # Menghitung panjang vektor
            length = math.sqrt(direction_x ** 2 + direction_y ** 2)

            # Normalisasi vektor (mengubahnya menjadi vektor satuan)
            if length != 0:
                direction_x /= length
                direction_y /= length

            # Menggerakkan bintang perlahan-lahan ke arah pemain
            if distance_x <= 200 and distance_y <= 700:
                speed = 10  # Atur kecepatan pergerakan bintang
                star.rect.x += direction_x * speed
                star.rect.y += direction_y * speed

    def display_magnet_indicator(self):
        # Menampilkan indikator UI untuk magnet
        magnet_image = pygame.image.load('graphics/magnet/1.png').convert_alpha()
        magnet_image = pygame.transform.scale(magnet_image, (75, 50))
        magnet_rect = magnet_image.get_rect(topleft=(10, 10))
        if self._magnet_duration > 0:
            # Hitung panjang indikator (panjang layar * (sisa waktu magnet / total waktu magnet))
            indicator_length = int((magnet_rect.width + 20) * (self._magnet_duration / 600))  
            indicator_surface = pygame.Surface((magnet_rect.width + 20, magnet_rect.height + 20), pygame.SRCALPHA)
            indicator_surface.set_alpha(128)  # Nilai alpha sekitar 50% transparan
            
            # Hitung posisi dan ukuran indikator putih berdasarkan magnet_duration
            indicator_rect = pygame.Rect(magnet_rect.left - 5, magnet_rect.top - 5, indicator_length, magnet_rect.height + 10)
            
            # Gambar indikator putih berkurang seiring waktu
            pygame.draw.rect(indicator_surface, (255, 255, 255), indicator_rect)
            
            # Gambar gambar magnet
            screen.blit(indicator_surface, (magnet_rect.left-5, magnet_rect.top - 10))  # Gambar indikator putih di atas magnet
            screen.blit(magnet_image, magnet_rect)
            
            
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
                        if self._pause == False:
                            self._background = 0
                            self._score = 0
                            self._magnet_duration = 0
                        self._pause = False
                        self._game_active = True
                        game_over_music.stop()
                        
                        self.main_game()
                    if menu_button.check_for_input(menu_mouse_pos):
                        run = False
                        game_over_music.stop()
                        self._score = 0
                        self._background = 0
                        self._setting_active = False
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

    # menampilkan pause menu
    def pause(self):
        pause_text = self.get_font(45).render('PAUSED', True, (203, 19, 13))
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        
        resume_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 
                            text_input="RESUME", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
        menu_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100), 
                            text_input="MENU", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if resume_button.check_for_input(mouse_pos):
                        run = False
                        self._pause = False
                        return
                    elif menu_button.check_for_input(mouse_pos):
                        self._pause = False
                        self._game_active = False
                        self._meteor.empty()
                        self._star.empty()
                        self._cloud.empty()
                        bg_music.stop()
                        wind_sound.stop()
                        self._setting_active = False
                        self.main_menu()
                        

            screen.blit(bg_surface, (0, 0))  # Tampilkan latar belakang saat game di-pause
        
            # Tampilkan karakter dan objeknya saat game di-pause
            self._player.draw(screen)
            self._meteor.draw(screen)
            self._star.draw(screen)
            self._cloud.draw(screen)
            self._magnet.draw(screen)
            self.display_score()
            self.display_magnet_indicator()
            
            screen.blit(pause_text, pause_rect)
            resume_button.update(screen)
            menu_button.update(screen)
            pygame.display.update()
            clock.tick(FPS)
    # menampilkan main menu
    def main_menu(self):
        if self._setting_active == False :
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
            self.difficulty_check()
            menu_mouse_pos = pygame.mouse.get_pos()
            # menginisiasi button untuk main menu
            play_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2-105, SCREEN_HEIGHT/2+30), 
                                text_input="PLAY", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            quit_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2+105, SCREEN_HEIGHT/2+30), 
                                text_input="QUIT", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            setting_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+130), 
                                text_input="SETTING", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            # Tombol untuk mengganti karakter
            prev_character_button = Button(image=pygame.transform.smoothscale(pygame.image.load("graphics/Button Rect.png"),(120,50)), pos=(SCREEN_WIDTH/2-200, SCREEN_HEIGHT-550),
                                text_input="<", font=self.get_font(50), base_color="Black", hovering_color="#baf4fc")
            next_character_button = Button(image=pygame.transform.smoothscale(pygame.image.load("graphics/Button Rect.png"),(120,50)), pos=(SCREEN_WIDTH/2+200, SCREEN_HEIGHT-550),
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
                        if self._pause == False:
                            self._background = 0
                            self._score = 0
                            self._magnet_duration = 0
                        self._pause = False
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
                    if setting_button.check_for_input(menu_mouse_pos):
                        run = False
                        self._setting_active = True
                        self.setting_menu()
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        exit()

            pygame.display.update()
    
    def setting_menu(self):
        # tampilan untuk main menu
        setting_text = self.get_font(45).render("Setting", True, "White")
        setting_rect = setting_text.get_rect(center=(SCREEN_WIDTH/2, 50))
        name_game = self.get_font(25).render('Kelompok 8', True, 'White')
        name_game_rect = name_game.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-100))
        if self._difficulty == 0:
            difficulty_text = self.get_font(45).render("Easy", True, "White")
            difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
        elif self._difficulty == 1:
            difficulty_text = self.get_font(45).render("Normal", True, "White")
            difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))
        elif self._difficulty == 2:
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
            screen.blit(intro_bg, (0, 0))
            screen.blit(setting_text, setting_rect)
            screen.blit(difficulty_text, difficulty_rect)
            screen.blit(name_game, name_game_rect)

            # update button
            for button in [back_button,next_difficulty_button,prev_difficulty_button]:
                button.change_color(menu_mouse_pos)
                button.update(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    # untuk mengecek apakah tombol diklik
                    if next_difficulty_button.check_for_input(menu_mouse_pos):
                        self._difficulty = (self._difficulty + 1) % 3
                        if self._difficulty == 0:
                            difficulty_text = self.get_font(45).render("Easy", True, "White")
                        elif self._difficulty == 1:
                            difficulty_text = self.get_font(45).render("Normal", True, "White")
                        elif self._difficulty == 2:
                            difficulty_text = self.get_font(45).render("Hard", True, "White")
                        difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))

                    if prev_difficulty_button.check_for_input(menu_mouse_pos):
                        self._difficulty = (self._difficulty - 1) % 3
                        if self._difficulty == 0:
                            difficulty_text = self.get_font(45).render("Easy", True, "White")
                        elif self._difficulty == 1:
                            difficulty_text = self.get_font(45).render("Normal", True, "White")
                        elif self._difficulty == 2:
                            difficulty_text = self.get_font(45).render("Hard", True, "White")
                        difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-550))

                    if back_button.check_for_input(menu_mouse_pos):
                        run = False
                        with open('setting.txt', 'w') as file:
                            if self._difficulty == 0:
                                file.write("easy")
                            elif self._difficulty == 1:
                                file.write("normal")
                            elif self._difficulty == 2:
                                file.write("hard")
                        self.main_menu()

            pygame.display.update()

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
magnet_timer = pygame.USEREVENT + 4
pygame.time.set_timer(magnet_timer, randint(10000, 30000))

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