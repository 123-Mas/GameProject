import pygame
from pyautogui import moveTo
import os
import sys
import Lvl_editor


FPS = 50
#Уничтожение
def terminate():
    pygame.quit()
    sys.exit()

#Загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

#Конец
def finish():
    intro_text = ["Поздравляем!",
                  "Вы победили!",
                  "Нажмите любую клавишу,",
                  "чтобы выйти"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                start_screen()
        pygame.display.flip()

#Начало
def start_screen():
    intro_text = ["Kursor.exe", "",
                  "Вы должны провести курсор в белый квадрат,",
                  "не задевая синие прямоугольники",
                  "1 - перейти к прохождению игры",
                  "2 - перейти в редактор уровней",
                  "3 - выйти из игры",
                  "",
                  "Нажмите на соответствующую цифру",
                  "на своей клавиатуре",
                  "",
                  "Управление в редакторе:",
                  "E - поставить финиш",
                  "Ctrl + C - сохранить",
                  "Ctrl + V - загрузить",
                  "Space - запустить игру"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 23)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    o = open("data\Lvl_coords.txt", encoding="utf8")
                    b = o.read().split('\n\n')
                    o.close()
                    for i in b:
                         if Lvl_editor.play(i) is True:
                             start_screen()
                    finish()
                    return  # начинаем игру
                if event.key == pygame.K_2:
                    Lvl_editor.editor()
                    start_screen()
                    # начинаем игру
                if event.key == pygame.K_3:
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Движущийся круг 2')
size = WIDTH, HEIGHT = 501, 501
screen = pygame.display.set_mode(size)
start_screen()
pygame.quit()