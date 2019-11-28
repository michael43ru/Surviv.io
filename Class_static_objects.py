import pygame
import math
from pygame.rect import Rect


pygame.init() # 'there is for test, i will delete it in the future


sc = pygame.display.set_mode((300, 200)) # это пример, для того, чтобы можно было тестить прогу, потом удалю

class Staticobjects(): # лучше вместо create везде прописать draw, чтобы больше по смыслу подходило
    def __init__(self, x, y, r, number_of_type, color):
        self.x = x
        self.y = y
        self.r = r
        self.type = number_of_type # у каждого типа объекта будет свой номер
        self.live = 10 # число жизней до разрушения, если что можно поменять
        self.color = color

    def collision_with_gamer(self, obj): # при столкновении с игроком, не пропускать игрока, возвращать угол объекта относительно игрока
        if self.type == 1: # куст дерево или что то круглое
            if math.hypot((obj.x - self.x), (obj.y - self.y)) <= (self.r + obj.r):
                if self.x == obj.x:
                    if obj.y < self.y:
                        return 0.5 * math.pi
                    else:
                        return -0.5 * math.pi
                elif self.y == obj.y:
                    if obj.x < self.x:
                        return 0
                    else:
                        return -math.pi
                else:
                    return math.atan((self.y - obj.y) / (self.x - obj.x))
            else:
                return 100 # если выводиться 100 это значит что нет столкновения, для других чисел выводится значение угла
                           # поворота объекта относительно игрока
        if self.type == 2: # ящик стена или что то прямоугольное
            if obj.x >= self.x:
                angle_90 = - 0.5 * math.pi
            elif obj.x < self.x:
                angle_90 = 0.5 * math.pi
            elif obj.y <= self.y:
                angle_90 = 0
            elif obj.y > self.y:
                angle_90 = - math.pi
            if self.x == obj.x:
                if obj.y <= self.y:
                    angle = - 0.5 * math.pi
                if obj.y > self.y:
                    angle = 0.5 * math.pi
            else:
                angle = - math.atan((self.y + 0.5 * self.r - obj.y) / (self.x + 0.5 * self.r - obj.x))
            if (self.x + self.r - obj.x - obj.r >= 0) and (self.x - obj.x - obj.r <= 0) and (
                    self.y + self.r - obj.y >= 0) and (self.y - self.r - obj.y <= 0):
                return angle_90
            elif (self.x + self.r - obj.x + obj.r >= 0) and (self.x - obj.x + obj.r <= 0) and (
                    self.y + self.r - obj.y >= 0) and (self.y - self.r - obj.y <= 0):
                return angle_90
            elif (self.x + self.r - obj.x >= 0) and (self.x - obj.x <= 0) and (
                    self.y + self.r - obj.y - obj.r >= 0) and (self.y - obj.y - obj.r <= 0):
                return angle_90
            elif (self.x + self.r - obj.x >= 0) and (self.x - obj.x <= 0) and (
                    self.y + self.r - obj.y + obj.r >= 0) and (self.y - self.r - obj.y + obj.r <= 0):
                return angle_90
            elif math.hypot((self.x - obj.x), (self.y - obj.y)) <= obj.r:
                return angle
            elif math.hypot((self.x + self.r - obj.x), (self.y - obj.y)) <= obj.r:
                return angle
            elif math.hypot((self.x - obj.x), (self.y + self.r - obj.y)) <= obj.r:
                return angle
            elif math.hypot((self.x + self.r - obj.x), (self.y + self.r - obj.y)) <= obj.r:
                return angle
            else:
                return 100

    def collision_with_fighter(self, obj): # применять в том случае, когда angle != 100
        pygame.event.get()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if math.hypot((pygame.mouse.get_pos() [0] - self.x), (pygame.mouse.get_pos() [1] - self.y)) <= self.r:
                if self.r >= 0.6:
                    self.r -= 0.5 # на сколько уменьшается радикс за один щелчкек
                else:
                    if self.type == 2:
                        return 1 # это значит надо примемить функцию присвоения предмета, объект уничтожить
                    else:
                        return 2 # просто уничтожить объект


class Tree(Staticobjects):
    def __init__(self, x, y, r, number_of_type, color, r_interior=5):
        Staticobjects.__init__(self, x, y, r, number_of_type, color)
        self.r_interior = r_interior # радиус ствола

    def create_tree(self): # создание дерева или куста, для каждого объекта будет отдельная функция создания
        pygame.draw.circle(sc, (255, 255, 255), [self.x, self.y], self.r_interior) # рисует ствол
        pygame.draw.circle(sc, (0, 128, 0), [self.x, self.y], self.r)


class Box(Staticobjects):
    def __init__(self, x, y, r, number_of_type, color, interior_stuff):
        Staticobjects.__init__(self, x, y, r, number_of_type, color)
        self.interior_stuff = interior_stuff

    def create_box(self):
        pygame.draw.rect(sc, (255, 255, 255), (self.x - self.r, self.y - self.r, self.r, self.r))

    def open_box(self): # при открытии ящика уничтожить его, человеку присвоить предмет
        pass


class Stone(Staticobjects):
    def __init__(self, x, y, r, number_of_type, color, r_interior=5):
        Staticobjects.__init__(self, x, y, r, number_of_type, color)

    def create_box(self)
        pygame.draw.rect(sc, (0, 0, 0), (self.x - self.r, self.y - self.r, self.r, self.r))
