def get_data():
    with open("data") as data:
        return data.read()


def find_unique(bufferstream, count):
    current = bufferstream[:count]
    l = count
    while len(set(current)) != count:
        l += 1
        current = bufferstream[l - count : l]

    return l


def main():
    bufferstream = get_data()

    l = find_unique(bufferstream, 4)

    print(l)
    print()

    l = find_unique(bufferstream, 14)
    print(l)


if __name__ == "__main__":
    main()
