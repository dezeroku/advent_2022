import heapq


def read_data():
    elves = []
    with open("data") as data:
        current = []
        for line in data.readlines():
            if line == "\n":
                elves.append(current)
                current = []
            else:
                current.append(int(line))

        elves.append(current)
    return elves


def main():
    elves = read_data()
    summ = map(lambda x: sum(x), elves)

    heap = []
    for elem in summ:
        heapq.heappush(heap, elem)

    print(heapq.nlargest(1, heap)[0])
    print()
    print(sum(heapq.nlargest(3, heap)))


if __name__ == "__main__":
    main()
