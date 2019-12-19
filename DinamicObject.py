from Vector import *
from GeometricObject import *
from Bag import *
from pygame.rect import Rect
import math as m
from abc import ABC, abstractmethod
import random
FPS = 30
COLOR = [255, 255, 120]
HEALTH_PLAYER = 10
HEALTH_BOTS = 4
TIME_TO_SHOT_SHOOTER = 3
TIME_TO_SHOT_KAMIKAZE = 5
STANDART_SIZE_OF_HANDS = 0.25


class DinamicObject(ABC):

    @abstractmethod
    def __init__(self, x, y, r, speed):
        self.bounds = Rect(x, y, r, r) #как бы границы объекта(квадрат вокруг нашей круглой фигуры)
        self.speed = speed
        self.array_color = [COLOR[0], COLOR[1], COLOR[2]]
        self.color = (self.array_color[0], self.array_color[1], self.array_color[2])
        #координаты центра объекта
        self.x = x + r / 2
        self.y = y + r / 2
        self.r = r
        self.stop = None

    @abstractmethod
    def move(self):
        self.x += self.speed.x
        self.y += self.speed.y
        self.bounds = self.bounds.move(self.speed.x, self.speed.y)

    @abstractmethod
    def draw(self):
        pass

    def is_collision(self, obj):
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False


class Bullet(DinamicObject):
    def __init__(self, target_x, target_y, player):
        self.name = "bullet"
        self.x = player.gun.x_end
        self.y = player.gun.y_end
        self.live = True
        self.speed_step = 6
        self.r = 3
        self.hit_distance = 80
        self.color = (0, 0, 0)
        self.direction = Vector(target_x - player.x, target_y - player.y).normalized()
        self.speed = self.direction.mult_by_scalar(self.speed_step)
        self.bounds = None

    def draw(self, surface):
        pass

    def move(self):
        if self.live:
            super().move()

    def update(self, surface):
        if self.live and self.hit_distance > 0:
            self.hit_distance -= 1
            self.bounds = Rect(self.x, self.y, self.r, self.r)
        else:
            self.live = False
        self.move()
        self.draw(surface)


class BulletWithoutGun(Bullet):
    def __init__(self, target_x, target_y, centre):
        self.name = "bullet"
        self.x = centre.x
        self.y = centre.y
        self.live = True
        self.speed_step = 30
        self.r = 3
        self.hit_distance = 80
        self.color = (0, 0, 0)
        self.direction = Vector(target_x - centre.x, target_y - centre.y).normalized()
        self.speed = self.direction.mult_by_scalar(self.speed_step)
        self.bounds = None

    def draw(self, surface):
        if self.live:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.r))


class SimpleShot(Bullet):
    def __init__(self, target_x, target_y, player):
        super().__init__(target_x, target_y, player)
        self.type = "simple"

    def draw(self, surface):
        if self.live:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.r))


class TripleShot(Bullet):
    def __init__(self, target_x, target_y, player):
        self.n = 3
        self.array = []
        self.type = "line"
        for i in range(self.n):
            self.array.append(SimpleShot(target_x, target_y, player))
        self.direction = Vector(target_x - player.x, target_y - player.y).normalized()
        for i in range(self.n):
            k = 2.5
            self.array[i].direction = Vector(target_x - player.x, target_y - player.y).normalized()
            self.array[i].speed = self.array[i].direction.mult_by_scalar(self.array[i].speed_step)
            self.array[i].x = player.gun.x_end + k*i*self.array[i].direction.x
            self.array[i].y = player.gun.y_end + k*i*self.array[i].direction.y

    def is_collision(self, obj):
        for i in range(self.n):
            self.array[i].is_collision(obj)

    def move(self):
        for i in range(self.n):
            self.array[i].move()

    def draw(self, surface):
        for i in range(self.n):
            self.array[i].draw(surface)

    def update(self, surface):
        for i in range(self.n):
            self.array[i].update(surface)


