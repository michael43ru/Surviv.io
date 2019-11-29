from DinamicObject import *
from Vector import *
import pygame
from StaticObject import *
from RedZone import *
from Map import *
from random import randrange as rnd, choice

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
# player = Player()

# dinamic_objects.extend([bots, bullets, bombs, player])
dinamic_objects.extend([bots, bullets, bombs])
static_objects.extend([boxes, trees, stones])


width = 800
height = 600
fps = 30

# Задаем цвета

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
color_grass = [160, 255, 100]
color_water = [70, 120, 255]

# Создаем игру и окно

pygame.init()
pygame.mixer.init() # Звук
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

s = 1000 # сторона карты

'''img_dir = path.join(path.dirname(__file__), 'img')
red_zone_img = pg.image.load(path.join(img_dir, "Red_zone.png")).convert()'''

v = Vector(0, 0)
player = Player(width / 2, height / 2, 20, v, (0, 0, 0)) # здесь координаты игрока на экране
player.get_target_vector(0, -1)
player.get_hands()
center_x = rnd(0.01 * s, 0.99 * s) # координаты игрока в мире
center_y = rnd(0.01 * s, 0.99 * s)

screen.fill(color_water)

'''water = pygame.draw.polygon(screen, color_water, ((width / 2, height / 2),
                                                  (s + width / 2, height / 2),
                                                  (s + width / 2, s + height / 2),
                                                  (width / 2, s - height / 2)))'''

'''grass = pygame.draw.polygon(screen, color_grass, ((0.02 * s  + width / 2 - center_x, 0.02 * s + height / 2 - center_y),
                                                  (0.98 * s + width / 2 - center_x, 0.02 * s + height / 2 - center_y),
                                                  (0.98 * s + width / 2 - center_x, 0.98 * s + height / 2 - center_y),
                                                  (0.02 * s + width / 2 - center_x, 0.98 * s + height / 2 - center_y)))'''

grass = Map(0.02 * s - center_x, 0.02 * s - center_y, 0.96 * s, 0.96 * s, color_grass)

# Цикл игры

running = True
while running:

    # Держим цикл на правильной скорости

    clock.tick(fps)

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
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

    for a in static_objects:
        for b in a:
            b.x -= player.speed.x
            b.y -= player.speed.y
    for a in dinamic_objects:
        for b in a:
            b.x -= player.speed.x
            b.y -= player.speed.y
    # water.x -= player.speed.x
    # water.y -= player.speed.y
    grass.x -= player.speed.x
    grass.y -= player.speed.y
    center_x += player.speed.x
    center_y += player.speed.y

    '''water = pygame.draw.polygon(screen, color_water, ((water.x, water.y), (water.x + s, water.y),
                                                      (water.x + s, water.y + s), (water.x, water.y + s)))'''
    screen.fill(color_water)
    '''grass = pygame.draw.polygon(screen, color_grass, ((grass.x, grass.y),
                                                      (0.98 * s + grass.x, grass.y),
                                                      (0.98 * s + grass.x, 0.98 * s + grass.y),
                                                      (grass.x, 0.98 * s + grass.y)))'''
    grass.draw(screen)

    player.draw(screen)

    pygame.display.flip()

pygame.quit()

