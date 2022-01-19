import pygame

pygame.init()

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, image, player, *group):
        super().__init__(*group)
        self.x = x
        self.y = y
        self.player = player
        self.image = image
        self.rect = pygame.Rect(100 + 50 * x, 100 + 50 * y, 50, 50)
    
    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            self.player.set_item(self)
            self.kill()