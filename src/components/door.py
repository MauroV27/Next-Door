class Door:
    "Class that represent the edges in graph. Connect 2 vertex/nodes."

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