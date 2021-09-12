from data import worldColors

from numpy import array
from pygame import Rect
from random import choice


blockSize = 32


class Block:
    def __init__(self, xIndex, yIndex):
        self.size = blockSize

        self.pos = (xIndex * self.size, yIndex * self.size)
        self.screenPos = array([*self.pos], dtype=float)

        self.rect = Rect(*self.screenPos, self.size, self.size)

        self.color = choice(list(worldColors.keys()))
        self.solid = True if self.color == 'brown' else False

    def updateRect(self):
        self.rect.update(*self.screenPos, self.size, self.size)


class Player:
    def __init__(self, image, x, y):
        self.pos = array([x, y], dtype=float)
        self.screenPos = (x, y)

        self.image = image
        self.rect = self.image.get_rect(center=self.screenPos)

        self.acceleration = 1
        self.maxSpeed = 5

    def getApproxIndex(self):
        return self.pos // blockSize
