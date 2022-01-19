import pygame
from random import randrange
from SearchGame import play
class Skeleton(pygame.sprite.Sprite):
    def __init__(self, side, player, room, display, *group):
        super().__init__(*group)
        self.display = display
        self.side = side
        self.room = room
        self.player = player
        self.fireballs = pygame.sprite.Group()
        self.image = pygame.image.load('Images\\objects\\skeleton_top_cad1.png')
        if self.side == 'top':
            self.x = randrange(2, len(self.room.floor) - 1)
            self.y = 0
            self.images = [pygame.image.load('Images\\objects\\skeleton_top_cad1.png'),
                           pygame.image.load('Images\\objects\\skeleton_top_cad2.png'),
                           pygame.image.load('Images\\objects\\skeleton_top_cad3.png')]
        elif self.side == 'left':
            self.x = -1
            self.y = randrange(2, len(self.room.floor) - 1)
            self.images = [pygame.image.load('Images\\objects\\skeleton_left_cad1.png'),
                           pygame.image.load('Images\\objects\\skeleton_left_cad2.png'),
                           pygame.image.load('Images\\objects\\skeleton_left_cad3.png')]
        
        elif self.side == 'right':
            self.x = len(self.room.floor) - 1
            self.y = randrange(2, len(self.room.floor) - 1)
            self.images = [pygame.image.load('Images\\objects\\skeleton_right_cad1.png'),
                           pygame.image.load('Images\\objects\\skeleton_right_cad2.png'),
                           pygame.image.load('Images\\objects\\skeleton_right_cad3.png')]

        elif self.side == 'down':
            self.x = randrange(2, len(self.room.floor) - 1)
            self.y = len(self.room.floor) 
            self.images = [pygame.image.load('Images\\objects\\skeleton_down_cad1.png'),
                           pygame.image.load('Images\\objects\\skeleton_down_cad2.png'),
                           pygame.image.load('Images\\objects\\skeleton_down_cad3.png')]
        self.rect = pygame.Rect(100 + self.x * 50, 100 + (self.y - 1) * 50, 50, 80)
        self.time = 0
    
    def add_fireball(self):
        fireball_side = self.side
        if self.side == 'top':
            fireball_x = self.x
            fireball_y = 1
        elif self.side == 'down':
            fireball_x = self.x
            fireball_y = len(self.room.floor)
        elif self.side == 'left':
            fireball_x = 1
            fireball_y = self.y - 1
        elif self.side == 'right':
            fireball_x = len(self.room.floor)
            fireball_y = self.y - 1
        self.fireballs.add(FireBall(fireball_x, fireball_y, fireball_side,
                                    self.player, self.room, self.fireballs))
    
    def update(self):
        if self.time == 150:
            self.add_fireball()
            self.time = 0
        self.image = self.images[self.time // 50]
        self.time += 1
        self.fireballs.update()
        self.fireballs.draw(self.display)
        

class FireBall(pygame.sprite.Sprite):
    def __init__(self, x, y, way, player, room, *group):
        super().__init__(*group)
        self.player = player
        self.room = room
        self.x = x
        self.y = y
        self.frame = 0
        if way == 'down':
            self.velocity = (0, -3)
            self.images = [pygame.image.load('Images\\objects\\fireball_down_cad1.png'),
                           pygame.image.load('Images\\objects\\fireball_down_cad2.png')]
            self.rect = pygame.Rect(100 + x * 50, 100 + (y - 1) * 50 - 70, 50, 50)
        elif way == 'top':
            self.velocity = (0, 3)
            self.images = [pygame.image.load('Images\\objects\\fireball_top_cad1.png'),
                           pygame.image.load('Images\\objects\\fireball_top_cad2.png')]
            self.rect = pygame.Rect(100 + x * 50, 100 + (y - 1) * 50 + 70, 50, 50)
        elif way == 'right':
            self.velocity = (-3, 0)
            self.images = [pygame.image.load('Images\\objects\\fireball_right_cad1.png'),
                           pygame.image.load('Images\\objects\\fireball_right_cad2.png')]
            self.rect = pygame.Rect(100 + (x - 1) * 50 - 70, 100 + y * 50, 50, 50)
        elif way == 'left':
            self.velocity = (3, 0)
            self.images = [pygame.image.load('Images\\objects\\fireball_left_cad1.png'),
                           pygame.image.load('Images\\objects\\fireball_left_cad2.png')]
            self.rect = pygame.Rect(100 + (x - 1) * 50 + 70, 100 + y * 50, 50, 50)
    
    def update(self):
        self.rect = self.rect.move(self.velocity)
        self.x = (self.rect.x - 100 - 70) // 50 + 1
        self.y = (self.rect.y - 100 - 70) // 50 + 1
        if pygame.sprite.spritecollideany(self, self.room.walls):
            self.kill()
        if pygame.sprite.collide_rect(self, self.player):
            self.player.take_damage()
            self.kill()

        self.image = self.images[self.frame // 5]
        self.frame += 1
        if self.frame == 10:
            self.frame = 0


class HiddenSpike(pygame.sprite.Sprite):
    def __init__(self, x, y, player, room, *group):
        super().__init__(*group)
        self.player = player
        self.room = room
        self.x = x
        self.y = y
        self.unworking_time = 0
        self.rect = pygame.Rect(100 + (self.x) * 50, 
                                 100 + (self.y) * 50, 40, 40)
        
        self.images = [pygame.image.load('Images\\objects\\spire_1_ver1.png'),
                       pygame.image.load('Images\\objects\\spire_2_ver1.png')]
        self.image = self.images[0]
        
    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            if self.unworking_time == 0:
                self.player.take_damage()
                self.unworking_time = 200
        if self.unworking_time != 0:
            self.image = self.images[1]
            self.unworking_time -= 1
        else:
            self.image = self.images[0]  


class OpenSpike(pygame.sprite.Sprite):
    def __init__(self, x, y, timer, player, room, *group):
        super().__init__(*group)
        self.timer = timer
        self.player = player
        self.room = room
        self.x = x
        self.y = y
        self.time = 0
        self.working = False
        self.rect = pygame.Rect(100 + (self.x) * 50, 
                                 100 + (self.y) * 50 - 10, 50, 50)
        
        self.images = [pygame.image.load('Images\\objects\\spire_2_ver2.png'),
                       pygame.image.load('Images\\objects\\spire_1_ver2.png')]
        self.image = self.images[0]
        
    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            if self.working:
                self.player.take_damage()
                self.working = False
                self.time = 300
                
        if self.time != 0:
            if self.working:
                self.image = self.images[1]
            else:
                self.image = self.images[0]
            self.time -= 1
        else:
            self.time = self.timer
            self.working = not self.working    


class StoneStopper(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.x = x
        self.y = y
        self.image = pygame.image.load(f'Images\\objects\\stone_stoper{randrange(1, 3)}.png')
        self.rect = pygame.Rect(100 + (self.x) * 50, 
                                 100 + (self.y) * 50, 50, 50)
    
    def update(self):
        pass


class FinishPoint(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.x = x
        self.y = y
        self.images = [pygame.image.load(f'Images\\puzzles\\mirror\\finish{i + 1}.png')
                       for i in range(6)]
        self.image = self.images[0]
        self.rect = pygame.Rect(100 + 50 * x, 100 + 50 * y, 50, 50)
        self.frame = 0
    
    def update(self):
        self.frame += 1
        if self.frame > 5 * 30:
            self.frame = 0
        self.image = self.images[self.frame // 30]


class Altar(pygame.sprite.Sprite):
    def __init__(self, x, y, player, item, group):
        super().__init__(*group)
        self.x = x
        self.y = y
        self.group = group
        self.item = item
        self.player = player
        self.rect = pygame.Rect(100 + 50 * x, 100 + 50 * y, 50, 50)
        self.image = pygame.image.load('Images\\objects\\2131.png')
    
    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            self.player.rect = pygame.Rect(100 + (50 * self.player.y - 3) + 4, 100 + 50 * self.player.x, 40, 49)
            if self.item is not None:
                play(self.player)
                self.group.add(self.item)
                self.item = None


class FinalDoor(pygame.sprite.Sprite):
    def __init__(self, x, y, player, display, *group):
        super().__init__(*group)
        self.x = x
        self.y = y
        self.display = display
        self.player = player
        self.rect = pygame.Rect(self.x * 50 + 100, self.y * 50 + 100, 50, 50)
        self.image = pygame.image.load('Images\\objects\\final_door.png')

    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            if len(self.player.items) >= 3:
                self.player.game_run = False
                self.player.kill()
                font = pygame.font.Font('data\\game_font.ttf', 60)
                loading_text = font.render('Загрузка...', True, (255, 255, 255))
                self.display.blit(loading_text, (300, 300))
                

class BegginingText():
    def __init__(self, number_of_floor):
        self.number_of_floor = number_of_floor
        self.font = pygame.font.Font('data\\game_font.ttf', 60)
        self.time = 255 

    def draw(self, display):
        self.time -= 1
        text = self.font.render(f"{self.number_of_floor} Этаж", True, (255 - self.time, 255, 255 - self.time ))
        display.blit(text, (300, 300))


class Fountain(pygame.sprite.Sprite):
    def __init__(self, x, y, player, *group):
        super().__init__(*group)
        self.x = x
        self.y = y
        self.player = player
        self.rect = pygame.Rect(100 + 50 * x, 100 + 50 * y, 50, 50)
        self.images = [pygame.image.load('Images\\objects\\fountain_cad1.png'),
                       pygame.image.load('Images\\objects\\fountain_cad2.png')]
        self.frame = 0
        self.image = self.images[0]
    
    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            if len(self.player.items) > 3:
                del self.player.items[-1]
                self.player.health += 1
            self.player.rect = pygame.Rect(100 + (50 * self.player.y - 2) + 4, 100 + 50 * self.player.x, 40, 49)
        self.frame += 1
        if self.frame == len(self.images) * 30:
            self.frame = 0
        self.image = self.images[self.frame // 30]

        



    