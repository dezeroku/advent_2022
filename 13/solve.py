import ast
from collections import deque
from functools import cmp_to_key
from itertools import zip_longest


def compare(left, right):
    to_check = deque()
    to_check.append((left, right))

    while to_check:
        left, right = deque.popleft(to_check)

        # Because of the list padding
        if left is None:
            return 1

        if right is None:
            return -1

        if type(left) == type(right) == int:
            if left < right:
                return 1
            elif left > right:
                return -1

            continue

        if type(left) == type(right) == list:
            deque.extendleft(to_check, reversed(list(zip_longest(left, right))))
            continue

        if type(left) != list:
            to_check.appendleft(([left], right))
        else:
            to_check.appendleft((left, [right]))

    return 1


def main():
    with open("data") as data:
        index = 1
        right_order = []
        packets = [[[2]], [[6]]]
        left = None
        right = None
        for line in data:
            if line == "\n":
                if compare(left, right) == 1:
                    right_order.append(index)

                index += 1
                packets.append(left)
                packets.append(right)
                left = None
                right = None
                continue

            if left is None:
                left = ast.literal_eval(line)
                continue

            if right is None:
                right = ast.literal_eval(line)
                continue

        # Take the last possibly not "\n" line into consideration
        if left is not None and right is not None:
            packets.append(left)
            packets.append(right)
            if compare(left, right) == 1:
                right_order.append(index)

    print(sum(right_order))

    packets.sort(key=cmp_to_key(compare), reverse=True)

    print((packets.index([[2]]) + 1) * (packets.index([[6]]) + 1))


if __name__ == "__main__":
    main()
