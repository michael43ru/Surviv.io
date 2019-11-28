class Red_zone:
    def __init__(self):
        self.x = rnd(0.3 * s, 0.7 * s)
        self.y = rnd(0.3 * s, 0.5 * s)
        self.r = 0.5 * s
        self.t = time.time()

        # self.image = pg.image.load(path.join(img_dir, "Red_zone.png")).convert()
        self.image = pg.transform.scale(red_zone_img, (1000, 1000))
        self.image.set_colorkey(white)
        self.image_rect = self.image.get_rect()

    def get_center(self):
        self.r = self.r / 2
        self.x = rnd(-self.r + self.x, self.r + self.x)
        self.y = rnd(-(self.r ** 2 - self.x ** 2) + self.y,
                     (self.r ** 2 - self.x ** 2) + self.y)
        self.R = self.r * 3

    def reduction(self): # Не доделано
        self.R -= self.v
