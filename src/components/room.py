class Room:
    "Class that represent the nodes/vertex of graph."

    def __init__(self, image, color, value:int=0, level:int=0) -> None:
        self.image_link = image
        self.base_color = color #format (r, g, b)
        self.room_number = value
        
        # used in graph algorithm to model the 'map' of game
        # level A < level B
        self.level = level

    
