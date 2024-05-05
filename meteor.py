import pygame
from item import Item
from random import randint

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

class Meteor(Item):
    def __init__(self,background):
        super().__init__('meteor')
        self._meteor_frames = []
        self._rand_int = randint(1,2)
        if(background == 0):
            for i in range(1, 4):
                self._meteor_frames.append(pygame.image.load('graphics/meteor/meteor_1.png').convert_alpha())
                self._meteor_frames = [pygame.transform.smoothscale(image, (120, 25)) for image in self._meteor_frames]
        else:
            for i in range(1, 4):
                self._meteor_frames.append(pygame.image.load('graphics/meteor/meteor_2.png').convert_alpha())
                self._meteor_frames = [pygame.transform.smoothscale(image, (150, 45)) for image in self._meteor_frames]
        self._meteor_frame_index = 0
        
        self.image = self._meteor_frames[self._meteor_frame_index]
        self.rect = self.image.get_rect(bottomright = (randint(1350, 1500), randint(50, SCREEN_HEIGHT)))
        self._vel = randint(4, 7)

    # animasi meteor
    def animation_state(self):
        self._meteor_frame_index += 1
        if self._meteor_frame_index >= len(self._meteor_frames):
            self._meteor_frame_index = 0
        self.image = self._meteor_frames[self._meteor_frame_index]

    # menghapus meteor jika sudah keluar layar
    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= self._vel
        self.destroy()