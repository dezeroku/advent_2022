def main():
    def set_pixel(cycle, sprite, display):
        display_index = (cycle - 1) % 40
        if display_index in sprite:
            display[cycle - 1] = 1

    with open("data") as data:
        # Cycle denotes at the START of which cycle we are right now
        sprite = set(range(3))
        display = [0 for _ in range(240)]
        cycle = 1
        values = []
        register = 1
        to_check = set(20 + 40 * x for x in range(0, 6))
        for line in data:
            cmd = line.strip().split()
            if len(cmd) == 1:
                if cycle in to_check:
                    values.append(register * cycle)

                set_pixel(cycle, sprite, display)

                cycle += 1
            else:
                diff = int(cmd[1])
                if cycle in to_check:
                    values.append(register * cycle)
                elif cycle + 1 in to_check:
                    values.append(register * (cycle + 1))

                set_pixel(cycle, sprite, display)
                set_pixel(cycle + 1, sprite, display)

                register += diff
                sprite = set(range(register - 1, register + 2))
                cycle += 2

    print(sum(values))

    for i in range(1, 241):
        print("#" if display[i - 1] else ".", end="")
        if i % 40 == 0:
            print()


if __name__ == "__main__":
    main()
