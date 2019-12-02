from DinamicObject import *
from Vector import *
import pygame
from StaticObject import *
from RedZone import *
from Map import *
from random import randrange as rnd


class Game:

    def __init__(self):
        self.static_objects = []
        self.dinamic_objects = []

        self.bots = []
        self.boxes = []
        self.bushes = []
        self.trees = []
        self.stones = []
        self.bullets = []
        self.bombs = []
        self.drops = []
        self.taken_objects = []

        self.dinamic_objects.extend([self.bots, self.bullets, self.bombs])
        self.static_objects.extend([self.boxes, self.bushes, self.trees, self.stones, self.drops])
        
        self.width = 800
        self.height = 600
        self.fps = 30
        self.len = 1000 # сторона карты

        self.center_x = rnd(0.01 * self.len, 0.99 * self.len) # координаты игрока в мире
        self.center_y = rnd(0.01 * self.len, 0.99 * self.len)

        self.true = True

        pygame.init()
        pygame.mixer.init() # Звук
        self.sc = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()

    def update(self):
        for lst in self.dinamic_objects:
            for obj in lst:
                obj.x -= player.speed.x
                obj.y -= player.speed.y

        for lst in self.static_objects:
            for obj in lst:
                obj.x -= player.speed.x
                obj.y -= player.speed.y

    def main(self):
        
        self.clock.tick(self.fps)

        self.update()

        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.true = False
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_a:
                    player.speed.x -= 8
                if key == pygame.K_d:
                    player.speed.x += 8
                if key == pygame.K_w:
                    player.speed.y -= 8
                if key == pygame.K_s:
                    player.speed.y += 8

            if event.type == pygame.KEYUP:
                key = event.key
                if key == pygame.K_a:
                    player.speed.x += 8
                if key == pygame.K_d:
                    player.speed.x -= 8
                if key == pygame.K_w:
                    player.speed.y += 8
                if key == pygame.K_s:
                    player.speed.y -= 8

        (x, y) = pygame.mouse.get_pos()
        player.get_target_vector(x, y)
        player.delete_hands()
        player.get_hands()

        for a in self.static_objects:
            for b in a:
                b.x -= player.speed.x
                b.y -= player.speed.y
        for a in self.dinamic_objects:
            for b in a:
                b.x -= player.speed.x
                b.y -= player.speed.y

        # water.x -= player.speed.x
        # water.y -= player.speed.y
        grass.x -= player.speed.x
        grass.y -= player.speed.y
        self.center_x += player.speed.x
        self.center_y += player.speed.y

        '''water = pygame.draw.polygon(screen, color_water, ((water.x, water.y), (water.x + s, water.y),
                                                          (water.x + s, water.y + s), (water.x, water.y + s)))'''
        self.sc.fill(color_water)
        '''grass = pygame.draw.polygon(screen, color_grass, ((grass.x, grass.y),
                                                          (0.98 * s + grass.x, grass.y),
                                                          (0.98 * s + grass.x, 0.98 * s + grass.y),
                                                          (grass.x, 0.98 * s + grass.y)))'''
        grass.draw(self.sc)

        player.draw(self.sc)

        pygame.display.flip()


# pygame.init()
game = Game()

# Задаем цвета

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
color_grass = [160, 255, 100]
color_water = [70, 120, 255]

'''# Создаем игру и окно

pygame.init()
pygame.mixer.init() # Звук
screen = pygame.display.set_mode((game.width, game.height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()'''

'''img_dir = path.join(path.dirname(__file__), 'img')
red_zone_img = pg.image.load(path.join(img_dir, "Red_zone.png")).convert()'''

v = Vector(0, 0)
player = Player(game.width / 2, game.height / 2, 20, v, (0, 0, 0)) # здесь координаты игрока на экране
player.get_target_vector(0, -1)
player.get_hands()

game.sc.fill(color_water)

'''water = pygame.draw.polygon(screen, color_water, ((width / 2, height / 2),
                                                  (s + width / 2, height / 2),
                                                  (s + width / 2, s + height / 2),
                                                  (width / 2, s - height / 2)))'''

'''grass = pygame.draw.polygon(screen, color_grass, ((0.02 * s  + width / 2 - center_x, 0.02 * s + height / 2 - center_y),
                                                  (0.98 * s + width / 2 - center_x, 0.02 * s + height / 2 - center_y),
                                                  (0.98 * s + width / 2 - center_x, 0.98 * s + height / 2 - center_y),
                                                  (0.02 * s + width / 2 - center_x, 0.98 * s + height / 2 - center_y)))'''

grass = Map(0.02 * game.len - game.center_x, 0.02 * game.len - game.center_y,
            0.96 * game.len, 0.96 * game.len, color_grass)

# Цикл игры

while game.true:
    game.main()

pygame.quit()
