import math
from functools import reduce


def get_data():
    with open("data") as data:
        connections = []
        for line in data.readlines():
            points = map(lambda x: x.strip().split(","), line.strip().split("->"))
            points = list(map(lambda x: tuple(map(int, x)), points))
            connections.append(points)

        connections_uni = reduce(lambda x, y: x + y, connections, [])

        xs = list(map(lambda x: x[0], connections_uni))
        ys = list(map(lambda x: x[1], connections_uni))

        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)

        col_offset = min_x
        col_count = max_x - min_x + 1
        row_offset = min_y
        row_count = max_y - min_y + 1

        # Add this just in case, so it's easier to trace the sand path
        additional_rows = row_offset

        # 0 for nothing
        # 1 for stone
        # 2 for sand in the future
        grid = [
            [0 for _ in range(col_count)] for _ in range(row_count + additional_rows)
        ]

        for connection in connections:
            previous = None
            for point in connection:
                point = (point[0] - col_offset, point[1] - row_offset + additional_rows)
                grid[point[1]][point[0]] = 1
                if previous:
                    # mark path from previous to current
                    if previous[0] != point[0]:
                        direction = -int(math.copysign(1, previous[0] - point[0]))
                        for i in range(0, abs(previous[0] - point[0])):
                            grid[previous[1]][previous[0] + direction * i] = 1
                    if previous[1] != point[1]:
                        direction = -int(math.copysign(1, previous[1] - point[1]))
                        for i in range(0, abs(previous[1] - point[1])):
                            grid[previous[1] + direction * i][previous[0]] = 1

                previous = point

    return row_offset, col_offset, grid


def print_grid(grid):
    for row in grid:
        print("".join(map(str, row)))


def find_a_place(grid, sand, row_count, col_count):
    # I don't like recursion :/
    # But will have to do for now
    def is_in_bounds(point):
        if point[0] < 0 or point[0] > row_count - 1:
            return False
        if point[1] < 0 or point[1] > col_count - 1:
            return False

        return True

    # Check if sand can be inserted at all
    if grid[sand[0]][sand[1]] != 0:
        return False

    # Go down as much as possible
    previous = sand
    while True:
        if not is_in_bounds(sand):
            return False

        if grid[sand[0]][sand[1]] == 0:
            previous = sand
            sand = (sand[0] + 1, sand[1])
        else:
            break

    alternative_left = (sand[0], sand[1] - 1)
    if not is_in_bounds(alternative_left):
        return False

    elif grid[alternative_left[0]][alternative_left[1]] != 0:
        # We can't go left, try right now
        alternative_right = (sand[0], sand[1] + 1)
        if not is_in_bounds(alternative_right):
            return False
        elif grid[alternative_right[0]][alternative_right[1]] != 0:
            # Use our fallback field
            grid[previous[0]][previous[1]] = 2
            return True
        else:
            # Try to find solution further on right
            return find_a_place(grid, alternative_right, row_count, col_count)
    else:
        # See if left can be used further
        return find_a_place(grid, alternative_left, row_count, col_count)


def fill_with_sand(grid, row_offset, col_offset):
    # Process sand until there is one that doesn't land anywhere on grid
    units_landed = 0
    starting_point = (0, 500 - col_offset)
    row_count = len(grid)
    col_count = len(grid[0])

    while find_a_place(grid, starting_point, row_count, col_count):
        units_landed += 1
        # print_grid(grid)

    return units_landed


def fill_with_sand_floor(grid, row_offset, col_offset):
    # A naive approach
    # Extend the grid to proper size (it's probably much too much, but better safe than sorry) and call the previous implementation
    required_side_buffer = (len(grid) + len(grid[0])) * 4
    col_offset = col_offset - required_side_buffer

    # Extend grid
    new_grid = []
    for row in grid:
        new_grid.append(
            [0 for _ in range(required_side_buffer)]
            + row
            + [0 for _ in range(required_side_buffer)]
        )

    # Add additional empty row:
    new_grid.append([0 for _ in range(len(new_grid[0]))])

    # Add floor
    new_grid.append([1 for _ in range(len(new_grid[0]))])

    # print_grid(new_grid)
    return fill_with_sand(new_grid, row_offset, col_offset)


def main():
    row_offset, col_offset, grid = get_data()

    print(fill_with_sand(grid, row_offset, col_offset))
    print()

    row_offset, col_offset, grid = get_data()
    print(fill_with_sand_floor(grid, row_offset, col_offset))


if __name__ == "__main__":
    main()
