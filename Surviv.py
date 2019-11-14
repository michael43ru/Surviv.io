from abc import ABC, abstractmethod
import pygame as pg

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


class Actor(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def move_land(self):
        pass


class DinamicObject(Actor):




