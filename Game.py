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
        self.len = 10000 # сторона карты
        self.speed = 20

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
                obj.update(obj.speed.x, obj.speed.y, self.sc)
                obj.x -= player.speed.x
                obj.y -= player.speed.y

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
        player.update(x, y, self.sc)

        grass.x -= player.speed.x
        grass.y -= player.speed.y

        player.x -= player.speed.x
        player.y -= player.speed.y

        self.center_x += player.speed.x
        self.center_y += player.speed.y


    def spawn(self):

        for i in range(3, 99, 10):
            for j in range(3, 99, 10):
                k = rnd(0, 4)
                r = rnd(49, 50)
                x = rnd(int(i * self.len / 100 + r * 0.75),
                        int((i + 1) * self.len // 100 - r * 0.75))
                y = rnd(int(j * self.len / 100 + r * 0.75),
                        int((j + 1) * self.len // 100 - r * 0.75))

                if k == 1: # Tree
                    obj = Tree(x - self.center_x, y - self.center_y, r, 1, green_tree)
                    self.trees.append(obj)
                    obj.r = obj.r_interior
                               
                if k == 2: # Box
                    stuff = rnd(1, 3)
                    obj = Box(x - self.center_x, y - self.center_y, r, 2, black, stuff)
                    self.boxes.append(obj)

                if k == 3: # Stone
                    obj = Stone(x - self.center_x, y - self.center_y, r, 1, black)
                    self.stones.append(obj)

                if k == 0: # Bot
                    k = rnd(0, 25)
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
                        
                        obj = Bots(x - self.center_x, y - self.center_y, 20,
                                   speed, (color_r, color_g, color_b))
                        self.bots.append(obj)
                # print(k)

    def draw(self): # исправить

        self.sc.fill(color_water)
        grass.draw(self.sc)
        for line in lines_x:
            line.draw(self.sc)
        for line in lines_y:
            line.draw(self.sc)

        for obj in self.boxes:
            obj.create_box(self.sc)

        for obj in self.trees:
            obj.create_tree(self.sc)

        for obj in self.stones:
            obj.create_stone(self.sc)

        for obj in self.bots:
            obj.draw(self.sc)
            
        player.draw(self.sc)
        


    def main(self):
        
        self.clock.tick(self.fps)

        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.true = False
                
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

        

        speed_x = player.speed.x
        speed_y = player.speed.y

        player.x += speed_x
        player.y += speed_y

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
                                dynamic.speed.x = rnd(-1, 1) * dynamic.speed.x
                                dynamic.speed.y = rnd(-1, 1) * dynamic.speed.y
                                while dynamic.speed.x == 0 and dynamic.speed.y == 0:
                                    dynamic.speed.x = rnd(-1, 1) * dynamic.speed.x
                                    dynamic.speed.y = rnd(-1, 1) * dynamic.speed.y
                            if dynamic in self.bullets:
                                dynamic.live = False
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


        
        player.speed.x = speed_x
        player.speed.y = speed_y

        self.sc.fill(color_water)
        grass.draw(self.sc)
        for line in lines_x:
            line.draw(self.sc)
        for line in lines_y:
            line.draw(self.sc)

        for obj in self.boxes:
            obj.create_box(self.sc)

        for obj in self.trees:
            obj.create_tree(self.sc)

        for obj in self.stones:
            obj.create_stone(self.sc)

        for obj in self.bots:
            obj.draw(self.sc)
            
        player.draw(self.sc)

        #self.draw()
        
        pygame.display.flip()



# pygame.init()

game = Game()

# Задаем цвета

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
green_tree = (0, 180, 0)
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



game.sc.fill(color_water)

v = Vector(0, 0)
player = Player(game.width / 2, game.height / 2, 20, v, (0, 0, 0)) # здесь координаты игрока на экране
player.get_target_vector(0, -1)
player.get_simple_hands()

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

lines_y = [0] * 101
lines_x = [0] * 101
for i in range(101):
    lines_y[i] = Map(i * game.len / 100 - game.center_x, -game.center_y,
                     0.5, game.len, white)
for i in range(101):
    lines_x[i] = Map(-game.center_x, i * game.len / 100 - game.center_y,
                     game.len, 0.5, white)

# game.spawn()

'''for i in range(3, 99, 10):
    for j in range(3, 99, 10):
        k = rnd(0, 4)
        r = rnd(10, 20)
        x = rnd(int(i * game.len / 100 + r * 0.75),
                int((i + 1) * game.len // 100 - r * 0.75))
        y = rnd(int(j * game.len / 100 + r * 0.75),
                int((j + 1) * game.len // 100 - r * 0.75))

        if k == 1: # Tree
            obj = Tree(x, y, r, 1, green_tree)
            game.trees.append(obj)
                               
        if k == 2: # Box
            stuff = rnd(1, 3)
            obj = Box(x, y, r, 2, black, stuff)
            game.boxes.append(obj)

        if k == 3: # Stone
            obj = Stone(x, y, r, 1, black)
            game.stones.append(obj)

        if k == 0: # Bot
            k = rnd(0, 25)
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
                        
                obj = Bots(x, y, 20, speed, (color_r, color_g, color_b))
                game.bots.append(obj)
        # print(k)'''

game.spawn()

'''tree = Tree(0, 0, 20, 1, green_tree)
game.trees.append(tree)'''
            


# Цикл игры

while game.true:
    game.main()

pygame.quit()
