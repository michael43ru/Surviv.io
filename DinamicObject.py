from Vector import *
from GeometricObject import *
from Bag import *
from pygame.rect import Rect
import math as m
from abc import ABC, abstractmethod


class DinamicObject(ABC):

    @abstractmethod
    def __init__(self, x, y, r, speed, color):
        self.bounds = Rect(x, y, r, r) #как бы границы объекта(квадрат вокруг нашей круглой фигуры)
        self.speed = speed
        self.color = color
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


class Bullet(DinamicObject):
    def __init__(self):
        self.x = None
        self.y = None
        self.live = True
        self.fire_flag = False
        self.speed_step = 3
        self.r = 3
        self.hit_distance = 50
        self.color = (0, 0, 0)
        self.direction = None
        self.speed = None
        self.bounds = None

    def draw(self):
        pass

    def move(self):
        if self.fire_flag and self.live:
            super().move()

    def is_collision(self, obj):
        if (self.x - obj.x)^2 + (self.y - obj.y)^2 < (self.r + obj.r)^2:
            return True
        else:
            return False

    def start_fire(self, target_x, target_y, gun, player):
        pass

    def update_speed(self):
        if self.fire_flag and self.hit_distance > 0:
            self.hit_distance -= 1
            self.bounds = Rect(self.x, self.y, self.r, self.r)
        else:
            self.fire_flag = False
        if self.hit_distance <= 0:
            self.live = False

        self.move()


class SimpleShot(Bullet):
    def __init__(self):
        super().__init__()
        self.type = "simple" #у каждого выстрела свой тип

    def draw(self, surface):
        if self.fire_flag and self.live:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.r))

    def start_fire(self, target_x, target_y, gun, player):
        self.fire_flag = True
        self.direction = Vector(target_x - player.x, target_y - player.y).normalized()
        self.speed = self.direction.mult_by_scalar(self.speed_step)
        self.x = gun.x_end
        self.y = gun.y_end


class TripleShot(Bullet):
    def __init__(self):
        self.n = 3
        self.array = []
        self.type = "line"
        for i in range(self.n):
            self.array.append(SimpleShot())

    def start_fire(self, target_x, target_y, gun, player):
        self.fire_flag = True
        self.direction = Vector(target_x - player.x, target_y - player.y).normalized()
        for i in range(self.n):
            self.array[i].fire_flag = True
            self.array[i].direction = Vector(target_x - player.x, target_y - player.y).normalized()
            self.array[i].speed = self.array[i].direction.mult_by_scalar(self.array[i].speed_step)
            self.array[i].x = gun.x_end + 3*i*self.array[i].direction.x
            self.array[i].y = gun.y_end + 3*i*self.array[i].direction.y

    def is_collision(self, obj):
        for i in range(self.n):
            self.array[i].is_collision(obj)

    def move(self):
        for i in range(self.n):
            self.array[i].move()

    def draw(self, surface):
        for i in range(self.n):
            self.array[i].draw(surface)

    def update_speed(self):
        for i in range(self.n):
            self.array[i].update_speed()


