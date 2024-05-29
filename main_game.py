import pygame
import os
import math
from random import randint
from menu import Menu
from meteor import Meteor
from star import Star
from cloud import Cloud
from magnet import Magnet

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700 

#child class MainGame -> Parent class Menu
class MainGame(Menu):
    def __init__(self):
        super().__init__()  # Memanggil inisialisasi kelas dasar
        

    def display(self,game):
        # Implementasikan logika main game di sini
        if game.pause == False:
            self.bg_music.play(-1)
            self.wind_sound.play(-1)

        # game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    game.pause = True
                if game.game_active:
                    # memunculkan objek sesuai timernya
                    if not game.pause:
                        if event.type == obstacle_timer:
                            game._meteor.add(Meteor(game.background, game.difficulty))
                        if event.type == star_timer:
                            game._star.add(Star(game.x_pos, game.y_pos))
                        if event.type == cloud_timer:
                            game._cloud.add(Cloud(game.background))
                        if event.type == magnet_timer:
                            game._magnet.add(Magnet())

            if game.game_active and game.pause == False:
                # buat ability magnet hanya selama 10 detik
                if game.magnet_duration > 0:
                    game.is_magnet_active = True
                    game.magnet_duration -= 1  
                else:
                    game.is_magnet_active = False
                    game.magnet_duration = 0
                # menampilkan background sunset ketika score < 40 dan malam ketika score > 40
                if game.score > 40:
                    self._screen.blit(new_bg_surface, (0, 0))
                    game.background = 1
                else:
                    self._screen.blit(bg_surface, (0, 0))
                self.high_score_check(game)
                star_hit = pygame.sprite.spritecollide(game._player.sprite, game._star, True)
                # jika terjadi star_hit maka akan menambahkan score
                if star_hit:
                    self.star_sound.play()
                    self.add_coin(game)
                    game.score+=1
                # jika terjadi maget_hit  maka akan menarik star
                if game.is_magnet_active == True:
                    self.magnet_active(game)
                magnet_hit = pygame.sprite.spritecollide(game._player.sprite, game._magnet, True)
                if magnet_hit:
                    game.is_magnet_active = True
                    game.magnet_duration = 600
                    self.star_sound.play()
                # menjalankan semua method dari objek
                game._player.draw(self._screen)
                game._player.update()
                game._meteor.draw(self._screen)
                game._meteor.update()
                game._star.draw(self._screen)
                game._star.update()
                game._cloud.draw(self._screen)
                game._cloud.update()
                game._magnet.draw(self._screen)
                game._magnet.update()
                # menampilkan indicator dan score
                self.display_score(game)
                self.display_magnet_indicator(game)
                game.game_active = self.collision_player(game)

            elif game.game_active and game.pause:
                game.pause_menu.display(game)
            # jika game tidak aktif maka akan menampilkan game over
            else:
                # mengupdate high score
                if game.score > game.high_score:
                    game.high_score = game.score
                    with open('high_score.txt', 'w') as file:
                        file.write(str(game.high_score))

                self.bg_music.stop()
                self.wind_sound.stop()
                game.game_over.display(game)

            pygame.display.update()
            self._clock.tick(self.FPS)
    # menampilkan score di dalam game
    def display_score(self,game):
        if game.background == 0:
            score_surf = self.get_font(25).render(f'Score: {game.score}', False, ('Black'))
        else:
            score_surf = self.get_font(25).render(f'Score: {game.score}', False, ('White'))
        score_rect = score_surf.get_rect(center = ((SCREEN_WIDTH/2), 30))
        self._screen.blit(score_surf, score_rect)
    
    def display_magnet_indicator(self,game):
        # Menampilkan indikator UI untuk magnet
        magnet_image = pygame.image.load('graphics/magnet/1.png').convert_alpha()
        magnet_image = pygame.transform.scale(magnet_image, (75, 50))
        magnet_rect = magnet_image.get_rect(topleft=(10, 10))
        if game.magnet_duration > 0:
            # Hitung panjang indikator (panjang layar * (sisa waktu magnet / total waktu magnet))
            indicator_length = int((magnet_rect.width + 20) * (game.magnet_duration / 600))  
            indicator_surface = pygame.Surface((magnet_rect.width + 20, magnet_rect.height + 20), pygame.SRCALPHA)
            indicator_surface.set_alpha(128)  # Nilai alpha sekitar 50% transparan
            
            # Hitung posisi dan ukuran indikator putih berdasarkan magnet_duration
            indicator_rect = pygame.Rect(magnet_rect.left - 5, magnet_rect.top - 5, indicator_length, magnet_rect.height + 10)
            
            # Gambar indikator putih berkurang seiring waktu
            pygame.draw.rect(indicator_surface, (255, 255, 255), indicator_rect)
            
            # Gambar gambar magnet
            self._screen.blit(indicator_surface, (magnet_rect.left-5, magnet_rect.top - 10))  # Gambar indikator putih di atas magnet
            self._screen.blit(magnet_image, magnet_rect)

    # mengecek high score dari file highscore.txt
    def high_score_check(self,game):
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as file:
                # menginisiasi nilai high score dari file high_score.txt
                game.high_score = int(file.read())
        else:
            #membuat file dan menulis highscore = 0
            with open('high_score.txt', 'a') as file:
                file.write(str(0))
    # mengecek apakah terjadi collision antara player dan meteor
    def collision_player(self,game):
        # jika terjadi collision maka akan mengosongkan semua grup objek
        if pygame.sprite.spritecollide(game._player.sprite, game._meteor, False):
            with open('coin.txt', 'w') as file:
                file.write(str(game.coin))
            self.dead_sound.play()
            game._meteor.empty()
            game._star.empty()
            game._cloud.empty()
            game._player.sprite.indicator_active = False
            return False
        return True
    
    def add_coin(self,game):
        game.coin += 1
        print(game.coin)
    
    def magnet_active(self,game):
        for star in game._star:
            # Menghitung vektor antara posisi bintang dan posisi pemain
            direction_x = game._player.sprite.rect.x - star.rect.x
            direction_y = game._player.sprite.rect.y - star.rect.y
            # Menghitung jarak antara posisi bintang dan posisi pemain
            distance_x = abs(star.rect.x - game._player.sprite.rect.x)
            distance_y = abs(star.rect.y - game._player.sprite.rect.y)

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
    def stop_music(self):
        self.bg_music.stop()
        self.wind_sound.stop()
        
# timer kemunculan objek
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(1000, 1500))
star_timer = pygame.USEREVENT + 2
pygame.time.set_timer(star_timer, randint(1000, 1500))
cloud_timer = pygame.USEREVENT + 3
pygame.time.set_timer(cloud_timer, randint(2000, 2500))
magnet_timer = pygame.USEREVENT + 4
pygame.time.set_timer(magnet_timer, randint(10000, 30000))

bg_surface = pygame.image.load('graphics/background.png').convert_alpha()
bg_surface = pygame.transform.smoothscale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
new_bg_surface = pygame.image.load('graphics/background_2.png').convert_alpha()
new_bg_surface = pygame.transform.smoothscale(new_bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
