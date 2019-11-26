from Vector import *
from GeometricObject import *
from pygame.rect import Rect
import math as m
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
        self.bounds = self.bounds.move(self.speed.x, self.speed.y)

    @abstractmethod
    def draw(self):
        pass


class Heroes(DinamicObject):

    def __init__(self, x, y, r, speed, color):
        super().__init__(x, y, r, speed, color)
        self.target_vector = Vector(0, 0) #нулевой вектор обозначает отсутствие цели
        self.live = True
        self.hands = []
        self.exist_hands = False
        self.exist_target = False
        #self.hands = self.get_hands(target_vector, self.x, self.y, self.r)

    def move(self):
        super().move()

    def draw(self, surface):
        #зачем int()
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.r))
        #голубым цветом откладывает вектор скорости от центра
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
                         self.target_vector.turn(30).y + self.y, k*self.r)
            hand2 = Ball(self.target_vector.turn(-30).x + self.x,
                         self.target_vector.turn(-30).y + self.y, k*self.r)
        else:
            hand1 = Ball(self.target_vector.turn(30).x + self.x,
                         self.target_vector.turn(30).y + self.y, k*self.r)
            hand2 = Ball(self.target_vector.turn(-30).x + self.x,
                         self.target_vector.turn(-30).y + self.y, k*self.r)
        self.hands.append(hand1)
        self.hands.append(hand2)
        return self.hands

    def draw_hands(self, surface):
        for hand in self.hands:
            print(self.x, int(hand.x))
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
