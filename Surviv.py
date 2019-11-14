class World:
    static_objects = []
    dinamic_objects = []

    bots = []
    boxes = []
    bushes = []
    trees = []
    stones = []
    bullets = []
    bombs = []
    drops = []
    taken_objects = []
    player = Player()

    dinamic_objects.extend([bots, bullets, bombs, player])
    static_objects.extend([boxes, trees, stones])


class Object:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0


class La



