import pygame
import os.path as path
from random import choice, random, shuffle

from src.components.room import Room
from src.components.door import Door

class ImagePath:
    # Load path of folder and adjust for any absolute path  
    __main_path : str = path.dirname(path.abspath(__file__))

    simple_room :str = __main_path + "\\assets\\room_basic_area.png"

class GameManager:

    def __init__(self) -> None:
        
        # using list (__rooms) to store all rooms of the game
        # and use graph to manager connections : [__rooms[lsit->index]] = {go:[int, int, int], back:[*int]}
        # every room have values (doors) pointing out to a index (with outher room) in list
        self.__rooms : list[Room]= []
        self.__graph : dict[int, list[int|None]] = {}

        self.currently_room : Room 
        self.currently_room_index : int = 0

        self._attempts : int = 0 # number of attempts to reach the end

        self.doors = {
            "A" : Door(120, 116, None),
            "B" : Door(275, 116, None),
            "C" : Door(430, 116, None)
        }


    def set_callback(self, callback):
        self.callback = callback

    def emit_callback(self):
        # called when player enter in last room
        (self.callback)()

    def get_attempts(self) -> int:
        return self._attempts

    def generate_rooms(self, num_rooms:int, chance_2_doors:float):

        _img1 = pygame.image.load(ImagePath.simple_room).convert_alpha()
        
        _level_list = self.__generate_level_list(num_rooms) 
        print('Level list: ', _level_list)

        # link to color pallete : https://lospec.com/palette-list/equpix15
        LEVEL_COLOR = [
            (82, 60, 78), (42, 42, 58), (62, 84, 66), (132, 84, 92), (56, 96, 124), (92, 122, 86), (16, 16, 36), (178, 126, 86), 
            (212, 78, 82), (85, 168, 148), (128, 172, 64), (236, 138, 75), (139, 208, 186), (255, 204, 104), (255, 248, 192) 
            ] 

        shuffle(LEVEL_COLOR) # randomize order of color in LEVEL_COLOR

        # lambda function to get colors in LEVEL_COLOR wihtout 'escape' of length
        _get_color = lambda index : LEVEL_COLOR[index] if 0 < index < len(LEVEL_COLOR) else (220, 220, 220)

        # Create vertex/nodes in graph
        for _room_value in range(len(_level_list)):
            _level = _level_list[_room_value]
            _create_basic_room = Room(_img1, _get_color(_level), _room_value, _level)
            self.insert_room( _create_basic_room )

        # Create connectiosn btw rooms (doors)
        self.generate_connectiosn_btw_rooms(chance_2_doors)

        self.currently_room_index = 0
        self.currently_room = self.__rooms[0] # get first room in graph

        self.update_doors_link()


    def __generate_level_list(self, number_rooms:int) -> list:
        
        if 2 <= number_rooms <= 11:
            _result = [1]
            _end_append = [1]
            _size = number_rooms - (2)
            _max_height = 3
        elif 11 < number_rooms <= 33:
            _result = [1, 2, 2, 2]
            _end_append = [1, 1, 1, 2]
            _size = number_rooms - (4 * 2)
            _max_height = 5
        else:
            _result = [1, 2, 2, 2, 3, 3, 3, 3, 3]
            _end_append = [1, 1, 1, 1, 1, 2, 2, 2, 3]
            _size = number_rooms - (9 * 2)
            _max_height = 7

        _size = _size // _max_height

        _level = _result[-1]

        for _ in range(_size):
            _level += 1
            _add_list = [_level for _ in range(_max_height)]
            _result.extend(_add_list)
        
        for i in range(len(_end_append)):
            _end_append[i] = _level + _end_append[i]
            
        _result.extend(_end_append)
        
        return _result


    def get_room_number(self) -> int:
        return self.currently_room.room_number

    def get_doors(self) -> dict:
        return self.doors


    def update_doors_link(self):
        
        _link_to = self.__graph[self.currently_room_index]
        self._attempts += 1

        self.doors["A"].set_room_index( _link_to[0] )
        self.doors["B"].set_room_index( _link_to[1] )
        self.doors["C"].set_room_index( _link_to[2] )

        if _link_to[0] == None and _link_to[1] == None and _link_to[2] == None:
            self.emit_callback() # when player won ( )
        

    def validate_collisions(self, px, py) -> int|None:    

        for door in self.doors.values():
            if door.point_collide_with_rect(px, py):
                return door.get_room_index()  

        return None


    def change_room(self, next_room:int|None) -> None:
        if next_room != None:
            if 0 <= next_room < len(self.__rooms):
                self.currently_room_index = next_room
                self.currently_room = self.__rooms[next_room]
                self.update_doors_link()


    def insert_room(self, room:Room) -> None:
        self.__rooms.append(room)

        _last_index : int = len(self.__rooms) - 1

        # go to index[0] or index[1] or index[2]
        self.__graph[_last_index] = [None, None, None]
        
 
    def generate_connectiosn_btw_rooms(self, chance_2_doors:float) -> None:
        # Create connections btw nodes/edges

        # Create a 'map' of index associetdes with levels
        _room_per_level : dict[int, list[int]] = {} # dict{int: list[int]}

        for index in range(len(self.__rooms)):
            _level : int = self.__rooms[index].level
            _get : list[int] = _room_per_level.get(_level, [])
            _get.append(index)
            _room_per_level.update({_level: _get})

        _LAST_LEVEL : int = self.__rooms[-1].level # level of last level room beside end game

        for room_index in range(len(self.__rooms)):
            _doors_num = 2 if random() < chance_2_doors else 3

            _selected_index : list[int|None] = []

            while len(_selected_index) < _doors_num:

                # ramdom choice a level value that can be previous, equal or next level 
                _select_level : int = self.__rooms[room_index].level + choice( (-1, 0, 1) )
                # get list of rooms in current level
                _get_rooms_in_level : list[int] | None = _room_per_level.get(_select_level, None)

                if _select_level <= 0 or _select_level > _LAST_LEVEL or _get_rooms_in_level ==  None: 
                    continue

                if room_index == (len(self.__rooms)-1):
                    break

                _target_index = choice( _get_rooms_in_level )

                if _target_index == room_index or _target_index in _selected_index:
                    continue
                else:
                    _selected_index.append(_target_index)
                    
            else:
                if _doors_num == 2:
                    _selected_index.insert(1, None) # add/insert None to index[1] ( Door 'B' )

                # print('a: ', room_index, ' --> ', _selected_index)
                self.__graph[room_index] = _selected_index

        #[ISSUE] : validate if exist some way to go for first room (level 1) until the last room (bigger level)
        self.__generate_path_to_win(_room_per_level)

    def print_game_map(self):

        # print ( room number,  doors(A:index, B:index, C:index), level)

        _result :dict = {}
        _room_index = 0

        for room in self.__rooms:
            _doors = {
                "A" : self.__graph[_room_index][0],
                "B" : self.__graph[_room_index][1],
                "C" : self.__graph[_room_index][2] 
            }

            _result[ _room_index ] = [_doors, room.level, room.room_number]
            
            _room_index += 1

        print("Map of rooms: ")
        for i in _result:
            print('Sala :', i, '| ', _result[i][2], " |--> ", _result[i][0], '| level: ', _result[i][1])

    def __generate_path_to_win(self, level_map:dict[int, list[int]]) -> None:

        print(" --- Level map: --- ")
        for k in level_map.keys(): 
            print(k, level_map[k])
        
        __level_counter : int = 1 # get first level value (1)
        _LAST_LEVEL : int = self.__rooms[-1].level # level of last level room beside end game

        for room_index in range(len(self.__rooms)):

            _counter_rooms_checkeds_in_level : int = 0

            for index in self.__graph[room_index]:
                
                if index == None:
                    break

                if self.__rooms[index].level <= ( __level_counter + 1 ):
                    _counter_rooms_checkeds_in_level += 1
                    continue
                
                if self.__rooms[index].level == _LAST_LEVEL:
                    break

                if _counter_rooms_checkeds_in_level == ( len(self.__graph[room_index]) - 1):
                    print("caminho corrigido em", self.__graph[room_index], " --> ", room_index)
                    self.__graph[room_index][2] = self.__rooms[index].level + 1
                    print("novo caminho : ", self.__graph[room_index])

        __level_counter += 1

                