class DivergentShot(Bullet):
    def __init__(self, target_x, target_y, player):
        self.n = 3
        self.array = []
        self.type = "divergent"
        for i in range(self.n):
            self.array.append(SimpleShot(target_x, target_y, player))
        self.direction = Vector(target_x - player.x, target_y - player.y).normalized()
        for i in range(self.n):
            k = 7
            self.array[i].direction = Vector(target_x - player.x, target_y - player.y).normalized().turn(-k*((self.n - 1) // 2) + k*i)
            self.array[i].speed = self.array[i].direction.mult_by_scalar(self.array[i].speed_step)
            self.array[i].x = player.gun.x_end
            self.array[i].y = player.gun.y_end

    def is_collision(self, obj):
        for i in range(self.n):
            self.array[i].is_collision(obj)

    def move(self):
        for i in range(self.n):
            self.array[i].move()

    def draw(self, surface):
        for i in range(self.n):
            self.array[i].draw(surface)

    def update(self, surface):
        for i in range(self.n):
            self.array[i].update(surface)


class Heroes(DinamicObject):

    def __init__(self, x, y, r, speed):
        super().__init__(x, y, r, speed)
        self.name = "heroes"
        self.target_vector = Vector(0, 0) #нулевой вектор обозначает отсутствие цели
        self.is_live = True
        self.hands = []
        self.exist_hands = False
        self.exist_target = False
        self.gun_in_hands = False
        self.size_of_hands = STANDART_SIZE_OF_HANDS

    def wound(self, obj):
        if self.is_collision(obj) and obj.name == "bullet":
            self.health -= 1
            self.plus_red()
            return True
        else:
            return False

    def plus_red(self):
        #FIXME: работает только для игроков с цветом COLOR
        pass

    def move(self):
        super().move()

    def draw(self, surface):
        self.draw_body(surface)
        if self.exist_hands:
            self.draw_hands(surface)
        if self.gun_in_hands:
            self.draw_gun(surface)

    def draw_body(self, surface):
        #зачем int()
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.r))
        #голубым цветом откладывает вектор скорости от центра
        if not self.speed.is_null_vector():
            self.speed.draw(surface, (0, 70, 225), self.x, self.y)

    def hands_hit(self):
        pass

    def get_simple_hands(self):
        self.exist_hands = True
        if self.target_vector.is_null_vector():

            hand1 = Ball(self.target_vector.turn(30).x + self.x,
                         self.target_vector.turn(30).y + self.y, self.size_of_hands*self.r)
            hand2 = Ball(self.target_vector.turn(-30).x + self.x,
                         self.target_vector.turn(-30).y + self.y, self.size_of_hands*self.r)
        else:
            hand1 = Ball(self.target_vector.turn(30).x + self.x,
                         self.target_vector.turn(30).y + self.y, self.size_of_hands*self.r)
            hand2 = Ball(self.target_vector.turn(-30).x + self.x,
                         self.target_vector.turn(-30).y + self.y, self.size_of_hands*self.r)
        self.hands.append(hand1)
        self.hands.append(hand2)
        return self.hands

    def draw_hands(self, surface):
        for hand in self.hands:
            pygame.draw.circle(surface, self.color, (int(hand.x), int(hand.y)), int(hand.r))
            #черная каёмочка рук
            pygame.draw.circle(surface, (0, 0, 0), (int(hand.x), int(hand.y)), int(hand.r), int(0.15*hand.r))

    def get_target_vector(self, x, y):
        self.exist_target = True
        self.target_vector = Vector(x - self.x, y - self.y).normalized().mult_by_scalar(self.r)

    def draw_target_vector(self, surface):
        #черным цветом обозначен вектор цели
        self.target_vector.draw(surface, (800, 0, 0), self.x, self.y)

    def delete_target(self):
        self.exist_target = False
        self.target_vector = Vector(0, 0)

    def delete_hands(self):
        self.exist_hands = False
        self.hands = []

    def update(self, target_x, target_y, surface):
        self.delete_target()
        self.delete_hands()
        self.get_target_vector(target_x, target_y)
        if self.gun_in_hands:
            self.get_simple_gun()
        else:
            self.get_simple_hands()

        self.move()
        self.draw(surface)

    def get_simple_gun(self):
        if self.exist_target:
            self.exist_hands = True
            self.gun = SimpleGun(self.target_vector.x + self.x,
                                 self.target_vector.y + self.y,
                                 2.5*self.target_vector.x + self.x,
                                 2.5*self.target_vector.y + self.y)
            self.get_hands_to_simple_gun()
        else:
            print('Но у вас же нет цели, зачем оружие?!')

    def get_hands_to_simple_gun(self):
        #FIXME: как по-умному создавать новый объект в python?!
        turn_hand = Vector(self.target_vector.x, self.target_vector.y)
        hand1 = Ball(self.target_vector.x + self.x,
                     self.target_vector.y + self.y, self.size_of_hands*self.r)
        hand2 = Ball(turn_hand.mult_by_scalar(0.75).turn(-3).x + self.x + self.target_vector.x,
                     turn_hand.mult_by_scalar(0.75).turn(-3).y + self.y + self.target_vector.y,
                     self.size_of_hands*self.r)
        self.hands.append(hand1)
        self.hands.append(hand2)

    def draw_gun(self, surface):
        self.gun.draw(surface)


