from Vector import *
from pygame.rect import Rect
from abc import ABC, abstractmethod

class DinamicObject(ABC):

    @abstractmethod
    def __init__(self, x, y, r, speed, color):
        self.bounds = Rect(x, y, r, r) #как бы границы объекта(квадрат вокруг нашей круглой фигуры)
        self.speed = speed
        self.color = color
        #координаты центра объекта
        self.x = x + r / 2
        self.y = y + r / 2
        self.r = r

    @abstractmethod
    def move(self):
        self.x += self.speed.x
        self.y += self.speed.y
        self.bounds += self.bounds.move(self.speed.x, self.speed.y)

    @abstractmethod
    def draw(self):
        pass


class Heroes(DinamicObject):

    def __init__(self, x, y, r, speed, color):
        super().__init__(x, y, 1.1 * r, speed, color)
        self.target_vector = None
        self.live = True
        self.hands = self.get_hands(target_vector, self.x, self.y, self.r)

    def move(self, surface, event):
        print("Я двигаюсь!!")

    def draw(self, surface):
        print(type(self.x))
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.r)
        #голубым цветом откладывает вектор скорости от центра
        if not self.speed.null_vector():
            self.speed.draw(surface, (0, 70, 225), self.x, self.y)

        self.draw_hands(surface, self.hands)

    def hands_hit(self):
        pass

    def get_hands(self, target_vector, x, y, r):
        hands = []
        #геометрия
        return hands

    def draw_hands(self, surface, hands):
        for hand in hands:
            pygame.draw.circle(surface, self.color, (hand.x, hand.y), hand.r)

    def get_target(self, x, y):
        target_vector = unit_vector(x - (self.x - self.r), y - (self.y - self.r))
        return target_vector

    def draw_target(self, target_vector, surface):
        #черным цветом обозначен вектор цели
        target_vector.draw(surface, (0, 0, 0), self.x, self.y)


class Player(Heroes):
    pass


class Bots(Heroes):
    pass
