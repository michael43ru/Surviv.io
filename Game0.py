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
        self.heroes = []
        self.delete = []

        self.dinamic_objects.extend([self.bots, self.bullets, self.bombs])
        self.static_objects.extend([self.boxes, self.bushes, self.trees, self.stones, self.drops])
        
        self.width = 800
        self.height = 600
        self.fps = 30
        self.len = 2000 # сторона карты
        self.speed = 20

        self.center_x = rnd(0.03 * self.len, 0.97 * self.len) # координаты игрока в мире
        self.center_y = rnd(0.03 * self.len, 0.97 * self.len)

        self.true = True

        pygame.init()
        pygame.mixer.init() # Звук
        self.sc = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()

    def wound(self):
        for j in range(len(self.heroes) - 1, -1, -1):
            for i in range(len(self.bullets) - 1, -1, -1):
                #FIXME: может быть, не самая лучшая реализация фукции wound(), но work for me!
                if self.heroes[j].health > 0 and self.heroes[j].wound(self.bullets[i]):
                    del self.bullets[i]

    def attack(self):

        for i in range(len(self.bots) - 1, -1, -1):
            self.bots[i].is_enemy = False
        
        for i in range(len(self.bots) - 1, -1, -1):
            for j in range(len(self.heroes) - 1, -1, -1):
                if i != j - 1 and self.bots[i].attack(self.heroes[j]) and not self.bots[i].is_enemy:
                    self.bots[i].get_enemy(self.heroes[j])

                    if self.bots[i].type == "shooter":
                        if self.bots[i].time_to_shot < 0:
                            self.bullets.append(SimpleShot(self.bots[i].coords_enemy[0], self.bots[i].coords_enemy[1], self.bots[i]))
                            self.bots[i].time_to_shot = TIME_TO_SHOT_SHOOTER
                        else:
                            self.bots[i].time_to_shot -= 1/FPS

                    if self.bots[i].type == "kamikaze":
                        if self.bots[i].time_to_green > 1:
                            self.bots[i].plus_green_to_hands()
                            self.bots[i].time_to_green = 0
                        else:
                            self.bots[i].time_to_green += 1/FPS

                        if self.bots[i].time_to_shot < 0:
                            n = 10
                            for s in range(n):
                                self.bullets.append(BulletWithoutGun(self.bots[i].hands[0].x + self.bots[i].target_vector.turn(s * (360 / n)).x,
                                                               self.bots[i].hands[0].y + self.bots[i].target_vector.turn(s * (360 / n)).y,
                                                               self.bots[i].hands[0]))
                                self.bullets.append(BulletWithoutGun(self.bots[i].hands[1].x + self.bots[i].target_vector.turn(s * (360 / n)).x,
                                                               self.bots[i].hands[1].y + self.bots[i].target_vector.turn(s * (360 / n)).y,
                                                               self.bots[i].hands[1]))

                        self.bots[i].health = 0
                    else:
                        self.bots[i].time_to_shot -= 1/FPS

    def update(self):
        
        for i in range(len(self.bots) - 1, -1, -1):
            if self.bots[i].health > 0:
                self.bots[i].x -= player.speed.x
                self.bots[i].y -= player.speed.y
                self.bots[i].update(self.sc)
            else:
                del self.bots[i]

        for i in range(len(self.bullets) - 1, -1, -1):
            if self.bullets[i].live:
                self.bullets[i].x -= player.speed.x
                self.bullets[i].y -= player.speed.y
                self.bullets[i].update(self.sc)
            else:
                del self.bullets[i]

        for lst in self.static_objects:
            for obj in lst:
                obj.x -= player.speed.x
                obj.y -= player.speed.y

        for line in lines_x:
            line.x -= player.speed.x
            line.y -= player.speed.y
        for line in lines_y:
            line.x -= player.speed.x
            line.y -= player.speed.y

        (x, y) = pygame.mouse.get_pos()
        if player.health > 0:
            player.update(x, y, self.sc)
        else:
            print("ВЫ ПРОИГРАЛИ!")

        grass.x -= player.speed.x
        grass.y -= player.speed.y

        player.x -= player.speed.x
        player.y -= player.speed.y

        zone.x -= player.speed.x
        zone.y -= player.speed.y

        self.center_x += player.speed.x
        self.center_y += player.speed.y

    def spawn(self):

        for i in range(3, 9, 1):
            for j in range(3, 9, 1):
                k = rnd(0, 4)
                r = rnd(50, 51)
                x = rnd(int(i * self.len / 10 + r * 0.75),
                        int((i + 1) * self.len // 10 - r * 0.75))
                y = rnd(int(j * self.len / 10 + r * 0.75),
                        int((j + 1) * self.len // 10 - r * 0.75))

                if k == 1: # Tree
                    obj = Tree(x - self.center_x, y - self.center_y, r, 1)
                    self.trees.append(obj)
                    # obj.r = obj.r_interior
                               
                if k == 2: # Box
                    stuff = rnd(2, 7)
                    obj = Box(x - self.center_x, y - self.center_y, r, 2, black, stuff)
                    self.boxes.append(obj)

                if k == 3: # Stone
                    obj = Stone(x - self.center_x, y - self.center_y, r, 1, black)
                    self.stones.append(obj)

                if k == 0: # Bot
                    k = rnd(0, 4)
                    if k == 0:
                        vx = 0
                        vy = 0
                        while vx == 0 and vy == 0:
                            vy = rnd(-1, 2)
                            vx = rnd(-1, 2)
                        vx *= 8
                        vy *= 8
                        speed = Vector(vx, vy)
                        color_r = rnd(0, 256)
                        color_g = rnd(0, 256)
                        color_b = rnd(0, 256)
                        
                        obj = Shooter(x - self.center_x, y - self.center_y, 20,
                                   speed, speed)
                        self.bots.append(obj)

                    if k == 1:
                        vx = 0
                        vy = 0
                        while vx == 0 and vy == 0:
                            vy = rnd(-1, 2)
                            vx = rnd(-1, 2)
                        vx *= 8
                        vy *= 8
                        speed = Vector(vx, vy)
                        color_r = rnd(0, 256)
                        color_g = rnd(0, 256)
                        color_b = rnd(0, 256)
                        
                        obj = Kamikaze(x - self.center_x, y - self.center_y, 20,
                                   speed, speed)
                        self.bots.append(obj)
                # print(k)

    def draw(self):

        self.sc.fill(color_water)
        grass.draw(self.sc)
        for line in lines_x:
            line.draw(self.sc)
        for line in lines_y:
            line.draw(self.sc)

        player.draw(self.sc)
        for obj in self.bots:
            obj.draw(self.sc)

        for obj in self.boxes:
            obj.create_box(self.sc)

        for obj in self.trees:
            obj.create_tree(self.sc)

        for obj in self.stones:
            obj.create_stone(self.sc)

        for obj in self.bullets:
            obj.draw(self.sc)
        


    def main(self):
        
        self.clock.tick(self.fps)

        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.true = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1:
                    for stone in self.stones:
                        if math.hypot((player.x - stone.x), (player.y - stone.y)) <= 2 * (stone.r + player.r) and (
                            stone.collision_with_fighter() == 0):
                            self.delete.append(stone)
                    for box in self.boxes:
                        if math.hypot((player.x - box.x), (player.y - box.y)) <= 2 * (box.r + player.r) and (
                            box.r > 0) and box.collision_with_fighter() == 0:
                            box.r = 0
                            box.image = box.object_in_the_box
                        elif math.hypot((player.x - box.x), (player.y - box.y)) <= 2 * (box.r + player.r) and (
                            box.r == 0) and box.get_stuff() == 0:
                            self.delete.append(box)
                            if box.interior_stuff == 1:
                                player.gun_in_hands = True
                            if box.interior_stuff == 2:
                                player.bag.heart += 1
                            if box.interior_stuff == 3:
                                player.bag.aid += 1
                            if box.interior_stuff == 4:
                                player.gun_in_hands = True
                                player.bag.bullet_type = 'simple'
                                player.bag.bullets_number = 50
                            if box.interior_stuff == 5:
                                player.gun_in_hands = True
                                player.bag.bullet_type = 'line'
                                player.bag.bullets_number = 50
                            if box.interior_stuff == 6:
                                player.gun_in_hands = True
                                player.bag.bullet_type = 'divergent'
                                player.bag.bullets_number = 50
                                
                            
                    
                if event.button == 1:
                    (coord_x, coord_y) = pygame.mouse.get_pos()
                    #Добавляем при тройном и дивергированном выстреле каждую пульку отдельно!
                    #Очень глупо, что сам объект никуда не уходит, костыль
                    #получается, что добавление каждой из трех пуль нужно прописывать отдельно
                    #и вводится локальная переменная, которая после каждой итерации уничтожается
                    if player.gun_in_hands and player.bag.bullets_number > 0:
                        if player.bag.bullet_type == "simple":
                            self.bullets.append(SimpleShot(coord_x, coord_y, player))
                        elif player.bag.bullet_type == "divergent":
                            bullet_not_used = DivergentShot(coord_x, coord_y, player)
                            for i in range(bullet_not_used.n):
                                self.bullets.append(bullet_not_used.array[i])
                        elif player.bag.bullet_type == "line":
                            bullet_not_used = TripleShot(coord_x, coord_y, player)
                            for i in range(bullet_not_used.n):
                                self.bullets.append(bullet_not_used.array[i])
                        player.bag.bullets_number -= 1
                    else:
                        print("НЕВОЗМОЖНО СТРЕЛЯТЬ!")
                
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_a:
                    player.speed.x -= self.speed
                if key == pygame.K_d:
                    player.speed.x += self.speed
                if key == pygame.K_w:
                    player.speed.y -= self.speed
                if key == pygame.K_s:
                    player.speed.y += self.speed
                if key == pygame.K_LEFT:
                    player.speed.x -= self.speed
                if key == pygame.K_RIGHT:
                    player.speed.x += self.speed
                if key == pygame.K_DOWN:
                    player.speed.y += self.speed
                if key == pygame.K_UP:
                    player.speed.y -= self.speed

                if key == pygame.K_1 and player.bag.bullets_number > 0:
                    player.gun_in_hands = True
                if key == pygame.K_2:
                    player.gun_in_hands = False
                if key == pygame.K_3 and player.bag.heart > 0:
                    player.bag.heart -= 1
                    if player.health <= HEALTH_PLAYER - 3:
                        player.health += 3
                    else:
                        player.health = HEALTH_PLAYER
                    player.array_color[1] += 3 * COLOR[1] / HEALTH_PLAYER
                    player.array_color[2] += 3 * COLOR[2] / HEALTH_PLAYER
                    if player.array_color[1] > 255:
                        player.array_color[1] = 255
                    if player.array_color[2] > 120:
                        player.array_color[2] = 120

                if key == pygame.K_4 and player.bag.aid > 0:
                    player.health = HEALTH_PLAYER
                    player.bag.aid -= 1
                    player.color = COLOR

            if event.type == pygame.KEYUP:
                key = event.key
                if key == pygame.K_a:
                    player.speed.x += self.speed
                if key == pygame.K_d:
                    player.speed.x -= self.speed
                if key == pygame.K_w:
                    player.speed.y += self.speed
                if key == pygame.K_s:
                    player.speed.y -= self.speed
                if key == pygame.K_LEFT:
                    player.speed.x += self.speed
                if key == pygame.K_RIGHT:
                    player.speed.x -= self.speed
                if key == pygame.K_DOWN:
                    player.speed.y -= self.speed
                if key == pygame.K_UP:
                    player.speed.y += self.speed

        
        
        if abs(player.speed.x) < 0.25:
            player.speed.x = 0
        if abs(player.speed.y) < 0.25:
            player.speed.y = 0
        
        if player.speed.x != 0 and player.speed.y != 0:
            player.speed.mult_by_scalar(2 ** 0.5 / 2)

        speed_x = player.speed.x
        speed_y = player.speed.y

        player.x += player.speed.x
        player.y += player.speed.y

        for lst_s in self.static_objects:
            for static in lst_s:
                if static.collision_with_gamer(player) == 100:
                    pass
                elif static.collision_with_gamer(player) < math.pi / 2 and (
                    static.collision_with_gamer(player) > -math.pi / 2) and (
                     static.collision_with_gamer(player) != 0):
                    # player.x -= player.speed.x
                    # player.y -= player.speed.y
                    player.speed.x = 0
                    player.speed.y = 0
                elif static.collision_with_gamer(player) == 0:
                    # player.x -= player.speed.x
                    player.speed.x = 0
                elif static.collision_with_gamer(player) == math.pi / 2 or (
                    static.collision_with_gamer(player) == -math.pi / 2):
                    # player.x -= player.speed.y
                    player.speed.y = 0
        


        player.x -= speed_x
        player.y -= speed_y

        # print(player.speed.x, player.speed.y)

        self.wound()
        self.attack()
        self.update()


        # water.x -= player.speed.x
        # water.y -= player.speed.y
        

        for lst_s in self.static_objects:
            for static in lst_s:
                for lst_d in self.dinamic_objects:
                    for dynamic in lst_d:
                        if static.collision_with_gamer(dynamic) == 100:
                            pass
                        elif static.collision_with_gamer(dynamic) < math.pi / 2 and (
                            static.collision_with_gamer(dynamic) > -math.pi / 2) and (
                                static.collision_with_gamer(dynamic) != 0):
                            if dynamic in self.bots:
                                dynamic.x -= dynamic.speed.x
                                dynamic.y -= dynamic.speed.y
                                '''dynamic.speed.x = rnd(-1, 1) * dynamic.speed.x
                                dynamic.speed.y = rnd(-1, 1) * dynamic.speed.y
                                while dynamic.speed.x == 0 and dynamic.speed.y == 0:
                                    dynamic.speed.x = rnd(-1, 1) * dynamic.speed.x
                                    dynamic.speed.y = rnd(-1, 1) * dynamic.speed.y'''
                                dynamic.speed.x = -dynamic.speed.x
                                dynamic.speed.y = -dynamic.speed.y
                            if dynamic in self.bullets:
                                dynamic.live = False
                                if lst_s == self.stones:
                                    if static.r >= 20:
                                        static.r *= 0.8 # на сколько уменьшается радикс за один щелчок
                                    else:
                                        self.delete.append(static)
                                        
                                        
                        elif static.collision_with_gamer(dynamic) == 0:
                            if dynamic in self.bots:
                                dynamic.x -= dynamic.speed.x
                                dynamic.speed.x = -dynamic.speed.x 
                            if dynamic in self.bullets:
                                dynamic.live = False
                        elif static.collision_with_gamer(dynamic) == math.pi / 2 or (
                            static.collision_with_gamer(dynamic) == -math.pi / 2):
                            if dynamic in self.bots:
                                dynamic.y -= dynamic.speed.y
                                dynamic.speed.y = -dynamic.speed.y 
                            if dynamic in self.bullets:
                                dynamic.live = False


        for bot in self.bots:
            for bullet in self.bullets:
                if bot.wound(bullet):
                    self.delete.append(bullet)
            


        
        player.speed.x = speed_x
        player.speed.y = speed_y

        if speed_x != 0 and speed_y != 0:
            player.speed.mult_by_scalar(2 ** 0.5)

        if abs(player.speed.x) < 0.25:
            player.speed.x = 0
        if abs(player.speed.y) < 0.25:
            player.speed.y = 0
            
        zone.r -= zone.v
        for her in self.heroes:
            if zone.hit(her) == 0:
                her.array_color[1] -= 2
                her.array_color[2] -= 1
                for i in range(3):
                    if her.array_color[i] < 0:
                        her.array_color[i] = 0
                her.color = (her.array_color[0], her.array_color[1], her.array_color[2])
        

        
        for lst in self.static_objects:
            for obj in lst:
                if obj in self.delete:
                    lst.pop(lst.index(obj))
        for lst in self.dinamic_objects:
            for obj in lst:
                if obj in self.delete:
                    lst.pop(lst.index(obj))
        
            
        self.draw()
        zone.draw(self.sc)
        
        if player.health <= 0:
            cat = pygame.image.load('END0.jpg')
            self.sc.blit(cat, (0, 0))

        if zone.r <= self.len * 2 ** 0.5 / 10:
            print('ПОЗДРАВЛЯЮ, ВЫ ПОБЕДИТЕЛЬ!')
            Karasev = pygame.image.load('WIN.jpg')
            self.sc.blit(Karasev, (0, 0))
        
        pygame.display.flip()



# pygame.init()

game = Game()

FPS = 30
COLOR = [255, 255, 120]
HEALTH_PLAYER = 10
HEALTH_BOTS = 4
TIME_TO_SHOT_SHOOTER = 3
TIME_TO_SHOT_KAMIKAZE = 5
STANDART_SIZE_OF_HANDS = 0.25

# Задаем цвета

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
green_tree = (0, 180, 0)
blue = (0, 0, 255)
brown = (128, 64, 0)
color_grass = [160, 255, 100]
color_water = [70, 120, 255]
color_of_heroes = [255, 255, 120]


'''img_dir = path.join(path.dirname(__file__), 'img')
red_zone_img = pg.image.load(path.join(img_dir, "Red_zone.png")).convert()'''

game.sc.fill(color_water)

v = Vector(0, 0)
player = Player(game.width / 2, game.height / 2, 20, v) # здесь координаты игрока на экране
game.heroes = [player] + game.bots
player.get_target_vector(0, -1)
player.get_simple_hands()


grass = Map(0.02 * game.len - game.center_x, 0.02 * game.len - game.center_y,
            0.96 * game.len, 0.96 * game.len, color_grass)

zone = Red_zone(game.len / 2 - game.center_x, game.len / 2 - game.center_y,
                2 ** 0.5 * game.len / 2, game.len, game.sc)

lines_y = [0] * 11
lines_x = [0] * 11
for i in range(11):
    lines_y[i] = Map(i * game.len / 10 - game.center_x, -game.center_y,
                     0.5, game.len, white)
for i in range(11):
    lines_x[i] = Map(-game.center_x, i * game.len / 10 - game.center_y,
                     game.len, 0.5, white)

game.spawn()

'''v = Vector(10, 10)
bot = Bots(-40, -40, 20, v, v)
game.bots.append(bot)'''

# Цикл игры

while game.true:
    game.main()

cat = pygame.image.load('END.jpg')
game.sc.blit(cat, (0, 0))
'''true = True
while true == True:
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            true = False'''
pygame.quit()
