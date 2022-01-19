from random import randrange
import pygame

class Cell():
    def __init__(self, image, enabled, type_of_cell='floor', correcting_x = 0, correcting_y = 0):
        self.image = pygame.image.load(image)
        self.enabled = enabled
        self.type_of_cell = type_of_cell
        self.correcting_x = correcting_x
        self.correcting_y = correcting_y
    
    def get_correcting(self):
        return (self.correcting_x, self.correcting_y)

    def get_type(self):
        return self.type_of_cell

    def change_enabled(self):
        self.enabled = not self.enabled
    
    def get_image(self):
        return self.image


class Room():
    def __init__(self, room_type):
        self.room_type = room_type
        self.size = randrange(6, 12)

        self.floor = [[0] * self.size for i in range(self.size)]
        for row in range(1, self.size - 1):
            for col in range(1, self.size - 1):
                self.floor[row][col] = (Cell(f'Images\\floor\\piece_{randrange(1, 3)}.png',
                                                  True))
        for piece_num in range(self.size):
            self.floor[0][piece_num] = Cell(f'Images\\walls\\wall_with_grass.png',
                                                  False, correcting_y= -30)

            self.floor[-1][piece_num] = Cell(f'Images\\walls\\wall_with_grass_down.png',
                                                  False)

            self.floor[piece_num][0] = Cell(f'Images\\walls\\wall_with_grass_left.png',
                                                  False, correcting_x= -10)     
            self.floor[piece_num][-1] = Cell(f'Images\\walls\\wall_with_grass_right.png',
                                                  False) 
            
            self.floor[0][0] = Cell(f'Images\\walls\\space.png',
                                                  False)
            
            self.floor[-1][0] = Cell(f'Images\\walls\\space.png',
                                                  False)
            
            self.floor[0][-1] = Cell(f'Images\\walls\\space.png',
                                                  False)
            self.floor[-1][-1] = Cell(f'Images\\walls\\space.png',
                                                  False)
          
        self.items = []
    
    def show_floor(self, display):
        for floor_row in range(len(self.floor)):
            for floor_col in range(len(self.floor[floor_row])):
                display.blit(self.floor[floor_row][floor_col].get_image(), 
                            (100 + 50 * floor_col + self.floor[floor_row][floor_col].get_correcting()[0],
                             100 + 50 * floor_row + self.floor[floor_row][floor_col].get_correcting()[-1]))
    
    def set_door(self, way):
        if way == 'up':
            self.floor[0][randrange(1, len(self.floor[0]) - 1)] = Cell('Images\\walls\\door_up.png',
                                                         enabled = True, type_of_cell='door', correcting_y= -30)
        
        elif way == 'down':
            self.floor[-1][randrange(1, len(self.floor[0]) - 1)] = Cell('Images\\walls\\door_down.png',
                                                         enabled = True, type_of_cell='door')
        elif way == 'left':
            self.floor[randrange(1, len(self.floor[0]) - 1)][0] = Cell('Images\\walls\\door_left.png',
                                                         enabled = True, type_of_cell='door', correcting_x= -10)
        elif way == 'right':
            self.floor[randrange(1, len(self.floor[0]) - 1)][-1] = Cell('Images\\walls\\door_right.png',
                                                         enabled = True, type_of_cell='door')


    def put_items(self):
        pass

    def __repr__(self):
        return self.room_type
        


