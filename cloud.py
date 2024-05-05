import pygame
from item import Item
from random import randint

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

class Cloud(Item):
    def __init__(self,background):
        super().__init__('cloud')
        self._cloud_frames = []
        self._rand_int = randint(1,2)
        if(background == 0):
            for i in range(1, 4):
                self._cloud_frames.append(pygame.image.load('graphics/clouds/cloud{}.png'.format(i)).convert_alpha())
        else:
            for i in range(1, 4):
                self._cloud_frames.append(pygame.image.load('graphics/clouds/cloud_dark_{}.png'.format(i)).convert_alpha())
        self._cloud_frames = [pygame.transform.smoothscale(image, (95, 63)) for image in self._cloud_frames]
        self._cloud_frame_index = 0

        self.image = self._cloud_frames[self._cloud_frame_index]
        self.rect = self.image.get_rect(bottomright = (randint(1350, 1500), randint(60, SCREEN_HEIGHT)))

    # animasi cloud
    def animation_state(self):
        self._cloud_frame_index += 0.1
        if self._cloud_frame_index >= len(self._cloud_frames):
            self._cloud_frame_index = 0
        self.image = self._cloud_frames[int(self._cloud_frame_index)]

    # menghapus cloud jika sudah keluar layar
    
    def destroy(self):
        if self.rect.left <= -100:
            self.kill()
    
    def update(self):
        self.animation_state()
        self.rect.move_ip(-5, 0)
        self.destroy()