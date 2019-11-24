import pygame


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
            return m.sqrt(self.x ** 2 + self.y ** 2)
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

    def unit_vector(self, x, y):
        #единичный вектор
        unit = 10 # единица
        v = Vector(x, y)
        v = v.mult_by_scalar(1 / v.__abs__())
        v.mult_by_scalar(unit)
        return v

    def null_vector(self):
        if self.x == 0 and self.y == 0:
            return True
        else:
            return False
