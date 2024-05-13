import pygame
from item import Item
from random import randint

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

class Meteor(Item):
    def __init__(self,background,difficulty):
        super().__init__('meteor',difficulty)
        if(background == 0):
            for i in range(1, 4):
                self._frames.append(pygame.image.load('graphics/meteor/meteor_1.png').convert_alpha())
                self._frames = [pygame.transform.smoothscale(image, (120, 25)) for image in self._frames]
        else:
            for i in range(1, 4):
                self._frames.append(pygame.image.load('graphics/meteor/meteor_2.png').convert_alpha())
                self._frames = [pygame.transform.smoothscale(image, (150, 45)) for image in self._frames]
        self._frame_index = 0
        
        self.image = self._frames[self._frame_index]
        self.rect = self.image.get_rect(bottomright = (randint(1350, 1500), randint(50, SCREEN_HEIGHT)))

    # animasi meteor
    def animation_state(self):
        self._frame_index += 1
        if self._frame_index >= len(self._frames):
            self._frame_index = 0
        self.image = self._frames[self._frame_index]

    # menghapus meteor jika sudah keluar layar
    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= self._vel
        self.destroy()