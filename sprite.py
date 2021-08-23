from pygame import Surface


class Sprite:
    def __init__(self, name, x, y, size):
        self.name = name

        self.x = x
        self.y = y

        self.size = size

        self.image = Surface((size, size))
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Pod(Sprite):
    def __init__(self, image):
        super().__init__(name='pod', x=100, y=250, size=75)

        self.image = image
        self.speed = 10.0
