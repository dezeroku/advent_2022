def get_data():
    pairs = []
    with open("data") as data:
        for line in data.readlines():
            x, y = line.strip().split(",")
            pairs.append((tuple(map(int, x.split("-"))), tuple(map(int, y.split("-")))))

    return pairs


def find_complete_overlapping(pairs):
    return filter(
        lambda x: (x[0][0] <= x[1][0] and x[0][1] >= x[1][1])
        or (x[1][0] <= x[0][0] and x[1][1] >= x[0][1]),
        pairs,
    )


def find_all_overlapping(pairs):
    return filter(
        lambda x: (x[0][0] <= x[1][1] and x[0][0] >= x[1][0])
        or (x[0][1] <= x[1][1] and x[0][1] >= x[1][0])
        or (x[1][0] <= x[0][1] and x[1][0] >= x[0][0])
        or (x[1][1] <= x[0][1] and x[1][1] >= x[0][0]),
        pairs,
    )


def main():
    pairs = get_data()

    print(sum(1 for _ in find_complete_overlapping(pairs)))
    print()
    print(sum(1 for _ in find_all_overlapping(pairs)))


if __name__ == "__main__":
    main()
