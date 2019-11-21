from abc import ABC, abstractmethod
import pygame as pg
import Vector

class World:
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
    player = Player()

    dinamic_objects.extend([bots, bullets, bombs, player])
    static_objects.extend([boxes, trees, stones])


class DinamicObject(ABC):

    @abstractmethod
    def move_land(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def draw(self):
        pass


class Heroes(DinamicObject):
    def move_land(self):
        pass

    def delete(self):
        pass

    def __init__(self):
        pass

    def delete(self):
        pass

    def draw(self):
        pass

class Player(Heroes):

class Bots(Heroes):


def new_game():
    W = 800
    H = 600
    pygame.init()
    pygame.display.set_mode((W, H))





