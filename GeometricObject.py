import pygame


class Figure:
    #Задаются координаты левого верхнего угла
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Ball(Figure):
    #Задаются координаты центра окружности
    def __init__(self, x, y, r):
        super().__init__(x, y, r, r)
        self.r = r


class Ellipse(Figure):
    #Задаются координаты левого верхнего угла
    pass


class SimpleGun:
    def __init__(self, x1, y1, x2, y2):
        #самая простая реализация оружия -- отрезок
        #в качестве его параметров -- начало и конец
        self.x_start = x1
        self.y_start = y1
        self.x_end = x2
        self.y_end = y2

    def draw(self, surface):
        pygame.draw.line(surface, (0, 0, 0), [self.x_start, self.y_start], [self.x_end, self.y_end], 6)
