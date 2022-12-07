import string


def get_data():
    rucksacks = []
    with open("data") as data:
        for line in data.readlines():
            line = line.strip()
            l = len(line) // 2
            first = line[0:l]
            second = line[l:]
            assert len(first) == len(second)
            rucksacks.append((first, second))

    return rucksacks


def get_duplicate(rucksack):
    first, second = set(rucksack[0]), set(rucksack[1])

    return first.intersection(second).pop()


def get_priority(char):
    if char in string.ascii_lowercase:
        return ord(char) - 96
    else:
        return ord(char) - 38


def find_triple(rucksacks):
    length = len(rucksacks)
    for i in range(1, length):
        if rucksacks[0].intersection(rucksacks[i]):
            temp = rucksacks[0].intersection(rucksacks[i])
            for j in range(i + 1, length):
                if temp.intersection(rucksacks[j]):
                    return (i, j, temp.intersection(rucksacks[j]).pop())


def main():
    rucksacks = get_data()
    points = 0
    for rucksack in rucksacks:
        duplicate = get_duplicate(rucksack)
        points += get_priority(duplicate)

    print(points)
    print()

    points = 0
    rucksacks = list(map(lambda x: set(x[0]).union(set(x[1])), rucksacks))
    while rucksacks:
        (i, j, value) = find_triple(rucksacks)
        points += get_priority(value)
        del rucksacks[j]
        del rucksacks[i]
        del rucksacks[0]

    print(points)


if __name__ == "__main__":
    main()
