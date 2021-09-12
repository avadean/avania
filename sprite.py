from data import worldColors

from numpy import array
from pygame import sprite, Surface
from random import choice


class Section:
    def __init__(self, numBlocks, xMin, yMin, blockSize):
        self.blocks = [Block(x=i*blockSize + xMin,
                             y=j*blockSize + yMin,
                             width=blockSize,
                             height=blockSize) for i in range(numBlocks) for j in range(numBlocks)]

        self.xMin = min([b.pos[0] for b in self.blocks])
        self.xMax = max([b.pos[0] for b in self.blocks]) + blockSize

        self.yMin = min([b.pos[1] for b in self.blocks])
        self.yMax = max([b.pos[1] for b in self.blocks]) + blockSize

    def inSection(self, x, y):
        #print(self.xMin, self.yMin, self.xMax, self.yMax, x, y)
        return True if (self.xMin <= x <= self.xMax and self.yMin <= y <= self.yMax) else False


class Block(sprite.Sprite):
    def __init__(self, x, y, width, height, color=None):
        super().__init__()

        self.color = choice(list(worldColors.keys())) if color is None else color
        self.solid = True if self.color == 'brown' else False

        self.pos = array([x, y], dtype=float)

        self.image = Surface((width, height))
        self.image.fill(self.color)

        self.rect = self.image.get_rect()

    def __add__(self, other):
        x, y = other
        self.rect.x += x
        self.rect.y += y

    def setScreenPos(self, playerPos):
        self.rect.x, self.rect.y = self.pos - playerPos


class Player:
    def __init__(self, image, x, y, xScreen=None, yScreen=None):
        self.pos = array([x, y], dtype=float)
        xScreen = xScreen if xScreen is not None else x
        yScreen = yScreen if yScreen is not None else y
        self.screenPos = (xScreen, yScreen)

        self.image = image
        self.rect = self.image.get_rect(center=self.screenPos)

        self.acceleration = 1
        self.maxSpeed = 5
