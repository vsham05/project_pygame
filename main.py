import pygame
import pygame_menu
from pygame_menu import Theme
from random import randrange, choice
from labirint1 import Room, CloneRoom, SearchRoom, FinalRoom, FountainRoom
from Player import Player, Clone
from Traps import Skeleton, OpenSpike, HiddenSpike, StoneStopper, FinishPoint, Altar, FinalDoor, Fountain
from Traps import BegginingText
from about_programm import about_programm

pygame.init()


def about_program():
    about_programm()


def check_coord(floor, x, y):
    try:
        if x < 0 or y < 0:
            return False

        return floor[x][y]
        
    except IndexError:
        return False


def labirint_creator(display):
    floor_size = 10
    rooms = ['N', 'usual', 'usual', 'search', 'search', 'clone', 'clone', 'fountain']
    items_images = [pygame.image.load('Images\\puzzles\\rewards\\red_stone.png'),
                   pygame.image.load('Images\\puzzles\\rewards\\blue_stone.png'),
                   pygame.image.load('Images\\puzzles\\rewards\\yellow_stone.png')]
    floor = [['N'] * floor_size for i in range(floor_size)]

    
    for i in range(floor_size):
        for j in range(floor_size):
            room_type = choice(rooms)
            floor[i][j] = room_type

    start_room_x = randrange(1, 5)
    start_room_y = randrange(1, 5)
    player_group = pygame.sprite.Group()
    player = Player(player_group, x=3, y=3, room_x=start_room_x, room_y=start_room_y)
    final_room_x = choice([0, 5])
    final_room_y = choice([0, 5])

    for i in range(floor_size):
        for j in range(floor_size):
            if check_coord(floor, i + 1, j + 1):
                if floor[i][j + 1] == 'N' and floor[i + 1][j] == 'N':
                    room_type = choice(rooms)
                    if randrange(0, 2) == 0:
                        floor[i][j + 1] = room_type
                    else:
                        floor[i + 1][j] = room_type

    for i in range(len(floor)):
        for j in range(len(floor)):
            if floor[i][j] != 'N':
                if floor[i][j] == 'clone':       
                    floor[i][j] = CloneRoom('clone')
                    floor[i][j].make_traps([StoneStopper, FinishPoint], player, player_group, i, j, display, items_images= items_images)
                elif floor[i][j] == 'search':
                    floor[i][j] = SearchRoom('search')
                    floor[i][j].make_traps([Altar], player, display, items_images)
                
                elif floor[i][j] == 'fountain':
                    floor[i][j] = FountainRoom('fountain')
                    floor[i][j].make_traps([Fountain], player, display)

                else:
                    floor[i][j] = Room('Usual')
                    floor[i][j].make_traps([StoneStopper, HiddenSpike, OpenSpike, Skeleton], player, display)
        
    floor[start_room_x][start_room_y] = Room('Start')
    floor[final_room_x][final_room_y] = FinalRoom('Final')
    floor[final_room_x][final_room_y].make_traps([FinalDoor], player, display)
    
    for i in range(len(floor)):
        for j in range(len(floor)):
            if check_coord(floor, i + 1, j):
                if floor[i + 1][j] != 'N' and floor[i][j] != 'N':
                    floor[i][j].set_door('down')

            if check_coord(floor, i - 1, j):
                if floor[i - 1][j] != 'N' and floor[i][j] != 'N':
                    floor[i][j].set_door('up') 
            
            if check_coord(floor, i, j + 1):
                if floor[i][j + 1] != 'N' and floor[i][j] != 'N':
                    floor[i][j].set_door('right')
            
            if check_coord(floor, i, j - 1):
                if floor[i][j - 1] != 'N' and floor[i][j] != 'N':
                    floor[i][j].set_door('left')
    
    return floor, player, player_group



def game_run():
    true_run = True
    number_of_floor = 0
    with open('data\\record.txt', 'r', encoding='utf-8') as record:
        max_record = record.read()

    while true_run:
        number_of_floor += 1
        run = True
        display_w = 800
        display_h = 600
        display = pygame.display.set_mode((display_w, display_h))
        clock = pygame.time.Clock()
        font = pygame.font.Font('data\\game_font.ttf', 25)
        text_of_num_floor =  font.render(f"{number_of_floor} Этаж", True, (255, 255, 255))

        pygame.draw.rect(display, (0, 0, 0), (0, 0, 800, 600))
        labirint, player, player_group = labirint_creator(display)
        player.set_labirint(labirint)
        player.set_room(labirint[player.room_x][player.room_y])
        player.set_game_run(run)
        time = 0
        text_of_start = BegginingText(number_of_floor)
        health_img = pygame.image.load('Images\\objects\\player\\health.png').convert()
        mover = 1
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit()
                   quit()

            display.fill((0, 0, 0))
            for character in player_group:
                character.move(labirint[player.room_x][player.room_y].walls)
            if (len(player_group) == 2 and player.room.room_type != 'clone') or len(player_group) > 2:
                player_group = pygame.sprite.Group()
                player_group.add(player)
                if player.room.room_type == 'clone':
                    clone_x = randrange(1, len(player.room.room_type) - 1)
                    clone_y = randrange(1, len(player.room.room_type) - 1)
                    while player.room.floor[clone_y][clone_x].get_item() is not None:
                        clone_x = randrange(1, len(player.room.room_type) - 1)
                        clone_y = randrange(1, len(player.room.room_type) - 1)
                    player_group.add(Clone(player_group, x=clone_x, y=clone_y, 
                                         room_x = 0,room_y = 0))
                player.change_group(player_group)
            labirint[player.room_x][player.room_y].show_floor(display, player_group)
            pygame.draw.rect(display, (0, 0, 0), (0, 0, 70, 70))
            player_group.draw(display)
            run = player.game_run
            if player.health <= 0:
                true_run = False
                run = False
                with open('data\\record.txt', 'w', encoding='utf-8') as record:
                    if number_of_floor - 1 > int(max_record):
                        record.write(str(number_of_floor - 1))
                    else:
                        record.write(max_record)
            elif player.health == 1:
                mover *= -1
            
            for hp in range(player.health):
                display.blit(health_img, (30 + 25 * hp + mover, 30 + mover))

            for item in range(len(player.items)):
                display.blit(player.items[item].image, (0, 100 + 50 * item))
            
            if text_of_start.time > 0:
                text_of_start.draw(display)
            display.blit(text_of_num_floor, (600, 25))
            pygame.display.flip()
            clock.tick(80)
            pygame.display.update()

    death_menu_run = True
    hint_text = font.render(f"Нажмите любую клавишу, чтобы выйти в меню.", True, (255, 255, 255))
    score_text = font.render(f"Этажей пройдено: {number_of_floor - 1}", True, (255, 255, 255))
    file = open('data\\record.txt', 'r', encoding='utf-8')
    max_score_text = font.render(f"Лучший счёт: {file.read()}", True, (255, 255, 255))
    file.close()
    while death_menu_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                death_menu_run = False
            display.fill((0, 0, 0))
            display.blit(score_text, (150, 200))
            display.blit(max_score_text, (150, 250))
            display.blit(hint_text, (150, 300))
            pygame.display.flip()
            clock.tick(80)
            pygame.display.update()
        

if __name__ == '__main__':
    display_w = 800
    display_h = 600
    display = pygame.display.set_mode((display_w, display_h))
    menu = pygame_menu.Menu('NotRogueLike', 600, 400, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Играть!', game_run)
    menu.add.button('О Программе', about_program)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(display)
    