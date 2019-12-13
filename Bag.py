from DinamicObject import *
from abc import ABC, abstractmethod
from Vector import *


class Bag(ABC):
    @abstractmethod
    def __init__(self):
        self.bombs_size = None
        self.bullets_size = None
        self.adrenalin = False
        self.bandage = False
        self.color = None

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass


class StandartBag(Bag):
    def __init__(self):
        self.bombs_size = 1
        self.bullets_size = 10
        self.bombs_number = 0
        self.bullets_number = 0
        self.bullet_type = "simple"
        self.adrenalin = False
        self.bandage = False
        self.color = (150, 75, 0)

    def draw(self, surface, player):
        k = 15
        pygame.draw.circle(surface, self.color,
                           (int(player.x - k*player.target_vector.normalized().x),
                            int(player.y - k*player.target_vector.normalized().y)),
                           int(0.8 * player.r))

    def get_bullets(self, type):
        self.bullet_type = type
        self.bullets_number = self.bullets_size

    def get_bomb(self):
        pass

    def update(self):
        pass
