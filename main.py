import pygame
from settings import *

from src.screenMenu import Menu
from src.screenGame import GameScreen

class Game:
    "Basic class for game init and runnig"
    def __init__(self) -> None:
        # Object with all game states
        self.states = {}

        # 'Pointer' to currently state in Object states
        self.game_state = None
        
        # Initialize all objects for game
        pygame.init()

        self.screen = pygame.display.set_mode(( SCREEN_WIDTH, SCREEN_HEIGHT ))
        pygame.display.set_caption("Next Door") # Show game name in window space

        # self.font_normal = pygame.font.SysFont(None, 20, True, False)

        # self.create_screen(ScreensController.START, Start)
        self.__create_screen(ScreensController.MENU, Menu)
        self.__create_screen(ScreensController.GAME, GameScreen)
        # self.create_screen(ScreensController.END, EndGame)

        self.__call_state(ScreensController.MENU)


    def __create_screen(self, state_name, state_func):
        self.states[state_name] = state_func


    def __call_state(self, new_state:int, _param=None):
        if new_state in self.states.keys():
            self.game_state = new_state
            self.reference_screen = self.states[self.game_state](self.screen, _param)

            # Abstração usando sinal ( tá meio complicado de explicar, mas funciona )
            self.reference_screen.define_signal(self.__call_state)


    def game_loop(self):
        "This is the only function that should be called outside of this class"

        self.previous = pygame.time.get_ticks()
        self.lag = 0

        while True:

            self.current = pygame.time.get_ticks()
            self.elapsed = self.current - self.previous
            self.previous = self.current
            self.lag += self.elapsed

            # code for manager user input
            self.reference_screen.input()
            
            # code for manager game update
            while self.lag >= MS_PER_UPDATE:
                self.reference_screen.update(MS_PER_UPDATE)
                self.lag -= MS_PER_UPDATE
            
            # code for render elements in screen
            self.reference_screen.render(self.screen)

            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.game_loop()