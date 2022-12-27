import numpy as np


def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = []
    for x in f:
        out.append([int(c) for c in x.strip()])
    return out


def part1(data_path="input"):
    """
    Calculate number of visible trees from boundaries
    """
    data = read_and_process(data_path)

    # Arrays of visible trees
    up = np.array(data)
    down = np.array(data)
    left = np.array(data)
    right = np.array(data)
    r = len(data)
    c = len(data[0])

    # Keep visible from down and up on the boundary
    for i in range(1, r):
        up[i, :] = np.multiply(up[i, :], up[i, :] > up[0, :])
        up[0, :] = np.maximum(up[i, :], up[0, :])
        down[r - 1 - i, :] = np.multiply(
            down[r - 1 - i, :], down[r - 1 - i, :] > down[r - 1, :]
        )
        down[r - 1, :] = np.maximum(down[r - 1 - i, :], down[r - 1, :])

    # Keep visible from left and right on the boundary
    for i in range(1, c):
        left[:, i] = np.multiply(left[:, i], left[:, i] > left[:, 0])
        left[:, 0] = np.maximum(left[:, i], left[:, 0])
        right[:, c - 1 - i] = np.multiply(
            right[:, c - 1 - i], right[:, c - 1 - i] > right[:, c - 1]
        )
        right[:, c - 1] = np.maximum(right[:, c - 1 - i], right[:, c - 1])

    return np.sum(np.sum(up + down + left + right > 0))


def part2(data_path="input"):
    """
    Find the best scenic score
    """
    data = read_and_process(data_path)

    scenic = np.zeros(shape=(len(data), len(data[0])))
    rows = len(data)
    cols = len(data[0])

    # Check every tree in the grid
    for r in range(rows):
        for c in range(cols):

            # Init counter for visible trees and condition to check direction
            visible_cnt = {"up": 0, "down": 0, "left": 0, "right": 0}
            check_dir = {
                "up": r > 0,
                "down": r < rows - 1,
                "left": c > 0,
                "right": c < cols - 1,
            }
            i = 0

            # Iterate all directions until needed
            while sum(check_dir.values()) > 0:
                i += 1
                if check_dir["up"]:
                    visible_cnt["up"] += 1
                    if (data[r - i][c] >= data[r][c]) or (r - i == 0):
                        check_dir["up"] = False
                if check_dir["down"]:
                    visible_cnt["down"] += 1
                    if (data[r + i][c] >= data[r][c]) or (r + i == rows - 1):
                        check_dir["down"] = False
                if check_dir["left"]:
                    visible_cnt["left"] += 1
                    if (data[r][c - i] >= data[r][c]) or (c - i == 0):
                        check_dir["left"] = False
                if check_dir["right"]:
                    visible_cnt["right"] += 1
                    if (data[r][c + i] >= data[r][c]) or (c + i == cols - 1):
                        check_dir["right"] = False

            scenic[r, c] = np.prod(np.array(list(visible_cnt.values())))

    return int(np.max(np.max(scenic)))


if __name__ == "__main__":

    print(f"Number of visible trees from boundaries is {part1()}")
    print(f"Highest possible scenic score is {part2()}")
