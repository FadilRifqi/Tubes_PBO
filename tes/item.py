import pygame
from random import randint
from abc import ABC,abstractmethod 
    

class Item(pygame.sprite.Sprite,ABC):
    def __init__(self,name,difficulty = None):
        super().__init__()
        self._name = name
        self._frames = []
        self._frame_index = 0
        if difficulty == 0 or difficulty == None:
            self._vel = randint(4, 7)
        elif difficulty == 1:
            self._vel = randint(7, 11)
        elif difficulty == 2:
            self._vel = randint(11, 15)
            

      
    @abstractmethod
    def update():
        pass
    @abstractmethod
    def destroy():        
        pass
    @abstractmethod
    def animation_state():
        pass
    