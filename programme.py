import numpy as np
import pygame as p

from os import listdir

from data import Colors
from sprite import Player, Section


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

    moveMap = {p.K_w: np.array([0.0, -1.0]),
               p.K_s: np.array([0.0, 1.0]),
               p.K_a: np.array([-1.0, 0.0]),
               p.K_d: np.array([1.0, 0.0]),

               #p.K_UP: np.array([0.0, -1.0]),
               #p.K_DOWN: np.array([0.0, 1.0]),
               p.K_LEFT: np.array([-1.0, 0.0]),
               p.K_RIGHT: np.array([1.0, 0.0])}

    worldSize = 100 # In number of blocks.
    blockSize = 24 # In pixels.
    sectionSize = 20 # In number of blocks.

    def __init__(self):
        self.running = True

        self.images = getImages()

        self.player = Player(image=self.images.get('knight3'),
                             x=0.0, y=0.0,
                             xScreen=self.screenWidth // 2,
                             yScreen=self.screenHeight // 2)

        self.rectsToDraw = p.sprite.Group()

        self.sections = [[Section(numBlocks=self.sectionSize,
                                  xMin=i*self.blockSize - self.screenWidth // 2,
                                  yMin=j*self.blockSize - self.screenHeight // 2,
                                  blockSize=self.blockSize)
                          for i in range(-self.worldSize // 2, self.worldSize // 2, self.sectionSize)]
                         for j in range(-self.worldSize // 2, self.worldSize // 2, self.sectionSize)]

        self.currentSections = []
        self.checkSections()

        for section in self.currentSections:
            for block in section.blocks:
                block.setScreenPos(self.player.pos)

    def manageEvents(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                self.running = False

    def update(self):
        self.move(p.key.get_pressed())
        self.checkSections()
        self.drawGame()

    def checkSections(self):
        # First element of self.currentSections is the specific section the player is/was in.
        try:
            if self.currentSections[0].inSection(*self.player.pos):
                return
        except IndexError:
            pass

        for section in self.currentSections:
            self.rectsToDraw.remove(*section.blocks)

        self.setSections()

        #for section in self.currentSections:
        #    for block in section.blocks:
        #        block.setScreenPos(self.player.pos)

        for section in self.currentSections:
            self.rectsToDraw.add(*section.blocks)

    def setSections(self):
        n = len(self.sections)

        for i, row in enumerate(self.sections):
            m = len(row)

            for j, section in enumerate(row):

                if section.inSection(*self.player.pos):
                    print(self.player.pos)
                    print(section.xMin, section.xMax, section.yMin, section.yMax)
                    print('')
                    self.currentSections = [section,
                                            self.sections[(i + 1) % n][(j + 1) % m],
                                            self.sections[(i + 1) % n][j % m],
                                            self.sections[(i + 1) % n][(j - 1) % m],
                                            self.sections[i % n][(j + 1) % m],
                                            #self.sections[i][j],
                                            self.sections[i % n][(j - 1) % m],
                                            self.sections[(i - 1) % n][(j + 1) % m],
                                            self.sections[(i - 1) % n][j % m],
                                            self.sections[(i - 1) % n][(j - 1) % m]]
                    return

        raise ValueError('Cannot find current sections')

    def move(self, pressed):
        moveArr = np.sum(self.moveMap[key] for key in self.moveMap if pressed[key])

        # Gravity.
        #moveArr += np.array([0.0, -1.0])

        if np.any(moveArr):
            self.player.pos += moveArr * self.player.maxSpeed

            for section in self.currentSections:
                for block in section.blocks:
                    block.setScreenPos(self.player.pos)
            #    block += moveArr
            #    block.rect.move_ip(*moveArr * self.player.maxSpeed)
            #    ##block.rect.clamp_ip(self.screen.get_rect())

    def drawGame(self):
        self.screen.fill(Colors.fill)

        self.drawWorld()
        self.drawPlayer()

    def drawPlayer(self):
        self.screen.blit(self.player.image, self.player.rect)

    def drawWorld(self):
        self.rectsToDraw.draw(self.screen)

        '''
        for rowPos, rowCol in zip(self.grid, self.colors):
            for blockPos, blockCol in zip(rowPos, rowCol):
                #if block.rect.colliderect(self.screen.get_rect()):
                #if np.linalg.norm(self.player.pos - block.screenPos) <= 1000.0:
                #if abs(xIndexBlock - xIndexPlayer) <= 20 or abs(yIndexBlock - yIndexPlayer) <= 20:
                #if np.all(np.abs(block.pos - self.player.pos) <= max(self.screenWidth, self.screenHeight) // 1.5):
                block.updateRect()
                p.draw.rect(self.screen, block.color, block.rect)
        '''

    def tickClock(self):
        self.clock.tick(self.maxFPS)
