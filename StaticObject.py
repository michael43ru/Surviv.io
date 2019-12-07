import pygame
import math


class Staticobjects(): # лучше вместо create везде прописать draw, чтобы больше по смыслу подходило
    def __init__(self, x, y, r, number_of_type, color):
        self.x = x
        self.y = y
        self.r = r
        self.type = number_of_type # у каждого типа объекта будет свой номер
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
                        return 2 # это значит надо примемить функцию присвоения предмета, объект уничтожить
                    else:
                        return 1 # просто уничтожить объект


class Tree(Staticobjects):
    def __init__(self, x, y, r, number_of_type, color, r_interior=5):
        Staticobjects.__init__(self, x, y, r, number_of_type, color)
        self.r_interior = r_interior # радиус ствола
        self.tree_surf = pygame.image.load('bush.png') # здесь ссылка на файл с кустом
        self.tree_rect = self.tree_surf.get_rect(bottomright=((self.x + self.r), (self.y + self.r)))

    def create_tree(self, sc): # создание дерева или куста, для каждого объекта будет отдельная функция создания
        pygame.draw.circle(sc, (255, 255, 255), [self.x, self.y], self.r_interior) # рисует ствол
        sc.blit(self.tree_surf, self.tree_rect)

    def collision_with_fighter(self, event): # применять в том случае, когда angle != 100
        pygame.event.get()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if math.hypot((pygame.mouse.get_pos()[0] - self.x), (pygame.mouse.get_pos()[1] - self.y)) <= self.r:
                if self.r >= 0.6:
                    self.r *= 0.8 # на сколько уменьшается радикс за один щелчкек
                    self.tree_surf = pygame.transform.scale(self.tree_surf, (self.r * 0.8), (self.r * 0.8))
                else:
                    return 0 # это значит что надо перестать рисовать дерево


class Box(Staticobjects):
    def __init__(self, x, y, r, number_of_type, color, interior_stuff):
        Staticobjects.__init__(self, x, y, r, number_of_type, color)
        self.interior_stuff = interior_stuff
        self.box_surf = pygame.image.load('box.png') # здесь ссылка на файл с ящиком
        self.box_rect = self.box_surf.get_rect(bottomright=((self.x + self.r), (self.y + self.r)))
        if self.interior_stuff == 1:
            self.object_in_the_box =pygame.image.load('gun.png')
            self.object_in_the_box_rect = self.object_in_the_box.get_rect(
                bottomright=((self.x + self.r), (self.y + self.r)))
        if self.interior_stuff == 2:
            self.object_in_the_box = pygame.image.load('heart.png')
            self.object_in_the_box_rect = self.object_in_the_box.get_rect(
                bottomright=((self.x + self.r), (self.y + self.r)))
        if self.interior_stuff == 3:
            self.object_in_the_box = pygame.image.load()
            self.object_in_the_box_rect = self.object_in_the_box.get_rect(
                bottomright=((self.x + self.r), (self.y + self.r)))

    def create_box(self, sc):
        sc.blit(self.box_surf, self.box_rect)

    def collision_with_fighter(self, event): # применять в том случае, когда angle != 100
        pygame.event.get()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if math.hypot((pygame.mouse.get_pos()[0] - self.x - 0.5 * self.r),
                          (pygame.mouse.get_pos()[1] - self.y - 0.5 * self.r)) <= self.r:
                if self.r >= 0.6:
                    self.r *= 0.8 # на сколько уменьшается радикс за один щелчкек
                    self.box_surf = pygame.transform.scale(self.box_surf, (self.r * 0.8), (self.r * 0.8))
                else:
                    return 0 # это значит что надо перестать рисовать ящик, и вызвать функцию create_stuff, при этом открыть игроку возможность брать предметы

    def create_stuff(self, sc):
        sc.blit(self.object_in_the_box, self.object_in_the_box_rect)

    def get_stuff(self, event):
        pygame.event.get()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if math.hypot((pygame.mouse.get_pos()[0] - self.x - 0.5 * self.r),
                              (pygame.mouse.get_pos()[1] - self.y - 0.5 * self.r)) <= self.r:
                    return 0 # начать рисовать предмет на человеке

    def open_box(self): # при открытии ящика уничтожить его, начать отрисовку внутреннего стаффа
        return 0


class Stone(Staticobjects):
    def __init__(self, x, y, r, number_of_type, color, r_interior=5):
        Staticobjects.__init__(self, x, y, r, number_of_type, color)


    def create_stone(self, sc):
        pygame.draw.circle(sc, (0, 0, 0), [self.x, self.y], self.r)

    def collision_with_fighter(self, event): # применять в том случае, когда angle != 100
        pygame.event.get()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if math.hypot((pygame.mouse.get_pos()[0] - self.x), (pygame.mouse.get_pos()[1] - self.y)) <= self.r:
                if self.r >= 0.6:
                    self.r *= 0.8 # на сколько уменьшается радикс за один щелчкек
                    self.tree_surf = pygame.transform.scale(self.tree_surf, (self.r * 0.8), (self.r * 0.8))
                else:
                    return 0 # это значит что надо перестать рисовать камень
