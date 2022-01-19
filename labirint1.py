from random import randrange, choice
import pygame
from Traps import Skeleton, HiddenSpike, OpenSpike, StoneStopper, FinishPoint, Altar, FinalDoor, Fountain
from rewards import Item


pygame.init()


class Cell(pygame.sprite.Sprite):
    def __init__(self, *group, enabled, type_of_cell='floor', item = None, side=None, correcting_x = 0, correcting_y = 0):
        super().__init__(*group)
        self.item = item
        self.correcting_x = correcting_x
        self.correcting_y = correcting_y
        self.rect = (0, 0, 0, 0)
        self.side = side
        if type_of_cell == 'floor':
            self.image = pygame.image.load(f'Images\\floor\\piece_{randrange(1, 4)}.png').convert()
        elif type_of_cell == 'wall':
            if side == 'left':
                self.image = pygame.image.load(f'Images\\walls\\wall_left{randrange(1, 4)}.png').convert()
            if side == 'right':
                self.image = pygame.image.load(f'Images\\walls\\wall_right{randrange(1, 4)}.png').convert()
            if side == 'down':
                self.image = pygame.image.load(f'Images\\walls\\wall_down{randrange(1, 4)}.png').convert()
            if side == 'up':
                self.image = pygame.image.load(f'Images\\walls\\wall_top{randrange(1, 4)}.png').convert()

        self.enabled = enabled
        self.type_of_cell = type_of_cell
    
    def get_item(self):
        return self.item
    
    def set_item(self, item):
        self.item = item

    def get_correcting(self):
        return (self.correcting_x, self.correcting_y)

    def get_type(self):
        return self.type_of_cell

    def change_enabled(self):
        self.enabled = not self.enabled

    def get_side(self):
        return self.side
    
    def get_image(self):
        return self.image


class Room():
    def __init__(self, room_type):
        self.floors = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.room_type = room_type
        self.items = pygame.sprite.Group()
        self.size = randrange(8, 9)
        self.floor = [[0] * self.size for i in range(self.size)]
        for row in range(1, self.size - 1):
            for col in range(1, self.size - 1):
                self.floor[row][col] = (Cell(self.floors, enabled=True))

        for piece_num in range(self.size):
            self.floor[0][piece_num] = Cell(self.walls, enabled=False, type_of_cell='wall', side='left', correcting_x= -20)

            self.floor[-1][piece_num] = Cell(self.walls, enabled=False, type_of_cell='wall', side='right')

            self.floor[piece_num][0] = Cell(self.walls, enabled=False, type_of_cell='wall', side='up', correcting_y= -30)

            self.floor[piece_num][-1] = Cell(self.walls, enabled=False, type_of_cell='wall', side='down')

        self.floor[0][0].image = pygame.image.load('Images\\walls\\space.png').convert()

        self.floor[-1][0].image = pygame.image.load('Images\\walls\\space.png').convert()

        self.floor[0][-1].image = pygame.image.load('Images\\walls\\space.png').convert()

        self.floor[-1][-1].image = pygame.image.load('Images\\walls\\space.png').convert()

        for col in range(len(self.floor)):
            for row in range(len(self.floor[0])):
                if self.floor[col][row].get_type() == 'floor':
                    self.floor[col][row].rect = (100 + 50 * col, 100 + 50 * row, 50, 50)
                elif self.floor[col][row].get_type() in ('wall', 'door'):
                    if self.floor[col][row].side in ['left', 'right']:
                        self.floor[col][row].rect = (100 + 50 * col + self.floor[col][row].get_correcting()[0],
                                                     100 + 50 * row + self.floor[col][row].get_correcting()[1], 70, 50)
                    if self.floor[col][row].side in ['down', 'up']:
                        self.floor[col][row].rect = (100 + 50 * col + self.floor[col][row].get_correcting()[0],
                                                     100 + 50 * row + self.floor[col][row].get_correcting()[1], 50, 70)

    def show_floor(self, display, player_group):
        self.floors.draw(display)
        self.walls.draw(display)
        self.items.draw(display)
        self.items.update()
    
    def set_door(self, way):
        door_place = randrange(2, len(self.floor[0]) - 2)
        if way == 'up':
            self.floor[door_place][0].image = pygame.image.load(f'Images\\walls\\door_up.png').convert()
            self.floor[door_place][0].change_enabled()
            if self.floor[door_place + 1][0].get_item() is not None:
                self.floor[door_place + 1][0].kill()
        elif way == 'down':
            self.floor[door_place][-1].image = pygame.image.load(f'Images\\walls\\door_down.png').convert()
            self.floor[door_place][-1].change_enabled()
            if self.floor[door_place - 1][-1].get_item() is not None:
                self.floor[door_place - 1][-1].kill()
        elif way == 'left':
            self.floor[0][door_place].change_enabled()
            self.floor[0][door_place].image = pygame.image.load(f'Images\\walls\\door_left.png').convert()
            if self.floor[1][door_place].get_item() is not None:
                self.floor[1][door_place].kill()
        elif way == 'right':
            self.floor[-1][door_place].change_enabled()
            self.floor[-1][door_place].image = pygame.image.load(f'Images\\walls\\door_right.png').convert()
            if self.floor[-2][door_place].get_item() is not None:
                self.floor[-2][door_place].kill()

    def put_items(self, items):
        for item in items:
            self.items.add(item)
    
    def make_traps(self, traps_classes, player, display):
        for trap in traps_classes:
            if trap == StoneStopper:
                num_traps = randrange(0, 4)
                for i in range(num_traps):
                    x = randrange(3, len(self.floor) - 3)
                    y = randrange(3, len(self.floor) - 3)
                    if self.floor[x][y].get_item() is None:
                        stone = StoneStopper(x, y)
                        self.items.add(stone)
                        self.floor[x][y].set_item(stone)
                        self.walls.add(stone)
            elif trap == OpenSpike:
                num_traps = randrange(0, 3)
                for i in range(num_traps):
                    side = choice(['horizontal', 'vertical'])
                    c = randrange(3, len(self.floor) - 3)
                    timer = randrange(150, 200)
                    if side == 'horizontal':
                        for x in range(1, len(self.floor) - 1):
                            if self.floor[x][c].get_item() is None:
                                spike = OpenSpike(x, c, timer, player, self)
                                self.items.add(spike)
                                self.floor[x][c].set_item(spike)
                    elif side == 'vertical':
                        for y in range(1, len(self.floor) - 1):
                            if self.floor[c][y].get_item() is None:
                                spike = OpenSpike(c, y, timer, player, self)
                                self.items.add(spike)
                                self.floor[c][y].set_item(spike)
            elif trap == HiddenSpike:
                num_traps = randrange(0, 4)
                for i in range(num_traps):
                    x = randrange(3, len(self.floor) - 3)
                    y = randrange(3, len(self.floor) - 3)
                    spike = HiddenSpike(x, y, player, self)
                    if self.floor[x][y].get_item() is None:
                        self.items.add(HiddenSpike(x, y, player, self))
                        self.floor[x][y].set_item(spike)
            elif trap == Skeleton:
                sides = ['top', 'left', 'right', 'down']
                num_traps = randrange(0, 5)
                for c in range(num_traps):
                    self.items.add(Skeleton(choice(sides), player, self, display))

        
    def __repr__(self):
        return self.room_type
    

