from abc import ABC, abstractmethod

class Bag(ABC):
    @abstractmethod
    def __init__(self):
        self.bombs_size = None
        self.bullets_size = None
        self.bullets = []
        self.bombs = []
        self.adrenalin = None
        self.bandage = None
        self.next_bullet = None
        self.next_bomb = None
        self.bombs_exist = False
        self.bullets_exist = False


    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass


class StandartBag(ABC):
    self.standart_bullets_size = 10
    self.standart_bombs_size = 1
    def __init__(self):
        self.bullets_size = self.standart_bullets_size
        self.bombs_size = self.standart_bombs_size


class Bomb:
    pass
