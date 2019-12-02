import pygame


class Map:

    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.width = dx
        self.height = dy
        self.color = color

    def draw(self, screen):
        self.id = pygame.draw.polygon(screen, self.color, ((self.x, self.y),
                                                           (self.x + self.width, self.y),
                                                           (self.x + self.width, self.y + self.height),
                                                           (self.x, self.y + self.height)))
