import pygame
import os.path as path
from random import choice

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
        self.__rooms = []
        self.__graph = {}

        self.currently_room : Room 

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

        # if num_rooms < 0 or num_rooms is not int:
        #     raise ValueError('number of rooms must be a positive integer.')

        # if chance_2_doors < 0 or chance_2_doors > 1:
        #     raise ValueError('chance of two doors rooms must be a float number btw 0 and 1.')

        _img1 = pygame.image.load(ImagePath.simple_room).convert()
        
        _level_list = self.__generate_level_list(num_rooms)
        print('Teste: ', _level_list)
        # Create vertex/nodes in graph
        for _room_value in range(len(_level_list)):
            _level = _level_list[_room_value]
            _create_basic_room = Room(_img1, (245, 180, 200), _room_value, _level)
            self.insert_room( _create_basic_room )

        # Create connectiosn btw rooms (doors)
        # [ISSUE] : implement possibility to generate only 2 doors
        self.generate_connectiosn_btw_rooms()

        self.currently_room_index = 0
        self.currently_room = self.__rooms[0] # get first room in graph

        self.update_doors_link()

        # self.__graph[-1]['GO_TO'] = [None, None, None]


    def __generate_level_list(self, number_rooms:int) -> list:
        
        if 2 <= number_rooms <= 11:
            _result = [1]
            _end_append = [1]
            _level = 2
            _size = number_rooms - (2)
            _max_height = 3
        elif 11 < number_rooms <= 33:
            _result = [1, 2, 2, 2]
            _end_append = [2, 2, 2, 1]
            _level = 3
            _size = number_rooms - (4 * 2)
            _max_height = 5
        else:
            _result = [1, 2, 2, 2, 3, 3, 3, 3, 3]
            _end_append = [3, 3, 3, 3, 3, 2, 2, 2, 1]
            _size = number_rooms - (9 * 2)
            _level = 4
            _max_height = 7
        
        _counter = 0
        for i in range(_size+1):
            
            if _counter >= _max_height:
                _counter = 0
                _level += 1
                
            _result.append(_level)
            _counter += 1
        
        if _counter == 0 :
            _level += 1
        
        _last_value =  _end_append[0]
        for i in range(len(_end_append)):
            if _last_value != _end_append[i]:
                _level += 2
            _end_append[i] += _level
            
        # _result = _result + _end_append
        _result.extend(_end_append)
        
        return _result

    def get_room_number(self) -> int:
        return self.currently_room.room_number

    def get_doors(self) -> dict:
        return self.doors


    def update_doors_link(self):
        
        _link_to = self.__graph[self.currently_room_index]['GO_TO']
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

        self.__graph[_last_index] = {
            'GO_TO' : [None, None, None],       # go to index[0] or index[1] or index[2]
            'COMES' : []                        # comes from any nodes, just need be different to go to index 
        }
 
    def generate_connectiosn_btw_rooms(self) -> None:
        # Create connections btw nodes/edges

        # Create a 'map' of index associetdes with levels
        _room_per_level : dict = {}

        for index in range(len(self.__rooms)):
            _level = self.__rooms[index].level
            _get : list = _room_per_level.get(_level, [])
            _get.append(index)
            _room_per_level.update({_level: _get})

        _LAST_LEVEL : int = self.__rooms[-1].level # level of last level room beside end game

        # QUANDO CRIAR A CONEXÃO ENTRE 2 VERTEX DEVO CHEGAR
            # - Se o index é o mesmo...
            # - Se o index ésta em (-1, 0, 1) level acima
            # - Se o target index já envia para aquele index

        for room_index in range(len(self.__rooms)):
            # [ISSUE] : implement possibility to generate only 2 doors
            _selected_index = []
            while len(_selected_index) < 3:

                _select_level = self.__rooms[room_index].level + choice( (-1, 0, 1) )
                _get_rooms_in_level =_room_per_level.get(_select_level, None)

                if _select_level <= 0 or _select_level > _LAST_LEVEL or _get_rooms_in_level ==  None: 
                    continue

                if room_index == (len(self.__rooms)-1):
                    break

                _target_index = choice( _get_rooms_in_level )

                if _target_index == room_index or _target_index in _selected_index:
                    continue
                else:
                    _selected_index.append(_target_index)
                    # self.__graph[_target_index]['COMES'].append(room_index)
                    
            else:
                print('a: ', room_index, ' --> ', _selected_index)
                self.__graph[room_index]['GO_TO'] = _selected_index

        #[ISSUE] : validate if exist some way to go for first room (level 1) until the last room (bigger level)

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

            _result[ _room_index ] = [_doors, room.level, room.room_number]
            
            _room_index += 1

        print("Map of rooms: ")
        for i in _result:
            print('Sala :', i, '| ', _result[i][2], " |--> ", _result[i][0], '| level: ', _result[i][1])