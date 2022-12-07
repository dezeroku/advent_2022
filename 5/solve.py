def get_data():
    pairs = []
    with open("data") as data:
        moves_start = False
        moves = []
        stacks = []
        for line in data.readlines():
            # Read stacks

            if line == "\n":
                moves_start = True
                continue

            if moves_start:
                temp = line.strip().split()
                moves.append((int(temp[1]), int(temp[3]) - 1, int(temp[5]) - 1))
            else:
                # Read stack info
                l = len(line)
                count = (l + 1) // 4
                if line[0] != "[":
                    continue

                if not stacks:
                    stacks = [[] for _ in range(0, count)]

                for i in range(0, count):
                    data = line[4 * i : 4 * (i + 1)]
                    if "[" not in data:
                        continue

                    char = data[1]
                    stacks[i].append(char)

    return (list(map(lambda x: list(reversed(x)), stacks)), moves)


def apply_move(stacks, move):
    count, origin, to = move
    for _ in range(0, count):
        stacks[to].append(stacks[origin].pop())


def apply_move_batch(stacks, move):
    count, origin, to = move
    stacks[to] += stacks[origin][-count:]
    stacks[origin] = stacks[origin][:-count]


def main():
    stacks, moves = get_data()

    for move in moves:
        apply_move(stacks, move)

    print("".join(map(lambda x: x.pop(), stacks)))
    print()

    stacks, moves = get_data()
    for move in moves:
        apply_move_batch(stacks, move)

    print("".join(map(lambda x: x.pop(), stacks)))


if __name__ == "__main__":
    main()
