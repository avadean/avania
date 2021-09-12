from programme import Programme, updateDisplay
from sprite import Sprite


def main():
    sprites = [Sprite(name='black', x=50*i, y=100*i, size=50) for i in range(3)]

    prog = Programme(sprites=sprites)

    while prog.running:
        prog.manageEvents()

        prog.drawGame()

        prog.tickClock()

        updateDisplay()


if __name__ == '__main__':
    main()
