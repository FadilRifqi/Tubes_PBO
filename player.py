import pygame

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

# class player mempunyai parent class sprite 
class Player(pygame.sprite.Sprite):
    def __init__(self,character):
        super().__init__()
        #enkapsulasi start
        self._player_frames = []
        self._character = character
        #enkapsulasi end
        self.update_character()
        if character == 0:
            for i in range(1, 11):
                self._player_frames.append(pygame.image.load('graphics/player/naga_1/{}.png'.format(i)).convert_alpha())
        elif character == 1:
            for i in range(1, 11):
                self._player_frames.append(pygame.image.load('graphics/player/naga_2/{}.png'.format(i)).convert_alpha())
        else:
            for i in range(1, 11):
                self._player_frames.append(pygame.image.load('graphics/player/naga_3/{}.png'.format(i)).convert_alpha())
        self._player_frames = [pygame.transform.smoothscale(image, (95, 70)) for image in self._player_frames]
        self._player_frame_index = 0
        
        self.image = self._player_frames[self._player_frame_index]
        self.rect = self.image.get_rect(midbottom = (200, (SCREEN_HEIGHT/2)))

        self._active_time = 0

        self._ready = True

    def player_input(self):
        # pergerakan player sesuai input keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

            
    # batasan pergerakan player di layar game
    def player_constraint(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    # animasi player saat terbang
    def animation_state(self):
        self._player_frame_index += 0.1
        if self._player_frame_index >= len(self._player_frames):
            self._player_frame_index = 0
        self.image = self._player_frames[int(self._player_frame_index)]
            

    def update(self):
        self.player_input()
        self.player_constraint()
        self.animation_state()

    def update_character(self):
        self._player_frames = []
        if self._character == 0:
            for i in range(1, 11):
                self._player_frames.append(pygame.image.load('graphics/player/naga_1/{}.png'.format(i)).convert_alpha())
        elif self._character == 1:
            for i in range(1, 11):
                self._player_frames.append(pygame.image.load('graphics/player/naga_2/{}.png'.format(i)).convert_alpha())
        else:
            for i in range(1, 11):
                self._player_frames.append(pygame.image.load('graphics/player/naga_3/{}.png'.format(i)).convert_alpha())
        self._player_frames = [pygame.transform.smoothscale(image, (110, 75)) for image in self._player_frames]
        self._player_frame_index = 0
        self.image = self._player_frames[self._player_frame_index]
        self.rect = self.image.get_rect(midbottom=(200, (SCREEN_HEIGHT / 2)))
        
    def change_character(self, new_character):
        self._character = new_character
        self.update_character()
