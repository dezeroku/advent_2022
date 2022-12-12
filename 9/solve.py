import math


def get_data():
    moves = []
    with open("data") as data:
        for line in data.readlines():
            direction, count = line.strip().split()
            count = int(count)

            def assign(direction, count):
                match direction:
                    case "R":
                        return count, 0
                    case "L":
                        return -count, 0
                    case "D":
                        return 0, -count
                    case "U":
                        return 0, count
                    case _:
                        raise Exception(format("Move could not be parsed: %s", line))

            move = assign(direction, count)
            moves.append(move)

    return moves


def fixup_tail(head, tail):
    head_x, head_y = head
    tail_x, tail_y = tail

    if head_x != tail_x and head_y != tail_y:
        if head_x not in range(tail_x - 1, tail_x + 2) or head_y not in range(
            tail_y - 1, tail_y + 2
        ):
            if head_x > tail_x:
                tail_x = math.ceil((head_x + tail_x) / 2)
            else:
                tail_x = math.floor((head_x + tail_x) / 2)

            if head_y > tail_y:
                tail_y = math.ceil((head_y + tail_y) / 2)
            else:
                tail_y = math.floor((head_y + tail_y) / 2)

    elif head_x > tail_x + 1:
        tail_x += 1
    elif head_x < tail_x - 1:
        tail_x -= 1
    elif head_y > tail_y + 1:
        tail_y += 1
    elif head_y < tail_y - 1:
        tail_y -= 1

    return tail_x, tail_y


def apply_moves(moves, head, rope):
    visited = set()
    visited.add(rope[-1])

    def fixup_rope(rope, head):
        rope[0] = fixup_tail(head, rope[0])
        for i in range(1, len(rope)):
            rope[i] = fixup_tail(rope[i - 1], rope[i])

        visited.add(rope[-1])
        return rope

    for move in moves:
        x, y = move
        if x != 0:
            count = abs(x)
            direction = int(math.copysign(1, x))
            for _ in range(0, count):
                head = (head[0] + direction, head[1])

                rope = fixup_rope(rope, head)
                visited.add(rope[-1])
        else:
            count = abs(y)
            direction = int(math.copysign(1, y))
            for _ in range(0, count):
                head = (head[0], head[1] + direction)

                rope = fixup_rope(rope, head)
                visited.add(rope[-1])

    return head, rope, visited


def print_visited(visited, head=None, rope=None):
    length = len(rope)
    x_min, x_max = (
        min(map(lambda x: x[0], visited)) - 2 - length,
        max(map(lambda x: x[0], visited)) + 2 + length,
    )
    y_min, y_max = (
        min(map(lambda x: x[1], visited)) - 2 - length,
        max(map(lambda x: x[1], visited)) + 2 + length,
    )

    for y in range(y_max, y_min - 1, -1):
        row = ""
        for x in range(x_min, x_max + 1):
            location = (x, y)
            if head is not None and location == head:
                row += "H"
            elif rope is not None and location in rope:
                row += str(rope.index(location))
            elif location == (0, 0):
                row += "s"
            elif location in visited:
                row += "#"
            else:
                row += "."
        print(row)
    print()


def main():
    moves = get_data()
    head = (0, 0)
    rope = [(0, 0)]

    head, rope, visited = apply_moves(moves, head, rope)
    print(len(visited))
    # print_visited(visited, head, rope)

    head = (0, 0)
    rope = [(0, 0) for _ in range(9)]

    head, rope, visited = apply_moves(moves, head, rope)
    print(len(visited))
    # print_visited(visited, head, rope)


if __name__ == "__main__":
    main()
