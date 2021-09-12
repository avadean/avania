from programme import Programme, updateDisplay


def main():
    prog = Programme()

    while prog.running:
        prog.manageEvents()

        prog.update()

        prog.drawGame()

        prog.tickClock()

        updateDisplay()


if __name__ == '__main__':
    main()
