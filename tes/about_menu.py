import pygame
from menu import Menu
from button import Button

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700 

class AboutMenu(Menu):
    def __init__(self):
        super().__init__()

    def display(self,game):

        run = True
        while run:
            menu_mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(about_bg,(0,0))
            back_button = Button(image=pygame.transform.smoothscale(pygame.image.load("graphics/Button Rect.png"),(100,50)), pos=(60, 40), 
                                text_input="<-", font=self.get_font(30), base_color="Black", hovering_color="#baf4fc")
            for button in [back_button]:
                button.change_color(menu_mouse_pos,self.screen)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.check_for_input(menu_mouse_pos):
                        run = False 
                        game.setting_menu.display(self,game)
            
            pygame.display.update()

                

about_bg = pygame.image.load('graphics/about_bg.png').convert_alpha()
about_bg = pygame.transform.smoothscale(about_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))