# Try to get to starting point from destination point, going only to non-previously visited squares
# This is a bit like Dijkstra

from collections import deque
from functools import reduce


class Point:
    def __init__(self, height):
        self.height = height

        self.left = None
        self.right = None
        self.up = None
        self.down = None

        self.distance_from_end = float("inf")

    def __repr__(self):
        char = chr(self.height + 97)
        return f"{char}"


def get_grid():
    grid = []
    with open("data") as data:
        for line in data:
            row = []
            for char in line.strip():
                if char == "S":
                    start = Point(ord("a") - 97)
                    row.append(start)
                elif char == "E":
                    end = Point(ord("z") - 97)
                    end.distance_from_end = 0
                    row.append(end)
                else:
                    row.append(Point(ord(char) - 97))

            grid.append(row)

    # Calculate neighbours
    row_count = len(grid)
    col_count = len(grid[0])
    for row_index, row in enumerate(grid):
        for col_index, point in enumerate(row):
            if row_index > 0:
                point.up = grid[row_index - 1][col_index]
            if row_index + 1 < row_count:
                point.down = grid[row_index + 1][col_index]

            if col_index > 0:
                point.left = grid[row_index][col_index - 1]
            if col_index + 1 < col_count:
                point.right = grid[row_index][col_index + 1]

    return start, end, grid


def print_grid(grid, param=None):
    for row in grid:
        if not param:
            print("".join(map(str, row)))
        else:
            print("".join(map(lambda x: "|" + str(getattr(x, param)), row)))


def calculate_distances(grid, end):
    # Calculate distances from end until you get to start
    # Not necessarily the first solution is the best solution
    # So keep running until we run out of nodes
    to_visit = deque()
    to_visit.append(end)
    while to_visit:
        current = deque.pop(to_visit)

        for p in (current.left, current.right, current.up, current.down):
            if p is not None:
                # We can only go one up, but multiple down
                if current.height - p.height < 2 or p.height > current.height:
                    temp = p.distance_from_end
                    p.distance_from_end = min(
                        p.distance_from_end, current.distance_from_end + 1
                    )
                    if temp != p.distance_from_end:
                        # Only visit nodes that were changed
                        to_visit.append(p)


def main():
    start, end, grid = get_grid()
    calculate_distances(grid, end)

    # print_grid(grid, "distance_from_end")

    print(start.distance_from_end)
    print()

    print(
        min(
            map(
                lambda x: x.distance_from_end,
                filter(lambda x: x.height == 0, reduce(lambda x, y: x + y, grid, [])),
            )
        )
    )


if __name__ == "__main__":
    main()
