import pygame as pg

import random

import time

from random import randrange as rnd, choice

from os import path


width = 360
height = 480
fps = 30

# Задаем цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
color_trava = [160, 255, 100]
color_voda = [70, 120, 255]


# Создаем игру и окно
pg.init()
pg.mixer.init() # Звук
screen = pg.display.set_mode((width, height))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

'''class River:'''
s = 100000
'''pole = '''

img_dir = path.join(path.dirname(__file__), 'img')

class Red_zone:
    def __init__(self):
        self.x = rnd(0.4 * s, 0.6 * s)
        self.y = rnd(0.4 * s, 0.6 * s)
        self.r = 0.4 * s
        self.t = time.time()

        self.image = pg.image.load(path.join(img_dir, "Red_zone.png")).convert()
        self.image.set_colorkey(white)
        self.image_rect = self.image.get_rect()

    def center(self):
        self.r = self.r / 2
        self.x = rnd(-self.r + self.x, self.r + self.x)
        self.y = rnd(-(self.r ** 2 - self.x ** 2) + self.y,
                     (self.r ** 2 - self.x ** 2) + self.y)
        self.R = self.r * 3
        
    def reduction(self):
        self.R -= self.v
        


# камера
'''for a in static_objects:
    for b in a:
        b.x -= player.vx
        b.y -= player.vy
for a in dinamic_objects:
    for b in a:
        b.x -= player.vx
        b.y -= player.vy'''

zone = Red_zone()
# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(fps)
    # Ввод процесса (события)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False

    # Обновление
    
    # Рендеринг
    screen.fill(color_trava)
    screen.blit(zone.image, zone.image_rect)
    # После отрисовки всего, переворачиваем экран
    pg.display.flip()

pg.quit()
