import pygame
import os.path as path
from random import randint

from src.components.room import Room
from src.components.room import Door

class ImagePath:
    # Load path of folder and adjust for any absolute path  
    __main_path : str = path.dirname(path.abspath(__file__))

    simple_room :str = __main_path + "\\assets\\room_basic_area.png"

class GameManager:

    def __init__(self) -> None:
        
        # using list (__rooms) to store all rooms of the game
        # and use graph to manager connections : [__rooms[index]] = {go:[int, int, int], back:[*int]}
        # every room have values (doors) pointing out to a index (with outher room) in list
        self.__rooms = []
        self.__graph = {}

        self.first_room : Room 
        self.last_room : Room  
        self.currently_room : Room 

        self.doors = {
            "A" : Door(120, 115, None),
            "B" : Door(275, 115, None),
            "C" : Door(430, 115, None)
        }

    def generate_rooms(self, num_rooms:int, chance_2_doors:float):

        # if num_rooms < 0 or num_rooms is not int:
        #     raise ValueError('number of rooms must be a positive integer.')

        # if chance_2_doors < 0 or chance_2_doors > 1:
        #     raise ValueError('chance of two doors rooms must be a float number btw 0 and 1.')

        img1 = pygame.image.load(ImagePath.simple_room).convert()

        # Create nodes/edges in graph
        for i in range(num_rooms):
            _create_basic_room = Room(img1, (245, 180, 200), i)
            self.insert_room( _create_basic_room )

        # Create connectiosn btw rooms (doors)
        # [ISSUE] : implement possibility to generate only 2 doors
        self.generate_connectiosn_btw_rooms()

        # sort rooms in map
        # self.sort_rooms()

        self.first_room = self.__rooms[0] # [TEMP][DEBUG]
        self.currently_room_index = 0
        self.currently_room = self.first_room # get first room in graph

        
    def get_doors(self) -> dict:
        return self.doors


    def update_doors_link(self):
        
        __link_to = self.__graph[self.currently_room_index]['GO_TO']

        self.doors["A"].set_room_index( __link_to[0] )
        self.doors["B"].set_room_index( __link_to[1] )
        self.doors["C"].set_room_index( __link_to[2] )
        


    def validate_collisions(self, px, py) -> int|None:    

        for door in self.doors.values():
            if door.point_collide_with_rect(px, py):
                return door.get_room_index()  

        return None


    def change_room(self, next_room:int|None) -> None:
        if next_room != None:
            if 0 < next_room < len(self.__rooms):
                self.currently_room_index = next_room
                self.currently_room = self.__rooms[next_room]
                self.update_doors_link()


    def insert_room(self, room:Room) -> None:
        self.__rooms.append(room)

        __last_index = len(self.__rooms) - 1

        self.__graph[__last_index] = {
            'GO_TO' : [None, None, None],        # go to index[0] or index[1] or index[2]
            'COMES' : []                        # comes from any nodes, just need be different to go to index 
        }
 
    def generate_connectiosn_btw_rooms(self) -> None:
        # Create connections btw nodes/edges
        _room_index = 0

        __size_graph : int = len(self.__rooms) - 1

        for _ in self.__rooms:
            # [ISSUE] : implement possibility to generate only 2 doors
            _selected_index = []
            while len(_selected_index) < 3:
                _target_index = randint(0, __size_graph)

                if _target_index == _room_index or _target_index in _selected_index:
                    continue
                else:
                    _selected_index.append(_target_index)
                    
                    # room.set_door(len(_selected_index) - 1, to_room=_target_index)

                    # [DOCUMENT]
                    # intern_levle < --> first appear in game
                    # room.intern_level -= 1
                    # self.__graph[ _target_index ].intern_level += 1
            else:
                print('a: ', _room_index, ' --> ', _selected_index)
                self.__graph[_room_index]['GO_TO'] = _selected_index

            _room_index += 1


    def sort_rooms(self) -> None:

        _first_room = self.__graph[0]   #Room('', (), 0)
        _last_room = self.__graph[0]    #Room('', (), 0)
        
        _room_index = 0

        for room in self.__graph:

            room.room_number = _room_index

            if room.intern_level < _first_room.intern_level:
                _first_room = room
                __temp = _first_room.room_number
                _first_room.room_number = room.room_number
                room.room_number = __temp + 1

            if room.intern_level > _last_room.intern_level:
                _last_room = room
                __temp = _last_room.room_number
                _last_room.room_number = room.room_number + 1
                room.room_number = __temp

            _room_index = 1

        self.first_room = _first_room
        self.last_room = _last_room

    def print_game_map(self):

        # print ( room number,  doors(A:index, B:index, C:index), level)

        _result :dict = {}
        _room_index = 0

        for room in self.__rooms:
            _doors = {
                "A" : self.__graph[_room_index]['GO_TO'][0],
                "B" : self.__graph[_room_index]['GO_TO'][1],
                "C" : self.__graph[_room_index]['GO_TO'][2]
            }

            _result[ _room_index ] = [_doors, room.intern_level, room.room_number]
            
            _room_index += 1

        print("Map of rooms: ")
        for i in _result:
            print('Sala :', i, '| ', _result[i][2], " |--> ", _result[i][0], '| level: ', _result[i][1])