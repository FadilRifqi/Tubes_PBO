import pygame
from random import randint
from abc import ABC,abstractmethod 
    

class Item(pygame.sprite.Sprite,ABC):
    def __init__(self,name):
        super().__init__()
        self._name = name
        self._frames = []
        self._frame_index = 0
        self._vel = randint(4, 7)

      
    @abstractmethod
    def update():
        pass
    @abstractmethod
    def destroy():        
        pass
    @abstractmethod
    def animation_state():
        pass
    