class Player(Heroes):
    def __init__(self, x, y, r, speed):
        super().__init__(x, y, r, speed)
        self.gun_in_hands = False
        self.bag = StandartBag()
        self.gun = None
        self.health = HEALTH_PLAYER
        self.type = "player"

    def plus_red(self):
        #FIXME: работает только для игроков с цветом COLOR
        self.array_color[1] -= COLOR[1] / HEALTH_PLAYER
        self.array_color[2] -= COLOR[2] / HEALTH_PLAYER
        self.color = (self.array_color[0], self.array_color[1], self.array_color[2])

    def draw(self, surface):
        self.draw_body(surface)
        self.draw_hands(surface)
        if self.gun_in_hands:
            self.draw_gun(surface)
        self.bag.draw(surface, self)


class Bots(Heroes):
    def __init__(self, x, y, r, speed, default_target):
        super().__init__(x, y, r, speed)
        self.bounds_of_fight = 15*self.r
        self.health = HEALTH_BOTS
        self.is_enemy = False
        self.default_target = default_target
        self.coords_enemy = []
        self.default_speed = speed
        self.exist_target = True
        #self.gun_in_hands = random.choice(True, False)

    def draw(self, surface):
        super().draw(surface)
        #self.draw_target_vector(surface)

    def attack(self, obj):
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= self.bounds_of_fight**2:
            return True
        else:
            return False


class Kamikaze(Bots):
    def __init__(self, x, y, r, speed, default_target):
        super().__init__(x, y, r, speed, default_target)
        self.gun_in_hands = False
        self.time_to_shot = TIME_TO_SHOT_KAMIKAZE
        self.time_to_green = 0
        self.type = "kamikaze"
        self.array_color_hands = [COLOR[0], COLOR[1], COLOR[2]]
        self.color_hands = (self.array_color_hands[0], self.array_color_hands[1], self.array_color_hands[2])

    def update(self, surface):
        if self.is_enemy:
            super(Bots, self).update(self.coords_enemy[0], self.coords_enemy[1], surface)
        else:
            super(Bots, self).update(self.default_target.x, self.default_target.y, surface)

    def draw_hands(self, surface):
        for hand in self.hands:
            pygame.draw.circle(surface, self.color_hands, (int(hand.x), int(hand.y)), int(hand.r))
            #черная каёмочка рук
            pygame.draw.circle(surface, (0, 0, 0), (int(hand.x), int(hand.y)), int(hand.r), int(0.15*30*STANDART_SIZE_OF_HANDS))

    def get_enemy(self, enemy):
        self.is_enemy = True
        self.get_target_vector(enemy.x, enemy.y)
        self.speed = Vector(self.target_vector.x, self.target_vector.y).normalized().mult_by_scalar(1)
        self.coords_enemy = [enemy.x, enemy.y]

    def delete_enemy(self):
        self.is_enemy = False
        self.speed = self.default_speed
        # при удалении можно делать руки обычными, а можно оставлять большими
        #self.color_hands = self.color
        #self.size_of_hands = STANDART_SIZE_OF_HANDS

    def plus_green_to_hands(self):
        #FIXME: работает только для игроков с цветом COLOR
        self.array_color_hands[0] -= COLOR[0] / TIME_TO_SHOT_KAMIKAZE
        self.array_color_hands[2] -= COLOR[2] / TIME_TO_SHOT_KAMIKAZE
        self.color_hands = (self.array_color_hands[0], self.array_color_hands[1], self.array_color_hands[2])
        self.size_of_hands += 0.65 / (TIME_TO_SHOT_KAMIKAZE-1)

    def plus_red(self):
        #FIXME: работает только для игроков с цветом COLOR
        self.array_color[1] -= COLOR[1] / HEALTH_BOTS
        self.array_color[2] -= COLOR[2] / HEALTH_BOTS
        self.color = (self.array_color[0], self.array_color[1], self.array_color[2])


class Shooter(Bots):
    def __init__(self, x, y, r, speed, default_target):
        super().__init__(x, y, r, speed, default_target)
        self.gun_in_hands = False
        self.time_to_shot = TIME_TO_SHOT_SHOOTER
        self.gun = None
        self.type = "shooter"

    def plus_red(self):
        #FIXME: работает только для игроков с цветом COLOR
        self.array_color[1] -= COLOR[1] / HEALTH_BOTS
        self.array_color[2] -= COLOR[2] / HEALTH_BOTS
        self.color = (self.array_color[0], self.array_color[1], self.array_color[2])

    def get_enemy(self, enemy):
        self.is_enemy = True
        self.gun_in_hands = True
        self.get_target_vector(enemy.x, enemy.y)
        self.speed = Vector(self.target_vector.x, self.target_vector.y).normalized().mult_by_scalar(1)
        self.coords_enemy = [enemy.x, enemy.y]

    def delete_enemy(self):
        self.is_enemy = False
        self.gun_in_hands = False
        self.speed = self.default_speed

    def update(self, surface):
        if self.is_enemy:
            super(Bots, self).update(self.coords_enemy[0], self.coords_enemy[1], surface)
        else:
            super(Bots, self).update(self.default_target.x, self.default_target.y, surface)
