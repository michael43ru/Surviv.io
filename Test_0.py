import pygame

import random

import time

from random import randrange as rnd, choice

from os import path

# from Vector import *

# from GeometricObject import *

from pygame.rect import Rect

from abc import ABC, abstractmethod

import math


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def mult_by_scalar(self, l):
        self.x *= l
        self.y *= l
        return self

    def __add__(self, other):
        vector = Vector(self.x + other.x, self.y + other.y)
        return vector

    def __sub__(self, other):
        vector = Vector(self.x - other.x, self.y - other.y)
        return vector

    def __neg__(self):
        vector = Vector(- self.x, - self.y)
        return vector

    def __abs__(self):
        if self.x != 0 and self.y != 0:
            return math.sqrt(self.x ** 2 + self.y ** 2)
        else:
            print("У вас нулевой вектор!")

    def proection(self, other):
        try:
            return other.lambdamultiplication(other.__mul__(self) / (other.__abs__() ** 2))
        except ZeroError as e:
            print("Кажется, у вас есть нулевой вектор!")

    def draw(self, surface, color, x, y):
        #откладывает вектор (255, 255, 255) цвета от точки (x, y)
        pygame.draw.aaline(surface, color, [x, y], [x + self.x, y + self.y])

    def normalized(self):
        #нормировка(приведение к единичному модулю)
        return self.mult_by_scalar(1 / self.__abs__())

    def is_null_vector(self):
        if self.x == 0 and self.y == 0:
            return True
        else:
            return False

    def turn(self, degree):
        #поворот против часовой стрелки
        radian = degree * math.pi / 180
        x1 = self.x * math.cos(radian) - self.y * math.sin(radian)
        y1 = self.x * math.sin(radian) + self.y * math.cos(radian)
        return Vector(x1, y1)


class DinamicObject(ABC):

    @abstractmethod
    def __init__(self, x, y, r, speed, color):
        self.bounds = Rect(x, y, r, r) # как бы границы объекта(квадрат вокруг нашей круглой фигуры)
        self.speed = speed
        self.color = color
        
        # координаты центра объекта
        
        self.x = x + r / 2
        self.y = y + r / 2
        self.r = r

    @abstractmethod
    def move(self):
        self.x += self.speed.x
        self.y += self.speed.y
        self.bounds = self.bounds.move(self.speed.x, self.speed.y)

    @abstractmethod
    def draw(self):
        pass


class Heroes(DinamicObject):

    def __init__(self, x, y, r, speed, color):
        super().__init__(x, y, r, speed, color)
        self.target_vector = Vector(0, 0) # нулевой вектор обозначает отсутствие цели
        self.live = True
        self.hands = []
        self.exist_hands = False
        self.exist_target = False
        # self.hands = self.get_hands(target_vector, self.x, self.y, self.r)

    def move(self):
        super().move()

    def draw(self, surface):
        
        # зачем int()
        
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.r))

        # голубым цветом откладывает вектор скорости от центра
        
        if not self.speed.is_null_vector():
            self.speed.draw(surface, (0, 70, 225), self.x, self.y)
        if self.exist_hands:
            self.draw_hands(surface)

    def hands_hit(self):
        pass

    def get_hands(self):
        
        k = 0.25
        self.exist_hands = True
        if self.target_vector.is_null_vector():

            hand1 = Ball(self.target_vector.turn(30).x + self.x,
                         self.target_vector.turn(30).y + self.y, k * self.r)
            hand2 = Ball(self.target_vector.turn(-30).x + self.x,
                         self.target_vector.turn(-30).y + self.y, k * self.r)
        else:
            hand1 = Ball(self.target_vector.turn(30).x + self.x,
                         self.target_vector.turn(30).y + self.y, k * self.r)
            hand2 = Ball(self.target_vector.turn(-30).x + self.x,
                         self.target_vector.turn(-30).y + self.y, k * self.r)
        self.hands.append(hand1)
        self.hands.append(hand2)
        return self.hands

    def draw_hands(self, surface):
        
        for hand in self.hands:
            # print(self.x, int(hand.x))
            pygame.draw.circle(surface, self.color, (int(hand.x), int(hand.y)), int(hand.r))
            pygame.draw.circle(surface, (0, 0, 0), (int(hand.x), int(hand.y)), int(hand.r), int(0.15*hand.r))

    def get_target_vector(self, x, y):
        self.exist_target = True
        self.target_vector = Vector(x - (self.x - self.r), y - (self.y - self.r)).normalized().mult_by_scalar(self.r)

    def draw_target_vector(self, surface):
        #черным цветом обозначен вектор цели
        self.target_vector.draw(surface, (0, 0, 0), self.x, self.y)

    def delete_target(self):
        self.exist_target = False
        self.target_vector = Vector(0, 0)

    def delete_hands(self):
        self.exist_hands = False
        self.hands = []


