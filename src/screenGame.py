import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ScreensController
from src.utils.screen import Screen
from src.gameManager import GameManager


class RoomStates:
    """Enum for manager states in game"""
    NORMAL = 1
    TRANSITION = 2


class GameScreen(Screen):
    def __init__(self, screen, param=None) -> None:
        super().__init__(screen, "game-screen")

        self.next_screen = [ScreensController.MENU, ScreensController.MENU]

        self.game = GameManager()
        self.game.generate_rooms( 6, 0.12)

        # [DEBUG][TEST]
        self.game.print_game_map()

        # Fonts in game menu:
        self.font = pygame.font.SysFont('Calibri', 24, True, False)

        # Game State: 
        self.state = RoomStates.NORMAL


    def input(self):

        for event in pygame.event.get():
            self.quit_screen(event)

            if event.type == pygame.MOUSEBUTTONUP:
                self.state = RoomStates.NORMAL


        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        
        if self.game.currently_room != None:
            if pygame.mouse.get_pressed()[0] and self.state == RoomStates.NORMAL:

                _go_to = self.game.validate_collisions( mouse_x, mouse_y )

                print('cliquei!, vou para: ', _go_to) #[DEBUG][EXCLUDE]

                self.state = RoomStates.TRANSITION

                self.game.change_room(_go_to)



    def show_text(self, screen, valor, c_x, c_y) -> None:
        text = self.font.render(valor, True, (12, 12, 12))
        text_rect = text.get_rect(center= (c_x, c_y))
        screen.blit(text, text_rect)


    def render(self, screen) -> None:

        self.screen.fill((0,0,0))
        # self.game.currently_room.image_link.fill( self.game.currently_room.base_color )
        self.screen.blit(self.game.currently_room.image_link, (0,0))

        ## render doors
        for door in self.game.get_doors().values():
            pygame.draw.rect(self.screen, (2, 2, 2), (door.x, door.y, door.size[0], door.size[1]))

        ## render room id/value
        self.show_text(screen, str(self.game.currently_room.room_number), SCREEN_WIDTH/2, 80)