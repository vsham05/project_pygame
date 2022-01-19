import pygame

pygame.init()
pygame.font.init()


def about_programm():
    run = True
    
    sc = pygame.display.set_mode((800, 600))
    sc.fill((0, 0, 0))
    button = pygame.Rect(10, 10, 400, 50)

    f = pygame.font.SysFont('serif', 30)
    text = f.render("Управление:", False, (0, 150, 0))

    text1 = f.render("WASD - передвижение", False, (0, 150, 0))

    text5 = f.render("Правила:", False, (0, 150, 0))

    text6 = f.render("Игрок бегает по лабиринту и ", False, (0, 150, 0))

    text7 = f.render("выполняет задания, за которые", False, (0, 150, 0))

    text8 = f.render("он получает кристаллы.", False, (0, 150, 0))

  
    text9 = f.render("В игре очень много этажей, которые", False, (0, 150, 0))

    text10 = f.render("игрок попытается преодолеть...", False, (0, 150, 0))

    text11 = f.render("Для прохождения на следующий этаж,", False, (0, 150, 0))

    text12 = f.render("вам нужно собрать 3 кристалла.", False, (0, 150, 0))

    sc.blit(text, (10, 60))
    sc.blit(text1, (10, 110))
    sc.blit(text5, (10, 160))
    sc.blit(text6, (10, 210))
    sc.blit(text7, (10, 260))
    sc.blit(text8, (10, 310))
    sc.blit(text9, (10, 360))
    sc.blit(text10, (10, 410))
    sc.blit(text11, (10, 460))
    sc.blit(text12, (10, 510))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 10 < event.pos[0] < 410:
                    if 10 < event.pos[1] < 60:
                        run = False

        font = pygame.font.SysFont('serif', 48)
        text = font.render('Вернуться в меню', True, (200, 0, 0))
        pygame.draw.rect(sc, (0, 130, 0), button)
        sc.blit(text, (15, 5))

        pygame.display.update()