class Player(Heroes):
    pass


class Bots(Heroes):
    pass


class Figure:
    
    # Задаются координаты центра фигуры
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Ball(Figure):
    def __init__(self, x, y, r):
        super().__init__(x, y, r, r)
        self.r = r


class Static_objects:
    def __init__(self, x, y, r, number_of_type, color):
        self.x = x
        self.y = y
        self.r = r
        self.type = number_of_type # у каждого типа объекта будет свой номер
        self.live = 10 # число жизней до разрушения, если что можно поменять
        self.color = color

    def collision_with_gamer(self, obj): # при столкновении с игроком, не пропускать игрока
        if self.type == 1: # куст дерево или что то круглое
            if math.hypot((self.x - obj.x), (self.y - obj.y)) <= (self.r + obj.r):
                if self.x == obj.x:
                    if self.y < obj.y:
                        return 0.5 * math.pi
                    else:
                        return -0.5 * math.pi
                elif self.y == obj.y:
                    if self.x < obj.x:
                        return 0
                    else:
                        return -math.pi
                else:
                    return math.atan((obj.y - self.y) / (obj.x - self.x))
            else:
                return 100 # если выводиться 100 это значит что нет столкновения, для других чисел выводится значение угла
                           # поворота объекта относительно игрока
        if self.type == 2: # ящик стена или что то прямоугольное
            pass
            

class Solid_objects(Static_objects): # неразрушаемые объекты
    
    def create_tree(self): # создание дерева или куста, для каждого объекта будет отдельная функция создания
        pass

    def create_box(self): # при создании прикрепить к нему предмет со своим номером
        pass

    def collision_with_bullet(self): # при столкновении уничтожить пулю
        pass

    def collision_with_fighter(self): # если это ящик, то уменьшить колво жизней, для остальных не уменьшать (кулаки)
        pass

    def open_box(self): # при открытии ящика уничтожить его, человеку присвоить предмет
        pass


class Not_solid_objects(Static_objects):
    def create_stone(self):
        pass

    def collision_with_bullets(self): # при столкновении с пулей уничтожить пулю, уменьшить радиус камня
        pass


class Red_zone:
    def __init__(self):
        self.x = rnd(0.3 * s, 0.7 * s)
        self.y = rnd(0.3 * s, 0.5 * s)
        self.r = 0.5 * s
        self.t = time.time()

        # self.image = pg.image.load(path.join(img_dir, "Red_zone.png")).convert()
        self.image = pg.transform.scale(red_zone_img, (1000, 1000))
        self.image.set_colorkey(white)
        self.image_rect = self.image.get_rect()

    def get_center(self):
        self.r = self.r / 2
        self.x = rnd(-self.r + self.x, self.r + self.x)
        self.y = rnd(-(self.r ** 2 - self.x ** 2) + self.y,
                     (self.r ** 2 - self.x ** 2) + self.y)
        self.R = self.r * 3
        
    def reduction(self): # Не доделано
        self.R -= self.v


