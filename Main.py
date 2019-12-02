from DinamicObject import *
from Vector import *
import pygame
from StaticObject import *
from RedZone import *
from Map import *
from random import randrange as rnd
import Game


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
