# from src.components.door import Door

class Room:
    "Class that represent the nodes/vertex of graph."

    def __init__(self, image, color, value:int=0) -> None:
        self.image_link = image
        self.base_color = color #format (r, g, b)
        self.room_number = value
        
        # used in graph algorithm to model the 'map' of game
        # level A < level B
        self.intern_level = 0

    #     self.doors = {
    #         "A" : Door(120, 115, None),
    #         "B" : Door(275, 115, None),
    #         "C" : Door(430, 115, None)
    #     }

    # def set_door(self, door:int, to_room:int) -> None:
    #     "@params: door only can be 'A', 'B' or 'C'."

    #     _door = ["A", "B", "C"][door]

    #     # if to_room is int:
    #     self.doors[_door].set_room(to_room)

    # def get_door(self, door:str) :
    #     if door is ("A", "B", "C"):
    #         return self.doors[door].get_room()

    
class Door:
    "Class that represent the edge in graph. Connect 2 nodes."

    def __init__(self, pos_x, pos_y, to_room:int|None) -> None:
        
        self.x, self.y = (pos_x, pos_y)
        self.size = (90, 200)

        self.__room_index :int|None = to_room


    def get_room_index(self) -> int|None:
        return self.__room_index


    def set_room_index(self, to_room:int|None) -> None:
        self.__room_index = to_room

    def point_collide_with_rect(self, px, py) -> bool:
        
        _col_x = ( self.x < px < self.x + self.size[0] )
        _col_y = ( self.y < py < self.y + self.size[1] )

        return _col_x and _col_y

    def __repr__(self) -> str:
        return f'Door({self.x}, {self.y}, {self.__room_index})'