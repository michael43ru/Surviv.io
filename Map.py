class Map:

    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.width = dx
        self.height = dy
        self.color = color

    def draw(self):
        self.id = pygame.draw.polygon(screen, self.color, ((self.x + width / 2, self.y + height / 2),
                                                           (self.x + self.width + width / 2, self.y + height / 2),
                                                           (self.x + self.width + width / 2, self.y + self.height + height / 2),
                                                           (self.x  + width / 2, self.y + self.height + height / 2)))