class Map:

    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.width = dx
        self.height = dy
        self.color = color
        
    def draw(self):
        self.id = pygame.draw.polygon(screen, self.color, ((self.x + width / 2, self.y + height / 2),
                                                           (self.x + self.width + width / 2, self.y + height / 2),
                                                           (self.x + self.width + width / 2, self.y + self.height + height / 2),
                                                           (self.x  + width / 2, self.y + self.height + height / 2)))


# class World:
     
static_objects = []
dinamic_objects = []

bots = []
boxes = []
bushes = []
trees = []
stones = []
bullets = []
bombs = []
drops = []
taken_objects = []
# player = Player()

# dinamic_objects.extend([bots, bullets, bombs, player])
dinamic_objects.extend([bots, bullets, bombs])
static_objects.extend([boxes, trees, stones])


width = 800
height = 600
fps = 30

# Задаем цвета

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
color_grass = [160, 255, 100]
color_water = [70, 120, 255]

# Создаем игру и окно

pygame.init()
pygame.mixer.init() # Звук
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

s = 1000 # сторона карты

'''img_dir = path.join(path.dirname(__file__), 'img')
red_zone_img = pg.image.load(path.join(img_dir, "Red_zone.png")).convert()'''

v = Vector(0, 0)
player = Player(width / 2, height / 2, 20, v, (0, 0, 0)) # здесь координаты игрока на экране
player.get_target_vector(0, -1)
player.get_hands()
center_x = rnd(0.01 * s, 0.99 * s) # координаты игрока в мире
center_y = rnd(0.01 * s, 0.99 * s)

screen.fill(color_water)

'''water = pygame.draw.polygon(screen, color_water, ((width / 2, height / 2),
                                                  (s + width / 2, height / 2),
                                                  (s + width / 2, s + height / 2),
                                                  (width / 2, s - height / 2)))'''

'''grass = pygame.draw.polygon(screen, color_grass, ((0.02 * s  + width / 2 - center_x, 0.02 * s + height / 2 - center_y),
                                                  (0.98 * s + width / 2 - center_x, 0.02 * s + height / 2 - center_y),
                                                  (0.98 * s + width / 2 - center_x, 0.98 * s + height / 2 - center_y),
                                                  (0.02 * s + width / 2 - center_x, 0.98 * s + height / 2 - center_y)))'''

grass = Map(0.02 * s - center_x, 0.02 * s - center_y, 0.96 * s, 0.96 * s, color_grass)

# Цикл игры

running = True
while running:
    
    # Держим цикл на правильной скорости
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_a:
                player.speed.x -= 8
            if key == pygame.K_d:
                player.speed.x += 8
            if key == pygame.K_w:
                player.speed.y -= 8
            if key == pygame.K_s:
                player.speed.y += 8
                
        if event.type == pygame.KEYUP:
            key = event.key
            if key == pygame.K_a:
                player.speed.x += 8
            if key == pygame.K_d:
                player.speed.x -= 8
            if key == pygame.K_w:
                player.speed.y += 8
            if key == pygame.K_s:
                player.speed.y -= 8

    (x, y) = pygame.mouse.get_pos()
    player.get_target_vector(x, y)
    player.delete_hands()
    player.get_hands()

    for a in static_objects:
        for b in a:
            b.x -= player.speed.x
            b.y -= player.speed.y
    for a in dinamic_objects:
        for b in a:
            b.x -= player.speed.x
            b.y -= player.speed.y
    # water.x -= player.speed.x
    # water.y -= player.speed.y
    grass.x -= player.speed.x
    grass.y -= player.speed.y
    center_x += player.speed.x
    center_y += player.speed.y

    '''water = pygame.draw.polygon(screen, color_water, ((water.x, water.y), (water.x + s, water.y),
                                                      (water.x + s, water.y + s), (water.x, water.y + s)))'''
    screen.fill(color_water)
    '''grass = pygame.draw.polygon(screen, color_grass, ((grass.x, grass.y),
                                                      (0.98 * s + grass.x, grass.y),
                                                      (0.98 * s + grass.x, 0.98 * s + grass.y),
                                                      (grass.x, 0.98 * s + grass.y)))'''
    grass.draw()
    
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
