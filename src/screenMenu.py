import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ScreensController
from src.utils.screen import Screen

class Button:
    def __init__(self, _text, pos, size, call_action, func_param=None):
        self.button_text = _text
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.rect.center = (pos[0], pos[1])
        self.button_color = (200, 200, 200)
        self.text_color = (20, 20, 20)

        self.pressed_action = call_action
        self.func_param = func_param

    def button_input(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.mouse_hover()

            if pygame.mouse.get_pressed()[0]:
                self.button_pressed()
        else:
            self.mouse_is_overt()

    def mouse_hover(self):
        self.button_color = (40, 40, 40)
        self.text_color = (220, 220, 220)

    def mouse_is_overt(self):
        self.button_color = (200, 200, 200)
        self.text_color = (20, 20, 20)

    def button_pressed(self):
        self.pressed_action(self.func_param)

    def draw_button(self, screen, font):
        pygame.draw.rect(screen, self.button_color, [self.rect.x, self.rect.y, self.rect.width, self.rect.height])

        self.text = font.render( str(self.button_text), True, self.text_color)
        self.text_rect = self.text.get_rect(center = self.rect.center)
        screen.blit(self.text, self.text_rect)



class Menu(Screen):
    def __init__(self, screen, param=None) -> None:
        super().__init__(screen, "menu-screen")

        self.next_screen = [ScreensController.GAME]

        # Fonts in game menu:
        self.font_title = pygame.font.SysFont('Calibri', 48, True, False)
        self.font_normal = pygame.font.SysFont('Calibri', 24, True, False)
        self.font_authour = pygame.font.SysFont('Calibri', 14, True, False)

        buttons_size = [120, 40]

        self.button_start_game = Button("Start", [SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + 60], buttons_size, self.call_signal, self.next_screen[0])


    def input(self):

        for event in pygame.event.get():
            self.quit_screen(event)

        self.button_start_game.button_input()


    def render(self, screen):
        self.screen.fill((0,0,0))

        self.title = self.font_title.render("Next Door", True, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-90))
        self.screen.blit(self.title, self.title_rect)

        self.menu_text = self.font_normal.render("Click in button to start game", True, (255, 255, 255))
        self.menu_text_rect = self.menu_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-40))
        self.screen.blit(self.menu_text, self.menu_text_rect)

        self.button_start_game.draw_button(screen, self.font_normal)

        self.text = self.font_authour.render( "Game Made by Mauro Victor ©2022", True, (160, 160, 160))
        self.text_rect = self.text.get_rect(center=( SCREEN_WIDTH/2, SCREEN_HEIGHT - 20))
        self.screen.blit(self.text, self.text_rect)