class DivergentShot(Bullet):
    def __init__(self):
        self.n = 3
        self.array = []
        self.type = "divergent"
        for i in range(self.n):
            self.array.append(SimpleShot())

    def start_fire(self, target_x, target_y, gun, player):
        self.fire_flag = True
        self.direction = Vector(target_x - player.x, target_y - player.y).normalized()
        for i in range(self.n):
            self.array[i].fire_flag = True
            self.array[i].direction = Vector(target_x - player.x, target_y - player.y).normalized().turn(-8*((self.n - 1) // 2) + 8*i)
            self.array[i].speed = self.array[i].direction.mult_by_scalar(self.array[i].speed_step)
            self.array[i].x = gun.x_end
            self.array[i].y = gun.y_end

    def is_collision(self, obj):
        for i in range(self.n):
            self.array[i].is_collision(obj)

    def move(self):
        for i in range(self.n):
            self.array[i].move()

    def draw(self, surface):
        for i in range(self.n):
            self.array[i].draw(surface)

    def update_speed(self):
        for i in range(self.n):
            self.array[i].update_speed()


class Heroes(DinamicObject):

    def __init__(self, x, y, r, speed, color):
        super().__init__(x, y, r, speed, color)
        self.target_vector = Vector(0, 0) #нулевой вектор обозначает отсутствие цели
        self.is_live = True
        self.health = 10
        self.hands = []
        self.exist_hands = False
        self.exist_target = False
        self.gun_in_hands = False
        #self.hands = self.get_hands(target_vector, self.x, self.y, self.r)

    def move(self):
        super().move()

    def draw(self, surface):
        self.draw_body(surface)
        if self.exist_hands:
            self.draw_hands(surface)

    def draw_body(self, surface):
        #зачем int()
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.r))
        #голубым цветом откладывает вектор скорости от центра
        if not self.speed.is_null_vector():
            self.speed.draw(surface, (0, 70, 225), self.x, self.y)

    def hands_hit(self):
        pass

    def get_simple_hands(self):
        k = 0.25
        self.exist_hands = True
        if self.target_vector.is_null_vector():

            hand1 = Ball(self.target_vector.turn(30).x + self.x,
                         self.target_vector.turn(30).y + self.y, k*self.r)
            hand2 = Ball(self.target_vector.turn(-30).x + self.x,
                         self.target_vector.turn(-30).y + self.y, k*self.r)
        else:
            hand1 = Ball(self.target_vector.turn(30).x + self.x,
                         self.target_vector.turn(30).y + self.y, k*self.r)
            hand2 = Ball(self.target_vector.turn(-30).x + self.x,
                         self.target_vector.turn(-30).y + self.y, k*self.r)
        self.hands.append(hand1)
        self.hands.append(hand2)
        return self.hands

    def draw_hands(self, surface):
        for hand in self.hands:
            pygame.draw.circle(surface, self.color, (int(hand.x), int(hand.y)), int(hand.r))
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

    def update(self, target_x, target_y):
        self.delete_target()
        self.delete_hands()
        self.get_target_vector(target_x, target_y)
        self.get_simple_hands()

        self.move()


class Player(Heroes):
    def __init__(self, x, y, r, speed, color):
        super().__init__(x, y, r, speed, color)
        self.gun_in_hands = False
        self.bag = StandartBag()
        self.gun = None

    def draw(self, surface):
        self.draw_body(surface)
        self.draw_hands(surface)
        if self.gun_in_hands:
            self.draw_gun(surface)
        #self.bag.draw(surface, self)

    def get_simple_gun(self):
        if self.exist_target:
            self.gun_in_hands = True
            self.exist_hands = True
            self.gun = SimpleGun(self.target_vector.x + self.x,
                                 self.target_vector.y + self.y,
                                 2.5*self.target_vector.x + self.x,
                                 2.5*self.target_vector.y + self.y)
            self.get_hands_to_simple_gun()
        else:
            print('Но у вас же нет цели, зачем оружие?!')

    def get_hands_to_simple_gun(self):
        k = 0.25
        #FIXME: как по-умному создавать новый объект в python?!
        turn_hand = Vector(self.target_vector.x, self.target_vector.y)
        hand1 = Ball(self.target_vector.x + self.x,
                     self.target_vector.y + self.y, k*self.r)
        hand2 = Ball(turn_hand.mult_by_scalar(0.75).turn(-3).x + self.x + self.target_vector.x,
                     turn_hand.mult_by_scalar(0.75).turn(-3).y + self.y + self.target_vector.y,
                     k*self.r)
        self.hands.append(hand1)
        self.hands.append(hand2)

    def draw_gun(self, surface):
        self.gun.draw(surface)

    def update(self, target_x, target_y):
        self.update_bag()
        self.delete_target()
        self.delete_hands()
        self.get_target_vector(target_x, target_y)
        if self.gun_in_hands:
            self.get_simple_gun()
        else:
            self.get_simple_hands()

        self.move()

    def update_bag(self):
        #FIXME: как реализовывать рюкзак и количество патронов
        pass

    def fire(self, target_x, target_y, bullet):
        # функция принимает на вход патрон и координаты точки, куда стрелять
        bullet.start_fire(target_x, target_y, self.gun, self)


class Bots(Heroes):
    def draw(self, surface):
        super().draw(surface)
        self.draw_target_vector(surface)
