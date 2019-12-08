from DinamicObject import *
from Vector import *
import random

width = 1000
height = 600
fps = 30

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

player = Player(int(width / 2), int(height / 2), int(30), Vector(0, 0), white)
player.gun_in_hands = True
bullet = TripleShot()

bots = []
for i in range(10):
    bots.append(Heroes(int(random.randint(0, width)),
                       int(random.randint(0, height)),
                       int(30), Vector(random.randint(-2, 2), random.randint(-2, 2)), white))


running = True
while running:
    clock.tick(fps)
    speed_step = 3

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                (coord_x, coord_y) = pygame.mouse.get_pos()
                player.fire(coord_x,
                            coord_y,
                            bullet)
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_a:
                player.speed.x -= speed_step
            if key == pygame.K_d:
                player.speed.x += speed_step
            if key == pygame.K_w:
                player.speed.y -= speed_step
            if key == pygame.K_s:
                player.speed.y += speed_step
            if key == pygame.K_LEFT:
                player.speed.x -= speed_step
            if key == pygame.K_RIGHT:
                player.speed.x += speed_step
            if key == pygame.K_DOWN:
                player.speed.y += speed_step
            if key == pygame.K_UP:
                player.speed.y -= speed_step

        if event.type == pygame.KEYUP:
            key = event.key
            if key == pygame.K_a:
                player.speed.x += speed_step
            if key == pygame.K_d:
                player.speed.x -= speed_step
            if key == pygame.K_w:
                player.speed.y += speed_step
            if key == pygame.K_s:
                player.speed.y -= speed_step
            if key == pygame.K_LEFT:
                player.speed.x -= speed_step
            if key == pygame.K_RIGHT:
                player.speed.x += speed_step
            if key == pygame.K_DOWN:
                player.speed.y += speed_step
            if key == pygame.K_UP:
                player.speed.y -= speed_step

    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    screen.fill(blue)

    player.update(mouse_x, mouse_y)
    bullet.update_speed()

    for i in range(10):
        bots[i].update(player.x, player.y)
        bots[i].draw(screen)

    player.draw(screen)
    bullet.draw(screen)

    pygame.display.flip()

pygame.quit()
