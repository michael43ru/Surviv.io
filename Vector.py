import pygame
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
        if self.x != 0 or self.y != 0:
            return math.sqrt(self.x ** 2 + self.y ** 2)
        else:
            print("У вас нулевой вектор!")

    def projection(self, other):
        return other.mult_by_scalar(other.__mul__(self) / (other.__abs__() ** 2))

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
        x1 = self.x*math.cos(radian) - self.y*math.sin(radian)
        y1 = self.x*math.sin(radian) + self.y*math.cos(radian)
        return Vector(x1, y1)


