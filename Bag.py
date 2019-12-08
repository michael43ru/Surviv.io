from DinamicObject import *
from abc import ABC, abstractmethod
from Vector import *


class Bag(ABC):
    @abstractmethod
    def __init__(self):
        self.bombs_size = None
        self.bullets_size = None
        self.bullets = []
        self.bombs = []
        self.adrenalin = False
        self.bandage = False
        self.next_bullet = None
        self.next_bomb = None
        self.bombs_exist = False
        self.bullets_exist = False
        self.color = None


    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass


class StandartBag(Bag):
    def __init__(self):
        self.bullets_size = 10
        self.bombs_size = 1
        self.bullets = []
        self.bombs = []
        self.adrenalin = False
        self.bandage = False
        self.next_bullet = None
        self.next_bomb = None
        self.bombs_exist = False
        self.bullets_exist = False
        self.color = (150, 75, 0)

    def draw(self, surface, player):
        pygame.draw.circle(surface, self.color,
                           (int(player.x - player.target_vector.normalized.x),
                            int(player.y - player.target_vector.normalized.y)),
                           int(0.7 * player.r))

    def get_bullets(self, type):
        if type == "simple":
            for i in range(self.bullets_size):
                self.bullets.append(SimpleShot())
        if type == "line":
            for i in range(self.bullets_size):
                self.bullets.append(TripleShot())
        if type == "divergent":
            for i in range(self.bullets_size):
                self.bullets.append(DivergentShot())
        self.next_bullet = None

    def get_bomb(self):
        pass

    def update(self):
        pass

    def update_next_bullet(self):
        pass

