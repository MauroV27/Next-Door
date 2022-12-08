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

        self.next_screen = [ScreensController.MENU, ScreensController.END]

        self.game = GameManager()
        self.game.generate_rooms( 33, 0.12) # best values : 11

        self.game.set_callback(self.final_screen)

        # [DEBUG][TEST]
        self.game.print_game_map()

        # Fonts in game menu:
        self.number_room = pygame.font.SysFont('Calibri', 24, True, False)
        self.door_letter = pygame.font.SysFont('Calibri', 64, True, False)

        # Game State: 
        self.state = RoomStates.NORMAL

        # Image in screen
        self.image_to_render = None
        self.update_image_in_screen()

        # room value space
        self.bg_room_value = pygame.Surface((60, 30))
        self.bg_room_value.fill((220, 220, 220))


    def input(self):

        for event in pygame.event.get():
            self.quit_screen(event)

            if event.type == pygame.MOUSEBUTTONUP:
                self.state = RoomStates.NORMAL

            # Return to menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.call_signal(ScreensController.MENU)


        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        
        if self.game.currently_room != None:
            if pygame.mouse.get_pressed()[0] and self.state == RoomStates.NORMAL:

                _go_to = self.game.validate_collisions( mouse_x, mouse_y )

                print('cliquei!, vou para: ', _go_to) #[DEBUG][EXCLUDE]

                self.state = RoomStates.TRANSITION

                self.game.change_room(_go_to)
                self.update_image_in_screen()



    def show_text(self, screen, text, font, c_x, c_y, color=(12, 12, 12)) -> None:
        _text = font.render(text, True, color)
        _text_rect = _text.get_rect(center= (c_x, c_y))
        screen.blit(_text, _text_rect)


    def update_image_in_screen(self) -> None:
        image = self.game.currently_room.image_link
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(self.game.currently_room.base_color)
        
        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)

        self.image_to_render = finalImage


    def render(self, screen) -> None:

        self.screen.fill((0,0,0))

        # render colored room
        self.screen.blit(self.image_to_render, (0,0))

        ## render doors (with text)
        _door_counter : int = 0
        for door in self.game.get_doors().values():
            if door.get_room_index() == None:
                continue

            pygame.draw.rect(self.screen, (2, 2, 2), (door.x, door.y, door.size[0], door.size[1]))
            _letter = ['A', 'B', 'C'][_door_counter]
            _letter_pos = [door.x + door.size[0]/2, door.y + door.size[1]/2]
            self.show_text(screen, _letter, self.door_letter, _letter_pos[0], _letter_pos[1], color=(200, 200, 200))
            _door_counter += 1
            

        ## render room id/value
        self.screen.blit(self.bg_room_value, (SCREEN_WIDTH/2-30, 65))
        self.show_text(screen, str(self.game.get_room_number()), self.number_room, SCREEN_WIDTH/2, 80)

    
    def final_screen(self):
        print('Game end')
        print('Número de portas abertas até chegar ao final: ', self.game.get_attempts())
        self.call_signal(ScreensController.END, self.game.get_attempts())