import pygame
from pyautogui import moveTo
import pyautogui
import os

pyautogui.FAILSAFE = False
#Создание уровней по тексту
def lvler(b, scr):
    print(b + '\n')
    exit = [0, 0]
    if '*' in b:
        b, exit = b.split('*')[0], b.split('*')[1]
    c = [[int(i) for i in i.split(' ')] for i in b.split('\n') if i != '']
    a = []
    for i in c:
        pygame.draw.rect(scr, (0, 0, 255), ((i[0], i[1]), (i[2], i[3])), 1)
        a.append(i)
    exit = [int(i) for i in exit.split('+')]
    if len(exit) != 0:
        pygame.draw.rect(scr, ("white"), (exit, (20, 20)))
    pygame.display.flip()
    return a, exit
#Сам геймплэй
def play(spis):
    pyautogui.FAILSAFE = False
    size = width, height = 501, 501
    scr = pygame.display.set_mode(size)
    print(spis)
    a, pos = lvler(spis, scr)
    moveTo(400, 400)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            # Анти чит
            if event.type == pygame.VIDEOEXPOSE:
                moveTo(400, 400)
            if event.type == pygame.KEYDOWN:
                #Выход в меню
                if event.key == pygame.K_ESCAPE:
                    return True
                if event.key == pygame.K_TAB and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    return
            if event.type == pygame.MOUSEMOTION:
                print(event.pos)
                # Соприкосновение с финишем
                if event.pos[0] <= pos[0] + 20 and event.pos[0] >= pos[0] and event.pos[1] <= pos[1] + 20 \
                        and event.pos[1] >= pos[1]:
                    moveTo(0, 0)
                    return
                # Прикосновения к блокам
                for i in a:
                    if i[2] >= 0 and i[3] >= 0:
                        if event.pos[0] > i[0] and event.pos[0] < i[0] + i[2] and event.pos[1] > i[1] \
                                and event.pos[1] < i[1] + i[3]:
                            moveTo(400, 400)
                    elif i[2] <= 0 and i[3] >= 0:
                        if event.pos[0] < i[0] and event.pos[0] > i[0] + i[2] and event.pos[1] > i[1] \
                                and event.pos[1] < i[1] + i[3]:
                            moveTo(400, 400)
                    elif i[2] >= 0 and i[3] <= 0:
                        if event.pos[0] > i[0] and event.pos[0] < i[0] + i[2] and event.pos[1] < i[1] \
                                and event.pos[1] > i[1] + i[3]:
                            moveTo(400, 400)
                    elif i[2] <= 0 and i[3] <= 0:
                        if event.pos[0] < i[0] and event.pos[0] > i[0] + i[2] and event.pos[1] < i[1] \
                                and event.pos[1] > i[1] + i[3]:
                            moveTo(400, 400)
        pygame.draw.rect(scr, ("white"), (pos, (20, 20)))
        for i in a:
            pygame.draw.rect(scr, (0, 0, 255), ((i[0], i[1]), (i[2], i[3])), 1)

        pygame.display.flip()

#Редактор уровней
def editor():
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 501, 501
    screen = pygame.display.set_mode(size)

    intro_text = ["Поздравляем!",
                  "Вы победили!",
                  "Нажмите любую клавишу,",
                  "чтобы выйти"]

    running = True
    passing = False
    screen2 = pygame.Surface(screen.get_size())
    x1, y1, w, h = 0, 0, 0, 0
    a = []
    pos = []
    cir = True
    v = 100
    o = False
    drawing = False  # режим рисования выключен

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                # Отмена действия
                if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    screen2.fill((0, 0, 0))
                    b = []
                    for i in range(len(a) - 1):
                        pygame.draw.rect(screen2, (0, 0, 255), ((a[i][0], a[i][1]), (a[i][2], a[i][3])), 1)
                        pygame.display.flip()
                        b.append(a[i])
                    a = b
                # Загрузка уровня из текста
                if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    o = open("data\coordinates.txt", encoding="utf8")
                    b = o.read()
                    o.close()
                    a, pos = lvler(b, screen2)
                    cir = False
                # Поставить финиш
                if event.key == pygame.K_e:
                    pos = pygame.mouse.get_pos()
                    if cir:
                        pos = [i for i in pos]
                        pygame.draw.rect(screen2, ("white"), (pos, (20, 20)))
                    cir = False
                    o = True
                # Загрузка в текстовый файл уровня
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    b = open("data\coordinates.txt", 'w')
                    for i in a:
                        b.write(' '.join([str(i1) for i1 in i]) + "\n")
                    b.write('*' + '+'.join([str(i) for i in pos]))
                    b.close()
                # Запуск игры
                if event.key == pygame.K_SPACE:
                    print(999)
                    moveTo(0, 0)
                    passing = not passing
                # Чтобы не читерили
            if event.type == pygame.VIDEOEXPOSE and passing:
                moveTo(0, 0)
                passing = not passing
            # Рисование
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not passing:
                    drawing = True
                    x1, y1 = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                # сохраняем нарисованное (на втором холсте)
                if drawing:
                    screen2.blit(screen, (0, 0))
                    a.append([x1, y1, w, h])
                    drawing = False
                    x1, y1, w, h = 0, 0, 0, 0


            if event.type == pygame.MOUSEMOTION:
                # запоминаем текущие размеры
                if drawing:
                    w, h = event.pos[0] - x1, event.pos[1] - y1
                if passing:
                    if not cir:
                        pygame.draw.rect(screen2,(255, 255, 255), ((240, 240), (20, 20)))
                    # Соприкосновение с финишем
                    if event.pos[0] <= pos[0] + 20 and event.pos[0] >= pos[0] and event.pos[1] <= pos[1] + 20\
                            and event.pos[1] >= pos[1]:
                        moveTo(400, 400)
                    # Соприкосновение с блоками
                    for i in a:
                        if i[2] >= 0 and i[3] >= 0:
                            if event.pos[0] > i[0] and event.pos[0] < i[0] + i[2] and event.pos[1] > i[1]\
                                    and event.pos[1] < i[1] + i[3]:
                                moveTo(0, 0)
                        elif i[2] <= 0 and i[3] >= 0:
                            if event.pos[0] < i[0] and event.pos[0] > i[0] + i[2] and event.pos[1] > i[1]\
                                    and event.pos[1] < i[1] + i[3]:
                                moveTo(0, 0)
                        elif i[2] >= 0 and i[3] <= 0:
                            if event.pos[0] > i[0] and event.pos[0] < i[0] + i[2] and event.pos[1] < i[1]\
                                    and event.pos[1] > i[1] + i[3]:
                                moveTo(0, 0)
                        elif i[2] <= 0 and i[3] <= 0:
                            if event.pos[0] < i[0] and event.pos[0] > i[0] + i[2] and event.pos[1] < i[1]\
                                    and event.pos[1] > i[1] + i[3]:
                                moveTo(0, 0)
        #Обновление
        if o:
            screen2.fill((0, 0, 0))
            i = 0
            d = v / 1000
            if not cir:
                pygame.draw.rect(screen2, ("white"), (pos, (20, 20)))
            for i in a:
                pygame.draw.rect(screen2, (0, 0, 255), ((i[0], i[1]), (i[2], i[3])), 1)


        screen.fill(pygame.Color('black'))
        screen.blit(screen2, (0, 0))
        if drawing:  # и, если надо, текущий прямоугольник
            pygame.draw.rect(screen, (0, 0, 255), ((x1, y1), (w, h)), 1)
        pygame.display.flip()
    pygame.quit()