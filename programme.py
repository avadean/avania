import numpy as np
import pygame as p

from os import listdir

from sprite import Pod


def updateDisplay():
    p.display.flip()


def getImages():
    imagesDir = 'images/'
    size = 50

    pngs = [item[:-4] for item in listdir(imagesDir) if item.endswith('.png')]

    images = {png: p.transform.scale(p.image.load(f'{imagesDir}{png}.png').convert_alpha(), (size, size)) for png in pngs}

    return images


class Programme:
    p.init()

    windowWidth = 768
    windowHeight = 512

    screen = p.display.set_mode((windowWidth, windowHeight))

    clock = p.time.Clock()

    maxFPS = 60

    moveMap = {p.K_w: np.array([0.0, -1.0]),
               p.K_s: np.array([0.0, 1.0]),
               p.K_a: np.array([-1.0, 0.0]),
               p.K_d: np.array([1.0, 0.0])}

    def __init__(self, sprites):
        self.running = True

        self.images = getImages()

        self.pod = Pod(self.images.get('pod'))

        self.sprites = sprites

    def manageEvents(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                self.running = False

            elif event.type == p.KEYDOWN:
                self.move(p.key.get_pressed())

    def move(self, pressed):
        moveArr = np.sum(self.moveMap[key] for key in self.moveMap if pressed[key])
        # TODO: GRAVITY
        if np.any(moveArr):
            for sprite in self.sprites:
                sprite.rect.move_ip(*moveArr * self.pod.speed)
                sprite.rect.clamp_ip(self.screen.get_rect())

    def drawGame(self):
        self.screen.fill(Colors.fill)

        self.drawPod()
        self.drawSprites()

    def drawPod(self):
        self.screen.blit(self.pod.image,
                         p.Rect(self.pod.x, self.pod.y, self.pod.size, self.pod.size))

    def drawSprites(self):
        for sprite in self.sprites:
            self.screen.blit(self.images[sprite.name], sprite.rect)

    def tickClock(self):
        self.clock.tick(self.maxFPS)



class Colors:
    white = p.Color('white')
    black = p.Color('black')

    fill = white
