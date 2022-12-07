def get_data():
    pairs = []
    with open("data") as data:
        for line in data.readlines():
            x, y = line.strip().split()
            pairs.append((x, y))

    return pairs


def shape_points(shape):
    mapping = {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }

    return mapping[shape]


def round_points(pair):
    mapping = {
        ("A", "X"): 3,
        ("A", "Y"): 6,
        ("A", "Z"): 0,
        ("B", "X"): 0,
        ("B", "Y"): 3,
        ("B", "Z"): 6,
        ("C", "X"): 6,
        ("C", "Y"): 0,
        ("C", "Z"): 3,
    }

    return mapping[pair]


def points_second(pair):
    def lose(x):
        return {
            "A": shape_points("Z"),
            "B": shape_points("X"),
            "C": shape_points("Y"),
        }[x]

    def draw(x):
        return {
            "A": shape_points("X"),
            "B": shape_points("Y"),
            "C": shape_points("Z"),
        }[x]

    def win(x):
        return {
            "A": shape_points("Y"),
            "B": shape_points("Z"),
            "C": shape_points("X"),
        }[x]

    def play(x, y):
        return {
            "X": 0 + lose(x),
            "Y": 3 + draw(x),
            "Z": 6 + win(x),
        }[y]

    op, result = pair
    return play(op, result)


def main():
    pairs = get_data()
    points = 0
    for pair in pairs:
        points += shape_points(pair[1])
        points += round_points(pair)

    print(points)
    print()

    points = 0
    for pair in pairs:
        points += points_second(pair)

    print(points)


if __name__ == "__main__":
    main()
