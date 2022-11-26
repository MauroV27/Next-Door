from src.components.room import Room

class Door:
    def __init__(self, pos_x, pos_y, to_room:Room|None) -> None:
        
        self.x, self.y = (pos_x, pos_y)
        self.size = (90, 200)

        self.__room = to_room

    def get_room(self) -> Room|None:
        return self.__room

    def set_room(self, to_room:Room|None) -> None:
        self.__room = to_room

    def point_collide_with_rect(self, px, py) -> bool:
        
        _col_x = ( self.x < px < self.x + self.size[0] )
        _col_y = ( self.y < py < self.y + self.size[1] )

        return _col_x and _col_y