class CloneRoom(Room):
    def make_traps(self, traps_classes, player, player_group, i, j, display, items_images):
        self.finish_points = []
        self.items_images = items_images
        x = randrange(2, len(self.floor) - 2)
        y = randrange(2, len(self.floor) - 2)
        self.reward = Item(x, y, choice(self.items_images), player)
        self.floor[x][y].set_item('REWAAAAAAARD!!!')
        self.player_group = player_group
        self.player = player
        self.passed = False

        for trap in traps_classes:
            if trap == StoneStopper:
                num_traps = randrange(3, 9)
                for i in range(num_traps):
                    x = randrange(2, len(self.floor) - 2)
                    y = randrange(2, len(self.floor) - 2)
                    if self.floor[x][y].get_item() is None:
                        stone = StoneStopper(x, y)
                        self.items.add(stone)
                        self.floor[x][y].set_item(stone)
                        self.walls.add(stone)
            elif trap == FinishPoint:
                for _ in range(2):
                    x = randrange(2, len(self.floor) - 2)
                    y = randrange(2, len(self.floor) - 2)
                    while self.floor[x][y].get_item() is not None:
                        x = randrange(2, len(self.floor) - 2)
                        y = randrange(2, len(self.floor) - 2)
                    finish_point = FinishPoint(x, y)
                    self.items.add(finish_point)
                    self.floor[x][y].set_item(finish_point)
                    self.finish_points.append(finish_point)
            
    def show_floor(self, display, player_group):
        super().show_floor(display, player_group)
        if (pygame.sprite.spritecollideany(self.finish_points[0], player_group) and
           pygame.sprite.spritecollideany(self.finish_points[1], player_group)) and self.reward is not None:
           self.items.add(self.reward)
           self.reward = None
           self.passed = True
        else:
            self.passed = False


class SearchRoom(Room):
    def make_traps(self, traps_classes, player, display, items_images):
        x = randrange(2, len(self.floor) - 2)
        y = randrange(2, len(self.floor) - 2)
        self.items_images = items_images
        self.reward = Item(x, y, choice(self.items_images), player)
        self.floor[x][y].set_item('REWAAAAAAARD!!!')
        for trap in traps_classes:
            if trap == Altar:
                x = randrange(3, len(self.floor) - 3)
                y = randrange(3, len(self.floor) - 3)
                if self.floor[x][y].get_item() is None:
                    altar = Altar(x, y, player, self.reward, self.items)
                    self.items.add(altar)
                    self.floor[x][y].set_item(altar)


class FinalRoom(Room):
    def make_traps(self, traps_classes, player, display):
        for trap in traps_classes:
            if trap == FinalDoor:
                x = randrange(3, len(self.floor) - 3)
                y = randrange(3, len(self.floor) - 3)
                self.items.add(FinalDoor(x, y, player, display))

class FountainRoom(Room):
    def make_traps(self, traps_classes, player, display):
        for trap in traps_classes:
            if trap == Fountain:
                x = randrange(3, len(self.floor) - 3)
                y = randrange(3, len(self.floor) - 3)
                self.items.add(Fountain(x, y, player))



                        

        


