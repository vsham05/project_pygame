import pygame
from random import randrange

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, room_x, room_y):
        super().__init__(*group)
        self.group = group
        self.clones = []
        self.items = []
        self.health = 3
        self.stand_image = [pygame.image.load('Images\\objects\\player\\player_stand.png')]
        self.rect = pygame.Rect(100 + 50 * x, 100 + 50 * y, 40, 45)
        self.move_image = [pygame.image.load('Images\\objects\\player\\player_move_1.png'),
                           pygame.image.load('Images\\objects\\player\\player_move_2.png')]
        self.frames = self.stand_image
        self.image = self.frames[0]
        
        self.room_x = room_x
        self.room_y = room_y
        self.frame = 0
    
    def set_item(self, item):
        self.items.append(item)

    def set_room(self, room):
        self.room = room
    
    def set_labirint(self, labirint):
        self.labirint = labirint
        
    def set_game_run(self, game_run):
        self.game_run = game_run

    def move(self, walls):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.frames = self.move_image
            self.frame = (self.frame + 1) % len(self.frames * 10)
            self.image = self.frames[self.frame // 10]
            self.rect = self.rect.move(0, -3)
            self.x = (self.rect.x - 100) // 50
            self.y = (self.rect.y - 100) // 50
            self.change_room()
            if pygame.sprite.spritecollideany(self, walls):
                self.rect = self.rect.move(0, 3)
                self.x = (self.rect.x - 100) // 50
                self.y = (self.rect.y - 100) // 50

        elif keys[pygame.K_s]:
                self.frames = self.move_image
                self.frame = (self.frame + 1) % len(self.frames * 10)
                self.rect = self.rect.move(0, 3)
                self.image = self.frames[self.frame // 10]
                self.x = (self.rect.x - 100) // 50
                self.y = (self.rect.y - 100) // 50 + 1
                self.change_room()
                if pygame.sprite.spritecollideany(self, walls):
                    self.rect = self.rect.move(0, -3)
                    self.x = (self.rect.x - 100) // 50
                    self.y = (self.rect.y - 100) // 50


        elif keys[pygame.K_a]:
            self.frames = self.move_image
            self.frame = (self.frame + 1) % len(self.frames * 10)
            self.rect = self.rect.move(-3, 0)
            self.image = self.frames[self.frame // 10]
            self.x = (self.rect.x - 100) // 50
            self.y = (self.rect.y - 100) // 50
            self.change_room()
            if pygame.sprite.spritecollideany(self, walls):
                self.rect = self.rect.move(3, 0)
                self.x = (self.rect.x - 100) // 50
                self.y = (self.rect.y - 100) // 50

        elif keys[pygame.K_d]:
            self.frames = self.move_image
            self.frame = (self.frame + 1) % len(self.frames * 10)
            self.rect = self.rect.move(3, 0)
            self.image = self.frames[self.frame // 10]
            self.x = (self.rect.x - 100) // 50 + 1
            self.y = (self.rect.y - 100) // 50 
            self.change_room()
            if pygame.sprite.spritecollideany(self, walls):
                self.rect = self.rect.move(-3, 0)
                self.x = (self.rect.x - 100) // 50
                self.y = (self.rect.y - 100) // 50
        else:
            self.frame += 0
            self.frames = self.stand_image
            self.image = self.frames[0]

        self.x = (self.rect.x - 100) // 50
        self.y = (self.rect.y - 100) // 50
    
    def take_damage(self):
        self.health -= 1

    def change_room(self):
        if self.room.floor[self.x][self.y].get_type() == 'wall' and self.room.floor[self.x][self.y].enabled:
            if self.room.floor[self.x][self.y].get_side() == 'up':
                self.room_x -= 1
                self.x = len(self.labirint[self.room_x][self.room_y].floor) - 2
                for i in range(1, len(self.labirint[self.room_x][self.room_y].floor[0]) - 1):
                    if self.labirint[self.room_x][self.room_y].floor[i][-1].enabled:
                        self.y = i 
                self.rect = pygame.Rect(100 + (50 * self.y - 1) + 3, 100 + 50 * self.x, 40, 45)
                self.room = self.labirint[self.room_x][self.room_y]

            if self.room.floor[self.x][self.y].get_side() == 'left':
                self.room_y -= 1
                self.y = len(self.labirint[self.room_x][self.room_y].floor) - 2
                for i in range(1, len(self.labirint[self.room_x][self.room_y].floor[0]) - 1):
                    if self.labirint[self.room_x][self.room_y].floor[-1][i].enabled:
                        self.x = i
                self.rect = pygame.Rect(100 + (50 * self.y - 1) + 3, 100 + 50 * self.x + 4, 40, 45)
                self.room = self.labirint[self.room_x][self.room_y]

            if self.room.floor[self.x][self.y].get_side() == 'right':
                self.room_y += 1
                self.y = 1
                for i in range(1, len(self.labirint[self.room_x][self.room_y].floor[0]) - 1):
                    if self.labirint[self.room_x][self.room_y].floor[0][i].enabled:
                        self.x = i
                self.rect = pygame.Rect(100 + (50 * self.y - 1) + 3, 100 + 50 * self.x + 4, 40, 45)
                self.room = self.labirint[self.room_x][self.room_y]

            if self.room.floor[self.x][self.y].get_side() == 'down':
                self.room_x += 1
                self.x = 1
                for i in range(1, len(self.labirint[self.room_x][self.room_y].floor[0]) - 1):
                    if self.labirint[self.room_x][self.room_y].floor[i][0].enabled:
                        self.y = i  
                self.rect = pygame.Rect(100 + (50 * self.y - 1) + 3, 100 + 50 * self.x, 40, 45)
                self.room = self.labirint[self.room_x][self.room_y]

            if self.room.room_type == 'clone':
                if not self.room.passed:
                    clone_x = randrange(1, len(self.room.floor) - 1)
                    clone_y = randrange(1, len(self.room.floor) - 1)
                    while self.room.floor[clone_y][clone_x].get_item() is not None:
                        clone_x = randrange(1, len(self.room.floor) - 1)
                        clone_y = randrange(1, len(self.room.floor) - 1)
                    clone = Clone(self.group, x=clone_x, y=clone_y, room_x = 0,room_y = 0)
                    clone.set_room(self.room)
    
    def change_group(self, *group):
        self.group = group

class Clone(Player):
    def change_room(self):
        pass

