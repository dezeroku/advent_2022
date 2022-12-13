import heapq
import math
import operator
from functools import partial, reduce


class Monkey:
    def __init__(
        self, items=[], operation=None, test=None, index_true=None, index_false=None
    ):
        self.items = items
        self.operation = operation
        self.test = test
        self.index_true = index_true
        self.index_false = index_false

        self.times_inspected = 0

    def __repr__(self):
        return f"{self.items}: {self.operation} - {self.test} - {self.index_true} - {self.index_false}"


def get_operation(entry: []):
    # Supported variables: "old" and numbers
    # Supported operations: - + * /
    def calculate(item):
        first_var = int(entry[0]) if entry[0] != "old" else item
        second_var = int(entry[2]) if entry[2] != "old" else item

        match entry[1]:
            case "+":
                return first_var + second_var
            case "-":
                return first_var - second_var
            case "*":
                return first_var * second_var
            case "/":
                return first_var / second_var
            case _:
                raise Exception(f"Unsupported operator {entry[1]}")

    return calculate


def get_data():
    monkeys = []
    dividers = []
    with open("data") as data:
        for line in data:
            if line.startswith("Monkey"):
                current = Monkey()
                continue

            if line == "\n":
                monkeys.append(current)
                current = None
                continue

            temp = line.strip().split()

            if temp[0] == "Starting":
                current.items = list(
                    map(lambda x: int(x.strip().rstrip(",")), temp[2:])
                )

            elif temp[0] == "Operation:":
                current.operation = get_operation(temp[3:])

            elif temp[0] == "Test:":
                divisible_by = int(temp[3])
                dividers.append(divisible_by)
                test = partial(lambda y, x: not (x % y), divisible_by)
                current.test = test

            elif temp[0] == "If":
                index = int(temp[5])
                if temp[1] == "true:":
                    current.index_true = index
                else:
                    current.index_false = index

        if current is not None:
            # Handle lack of last newline
            monkeys.append(current)

    return monkeys, reduce(operator.mul, dividers, 1)


def perform_round(monkeys, lcm=0):
    length = len(monkeys)
    for monkey in monkeys:
        while monkey.items:
            monkey.times_inspected += 1
            item = monkey.items.pop(0)
            item = monkey.operation(item)
            if not lcm:
                item = math.floor(item / 3)
            else:
                item = item % lcm
            target_index = (
                monkey.index_true if monkey.test(item) else monkey.index_false
            )
            monkeys[target_index].items.append(item)


def main():
    monkeys, _ = get_data()

    for _ in range(20):
        perform_round(monkeys)

    print(operator.mul(*heapq.nlargest(2, map(lambda x: x.times_inspected, monkeys))))
    print()

    monkeys, lcm = get_data()
    for i in range(10000):
        perform_round(monkeys, lcm)

    print(operator.mul(*heapq.nlargest(2, map(lambda x: x.times_inspected, monkeys))))


if __name__ == "__main__":
    main()
