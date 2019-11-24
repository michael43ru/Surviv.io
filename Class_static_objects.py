import pygame
import math


class Static_objects:
    def __init__(self, x, y, r, number_of_type, color):
        self.x = x
        self.y = y
        self.r = r
        self.type = number_of_type # у каждого типа объекта будет свой номер
        self.live = 10 # число жизней до разрушения, если что можно поменять
        self.color = color

    def collision_with_gamer(self, obj): # при столкновении с игроком, не пропускать игрока
        if self.type == 1: # куст дерево или что то круглое
            if math.hypot((self.x - obj.x), (self.y - obj.y)) <= (self.r + obj.r):
                if self.x == obj.x:
                    if self.y < obj.y:
                        return 0.5 * math.pi
                    else:
                        return -0.5 * math.pi
                elif self.y == obj.y:
                    if self.x < obj.x:
                        return 0
                    else:
                        return -math.pi
                else:
                    return math.atan((obj.y - self.y) / (obj.x - self.x))
            else:
                return 100 # если выводиться 100 это значит что нет столкновения, для других чисел выводится значение угла
                           # поворота объекта относительно игрока
        if self.type == 2: # ящик стена или что то прямоугольное
            


class Solid_objects(Static_objects): # неразрушаемые объекты
    def create_tree(self): # создание дерева или куста, для каждого объекта будет отдельная функция создания
        pass

    def create_box(self): # при создании прикрепить к нему предмет со своим номером
        pass

    def collision_with_bullet(self): # при столкновении уничтожить пулю
        pass

    def collision_with_fighter(self): # если это ящик, то уменьшить колво жизней, для остальных не уменьшать (кулаки)
        pass

    def open_box(self): # при открытии ящика уничтожить его, человеку присвоить предмет
        pass


class Not_solid_objects(Static_objects):
    def create_stone(self):
        pass

    def collision_with_bullets(self): # при столкновении с пулей уничтожить пулю, уменьшить радиус камня
        pass




