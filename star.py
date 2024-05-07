import pygame
from item import Item
from random import randint

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

class Star(Item):
    def __init__(self,x_character,y_character):
        super().__init__('star',None)
        for i in range(2,11):
         self._frames.append(pygame.image.load('graphics/star/{}.png'.format(i)).convert_alpha())
        self._frames = [pygame.transform.smoothscale(image, (69, 63)) for image in self._frames]
        self._frame_index = 0

        self.x_character = x_character
        self.y_character = y_character
        self.image = self._frames[self._frame_index]
        self.rect = self.image.get_rect(bottomright = (randint(1350, 1500), randint(60, SCREEN_HEIGHT)))
        self._last_frameupdate = pygame.time.get_ticks()  # Waktu terakhir animasi diperbarui

        # Penundaan antara perubahan frame (ms)
        self._animation_delay = 100  # Misalnya, 100 ms

    # animasi star
    def animation_state(self):
        self._frame_index += 0.1
        if self._frame_index >= len(self._frames):
            self._frame_index = 0
        self.image = self._frames[int(self._frame_index)]

    # menghapus star jika sudah keluar layar
    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= self._vel
        self.destroy()