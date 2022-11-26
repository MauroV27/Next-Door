import pygame, sys

class Screen:
    # Class base for screens
    def __init__(self, screen, param=None) -> None:
        self.screen = screen
        self.param = param

    def input(self):
        for event in pygame.event.get():
            self.quit_screen(event)

    def quit_screen(self, event:pygame.event.Event):
        'Method for quit game'
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def update(self, delta):
        pass

    def render(self, screen):
        pass

    def define_signal(self, signal_func):
        self.signal = signal_func

    def call_signal(self, next_screen, param=None):
        """nex_screen -> next screen in game and param represent any param that be passed for the next screen"""
        (self.signal)(next_screen, param)