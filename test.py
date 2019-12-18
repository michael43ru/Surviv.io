from DinamicObject import *
from Vector import *
import random
TIME_TO_SHOT_KAMIKAZE = 5
TIME_TO_SHOT_SHOOTER = 3
FPS = 30

width = 1000
height = 600
fps = 30

white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
color_of_heroes = [255, 255, 120]

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

player = Player(int(width / 2), int(height / 2), int(30), Vector(0, 0))
player.gun_in_hands = True
player.bag.get_bullets("divergent")
bullet = []

bots = []
number_of_bots = 7
l = 300
l_0 = 50
for i in range(number_of_bots):
    k = 0
#int(random.randint(0, width)),
#                        int(random.randint(0, height))
    bots.append(Kamikaze(int(random.randint(0, width)),
                        int(random.randint(0, height)),
                        int(30), Vector(random.randint(-k, k), random.randint(-k, k)),
                        Vector(0, 0)))


heroes = [player] + bots
running = True
while running:
    clock.tick(fps)
    speed_step = 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                (coord_x, coord_y) = pygame.mouse.get_pos()
                #Добавляем при тройном и дивергированном выстреле каждую пульку отдельно!
                #Очень глупо, что сам объект никуда не уходит, костыль
                #получается, что добавление каждой из трех пуль нужно прописывать отдельно
                #и вводится локальная переменная, которая после каждой итерации уничтожается
                if player.gun_in_hands and player.bag.bullets_number > 0:
                    if player.bag.bullet_type == "simple":
                        bullet.append(SimpleShot(coord_x, coord_y, player))
                    elif player.bag.bullet_type == "divergent":
                        bullet_not_used = DivergentShot(coord_x, coord_y, player)
                        for i in range(bullet_not_used.n):
                            bullet.append(bullet_not_used.array[i])
                    elif player.bag.bullet_type == "line":
                        bullet_not_used = TripleShot(coord_x, coord_y, player)
                        for i in range(bullet_not_used.n):
                            bullet.append(bullet_not_used.array[i])
                    player.bag.bullets_number -= 1
                else:
                    print("НЕВОЗМОЖНО СТРЕЛЯТЬ!")

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


# wound
    for j in range(len(heroes) - 1, -1, -1):
        for i in range(len(bullet) - 1, -1, -1):
            #FIXME: может быть, не самая лучшая реализация фукции wound(), но work for me!
            if heroes[j].health > 0 and heroes[j].wound(bullet[i]):
                del bullet[i]

#attack
    for i in range(len(bots) - 1, -1, -1):
        bots[i].is_enemy = False

    for i in range(len(bots) - 1, -1, -1):
        for j in range(len(heroes) - 1, -1, -1):
            if i != j-1 and bots[i].attack(heroes[j]) and not bots[i].is_enemy:
                bots[i].get_enemy(heroes[j])

                if bots[i].type == "shooter":
                    if bots[i].time_to_shot < 0:
                        bullet.append(SimpleShot(bots[i].coords_enemy[0], bots[i].coords_enemy[1], bots[i]))
                        bots[i].time_to_shot = TIME_TO_SHOT_SHOOTER
                    else:
                        bots[i].time_to_shot -= 1/FPS

                if bots[i].type == "kamikaze":
                    if bots[i].time_to_green > 1:
                        bots[i].plus_green_to_hands()
                        bots[i].time_to_green = 0
                    else:
                        bots[i].time_to_green += 1/FPS

                    if bots[i].time_to_shot < 0:
                        n = 10
                        for s in range(n):
                            bullet.append(BulletWithoutGun(bots[i].hands[0].x + bots[i].target_vector.turn(s * (360 / n)).x,
                                                           bots[i].hands[0].y + bots[i].target_vector.turn(s * (360 / n)).y,
                                                           bots[i].hands[0]))
                            bullet.append(BulletWithoutGun(bots[i].hands[1].x + bots[i].target_vector.turn(s * (360 / n)).x,
                                                           bots[i].hands[1].y + bots[i].target_vector.turn(s * (360 / n)).y,
                                                           bots[i].hands[1]))

                        bots[i].health = 0
                    else:
                        bots[i].time_to_shot -= 1/FPS

    for i in range(len(bots) - 1, -1, -1):
        if not bots[i].is_enemy:
            bots[i].delete_enemy()

#update
    for i in range(len(bullet) - 1, -1, -1):
        if bullet[i].live:
            bullet[i].update(screen)
        else:
            del bullet[i]

    if player.health > 0:
        player.update(mouse_x, mouse_y, screen)
    else:
        print("ВЫ ПРОИГРАЛИ!")

    for i in range(len(bots) - 1, -1, -1):
        if bots[i].health > 0:
            bots[i].update(screen)
        else:
            del bots[i]

    heroes = [player] + bots

    #print(len(heroes))

    pygame.display.flip()

pygame.quit()
