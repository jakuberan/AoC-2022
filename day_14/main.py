import numpy as np


def read_and_process(data_path: str):
    """
    Process and prepare input data
    """
    f = open(data_path, "r")
    out = []
    for x in f:
        out.append([c.split(",") for c in x.strip().split(" -> ")])
    return out


def build_walls(walls, w):
    """
    Add new walls to list of walls
    """
    for i in range(len(w) - 1):
        x_max = max(int(w[i][0]), int(w[i + 1][0]))
        x_min = min(int(w[i][0]), int(w[i + 1][0]))
        y_max = max(int(w[i][1]), int(w[i + 1][1]))
        y_min = min(int(w[i][1]), int(w[i + 1][1]))

        # For each horizontal position add a set of vertical ones
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                if x in walls:
                    walls[x].add(y)
                else:
                    walls[x] = {y}
    return walls


def sand_add(ws, sand):
    """
    Place the sand into the list of walls
    """
    num_above = np.sum(ws < sand)
    return np.insert(ws, num_above, sand)


def sand_move(walls: dict, floor=0, pos_x=500, pos_y=0):
    """
    Flow sand into the abyss
    """
    while True:
        if pos_y + 1 in walls[pos_x]:
            if pos_x - 1 in walls:
                if pos_y + 1 in walls[pos_x - 1]:
                    if pos_x + 1 in walls:
                        if pos_y + 1 in walls[pos_x + 1]:
                            # Sand unit was blocked
                            walls[pos_x] = sand_add(walls[pos_x], pos_y)
                            return walls, ((pos_y > 0) or (pos_x != 500))
                        else:
                            # Sand unit flows diagonally right
                            pos_x += 1
                            pos_y += 1
                    else:
                        if floor > 0:
                            walls[pos_x + 1] = np.array([floor - 1, floor])
                        return walls, (floor > 0)
                else:
                    # Sand unit flows diagonally left
                    pos_x -= 1
                    pos_y += 1
            else:
                # There is a new horizontal position to be handled
                if floor > 0:
                    walls[pos_x - 1] = np.array([floor - 1, floor])
                return walls, (floor > 0)
        else:
            num_above = sum(walls[pos_x] < pos_y)
            # Fall / place the unit of sand into the current horizontal position
            if num_above == len(walls[pos_x]):
                if floor > 0:
                    walls[pos_x] = np.concatenate(
                        (walls[pos_x], np.array([floor - 1, floor]))
                    )
                return walls, (floor > 0)
            else:
                pos_y = walls[pos_x][num_above] - 1


def find_floor(walls: dict) -> int:
    """
    Locate the floor coordinate
    """
    max_y = 0
    for x in walls:
        max_y = max(max_y, np.max(walls[x]))
    return max_y + 2


def solve(data_path="input"):
    """
    Number of units of sand before falling off the map / blocking the source
    """
    data = read_and_process(data_path)

    # Build all walls
    walls = dict()
    for d in data:
        walls = build_walls(walls, d)

    # Convert sets to arrays to better handle queries
    for vertical in walls:
        walls[vertical] = np.array(sorted(list(walls[vertical])))

    # Locate floor y coordinate
    floor_y = find_floor(walls)

    # Flow sand units
    keep_falling = True
    sand_cnt = -1
    sand_cnt_1 = None
    floor = 0
    while keep_falling:
        sand_cnt += 1
        if sand_cnt % 2000 == 0:
            print(sand_cnt)
        walls, keep_falling = sand_move(walls, floor=floor)
        # Save results for part one and restart the loop
        if not keep_falling:
            if sand_cnt_1 is None:
                sand_cnt_1 = sand_cnt
                keep_falling = True
                floor = floor_y

    return sand_cnt_1, sand_cnt


if __name__ == "__main__":

    part1, part2 = solve()
    print(f"The number of stable sand units is {part1} (no-floor setup)")
    print(f"The number of stable sand units is {part2} (floor setup)")
