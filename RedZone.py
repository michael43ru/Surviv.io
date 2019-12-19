import pygame
import math


class Red_zone:
    def __init__(self, x, y , r, sc):
        self.x = x
        self.y = y
        self.r = r
        self.v = 5

    def draw(self, sc):
        self.image = pygame.draw.circle(sc, (100, 0, 0), (self.x, self.y), int(self.r), 10)

    def hit(self, obj):
        if math.hypot((self.x - obj.x), (self.y - obj.y)) <= self.r:
            obj.health -= 0.5
