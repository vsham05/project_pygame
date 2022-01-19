from random import randrange
import pygame as pygame
pygame.init()


class SearchGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 50

        self.n = randrange(1, 10)
        self.n1 = randrange(1, 10)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pygame.draw.rect(screen, (255, 255, 255), ((self.left + self.cell_size * j,
                                                            self.top + self.cell_size * i),
                                                           (self.cell_size, self.cell_size)), 1)

    def render1(self, screen):
        for i in range(35, 535, 50):
            for j in range(35, 535, 50):
                if i // 50 != self.n or j // 50 != self.n1:
                    image = pygame.image.load(f"Images\\objects\\skull{randrange(1, 5)}.png")
                    image1 = image.get_rect(center=(i, j))
                    screen.blit(image, image1)
                else:
                    image = pygame.image.load("Images\\objects\\skull.png")
                    image1 = image.get_rect(center=(i, j))
                    screen.blit(image, image1)
                pygame.display.flip()

    def get_cell(self, mouse_pos):
        if (self.left < mouse_pos[0] < self.left + self.cell_size * len(self.board[0]) and
                self.top < mouse_pos[-1] < self.top + self.cell_size * len(self.board)):
            return [((mouse_pos[0] - self.left) // self.cell_size,
                    (mouse_pos[1] - self.top) // self.cell_size), (self.n, self.n1)]


def play(player):
    board = SearchGame(10, 10)
    screen = pygame.display.set_mode((800, 600))
    running = True
    screen.fill((0, 0, 0))

    f1 = pygame.font.Font(None, 25)

    text1 = f1.render("ПРАВИЛА", True, (255, 0, 0))
    text2 = f1.render("Вам нужно найти:", True, (255, 0, 0))
    text3 = f1.render("Нужно нажать на него", True, (255, 0, 0))
    text4 = f1.render("для выполнения задачи.", True, (255, 0, 0))
    text5 = f1.render("За неправильный выбор", True, (255, 0, 0))
    text6 = f1.render("будет отниматься жизнь.", True, (255, 0, 0))

    image = pygame.image.load("Images\\objects\\skull.png")
    image1 = image.get_rect(center=(750, 45))

    screen.blit(image, image1)
    screen.blit(text1, (630, 10))
    screen.blit(text2, (550, 40))
    screen.blit(text3, (550, 70))
    screen.blit(text4, (550, 100))
    screen.blit(text5, (550, 170))
    screen.blit(text6, (550, 200))

    board.render1(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.get_cell(event.pos) != None:
                    if board.get_cell(event.pos)[0] == board.get_cell(event.pos)[1]:
                        running = False
                    else:
                        player.take_damage()
                        if player.health == 0:
                            running = False

        board.render(screen)
        pygame.display.flip()