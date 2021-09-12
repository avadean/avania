import numpy as np
import pygame as p

from os import listdir

from data import Colors
from sprite import Block, Player


def updateDisplay():
    p.display.flip()


def getImages():
    imagesDir = 'images/'
    size = 50

    pngs = [item[:-4] for item in listdir(imagesDir) if item.endswith('.png')]

    images = {png: p.transform.scale(p.image.load(f'{imagesDir}{png}.png').convert_alpha(),
                                     (size, size)) for png in pngs}

    return images


class Programme:
    p.init()

    screenWidth = 960 #768
    screenHeight = 640 #512

    screen = p.display.set_mode((screenWidth, screenHeight))

    clock = p.time.Clock()

    maxFPS = 60

    moveMap = {p.K_w: np.array([0.0, 1.0]),
               p.K_s: np.array([0.0, -1.0]),
               p.K_a: np.array([1.0, 0.0]),
               p.K_d: np.array([-1.0, 0.0]),

               #p.K_UP: np.array([0.0, 1.0]),
               #p.K_DOWN: np.array([0.0, -1.0]),
               p.K_LEFT: np.array([1.0, 0.0]),
               p.K_RIGHT: np.array([-1.0, 0.0])}

    worldSize = 50

    def __init__(self):
        self.running = True

        self.images = getImages()

        self.player = Player(image=self.images.get('knight3'),
                             x=self.screenWidth // 2,
                             y=self.screenHeight // 2)

        self.grid = np.array([[Block(x, y) for x in range(-self.worldSize, self.worldSize)] for y in range(-50, 50)])

    def manageEvents(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                self.running = False

    def update(self):
        self.player.getApproxIndex()
        self.move(p.key.get_pressed())

    def move(self, pressed):
        moveArr = np.sum(self.moveMap[key] for key in self.moveMap if pressed[key])

        blockBeneath = self.player.rect.bottom
        #moveArr += np.array([0.0, -1.0])

        #blockBeneath = self.player.rect.y

        if np.any(moveArr):
            self.player.pos -= moveArr * self.player.maxSpeed

            for row in self.grid:
                for block in row:
                    block.screenPos += moveArr * self.player.maxSpeed
                    #block.rect.move_ip(*moveArr * self.player.maxSpeed)
                    ##block.rect.clamp_ip(self.screen.get_rect())

    def drawGame(self):
        self.screen.fill(Colors.fill)

        self.drawWorld()
        self.drawPlayer()

    def drawPlayer(self):
        self.screen.blit(self.player.image, self.player.rect)
        #print('player pos', self.player.pos)

    def drawWorld(self):
        for row in self.grid:
            for block in row:
                ##if block.rect.colliderect(self.screen.get_rect()):
                ##if np.linalg.norm(self.player.pos - block.screenPos) <= 1000.0:
                ##if abs(xIndexBlock - xIndexPlayer) <= 20 or abs(yIndexBlock - yIndexPlayer) <= 20:
                ##if np.all(np.abs(block.pos - self.player.pos) <= max(self.screenWidth, self.screenHeight) // 1.5):
                block.updateRect()
                p.draw.rect(self.screen, block.color, block.rect)

    def tickClock(self):
        self.clock.tick(self.maxFPS)
