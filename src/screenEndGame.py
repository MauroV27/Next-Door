import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ScreensController
from src.gameManager import ImagePath
from src.utils.screen import Screen
from src.screenMenu import Button


class EndGame(Screen):
    def __init__(self, screen, param=None) -> None:
        super().__init__(screen, "game-screen")

        print("Params em end game: ", param)

        self.scores = param

        self.next_screen = [ScreensController.MENU, ScreensController.GAME]

        # Fonts in game menu:
        self.button_font = pygame.font.SysFont('Calibri', 24, True, False)
        self.score_label = pygame.font.SysFont('Calibri', 32, True, False)

        # Image in screen
        self.image_to_render = pygame.image.load(ImagePath.simple_room).convert()

        # load buttons :
        buttons_size = [160, 40]

        self.BTN_back_to_menu = Button("Back to menu", [SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + 10], buttons_size, self.call_signal, self.next_screen[0])
        self.BTN_restart_game = Button("Restart game", [SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + 90], buttons_size, self.call_signal, self.next_screen[1])


    def show_text(self, screen, text, font, c_x, c_y, color=(12, 12, 12)) -> None:
        _text = font.render(text, True, color)
        _text_rect = _text.get_rect(center= (c_x, c_y))
        screen.blit(_text, _text_rect)

    
    def input(self):

        for event in pygame.event.get():
            self.quit_screen(event)

        self.BTN_back_to_menu.button_input()
        self.BTN_restart_game.button_input()

    
    def render(self, screen) -> None:

        self.screen.fill((0,0,0))

        self.screen.blit(self.image_to_render, (0,0))

        # render text :
        self.show_text(screen, f'Scores: {self.scores}', self.score_label, SCREEN_WIDTH/2, 80)

        # render buttons :
        self.BTN_back_to_menu.draw_button(screen, self.button_font)
        self.BTN_restart_game.draw_button(screen, self.button_font)




