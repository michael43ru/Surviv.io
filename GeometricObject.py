
class Figure:
    #Задаются координаты центра фигуры
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Ball(Figure):
    def __init__(self, x, y, r):
        super().__init__(x, y, r, r)
        self.r = r
