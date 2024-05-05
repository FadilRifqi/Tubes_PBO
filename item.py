import pygame
from abc import ABC,abstractmethod 
    

class Item(pygame.sprite.Sprite,ABC):
    def __init__(self,name):
        super().__init__()
        self._name = name
      
    @abstractmethod
    def update():
        pass
    def destroy():        
        pass
    def animation_state():
        pass
    