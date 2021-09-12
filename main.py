from programme import Programme, updateDisplay


def main():
    prog = Programme()
    i=0
    while prog.running:
        prog.manageEvents()

        prog.update()

        prog.tickClock()

        updateDisplay()

        if i % 10 == 0:
            pass#print(prog.clock.get_fps())

        i += 1


if __name__ == '__main__':
    main()
