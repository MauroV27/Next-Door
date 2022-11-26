SCREEN_WIDTH = 640 # 960
SCREEN_HEIGHT = 360 # 540

FPS = 60 # unit => frames / second
MS_PER_UPDATE = 1000 / FPS # unit => millisecond / frame

class ScreensController:
    """ Enum for controller main screns of game"""
    MENU : int = 1
    GAME : int = 2
    END : int = 3