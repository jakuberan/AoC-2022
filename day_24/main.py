from copy import deepcopy
import numpy as np


def read_and_process(data_path: str):
    """
    Process and prepare input data
    """
    f = open(data_path, "r")
    out = []
    for x in f:
        out.append([c for c in x.strip()[1:-1]])
    return out[1:-1]


def print_map(data, lim=25):
    """
    Helper function for printing out the underlying map
    """
    for r in data[:lim]:
        for c in r[:lim]:
            c0 = c if len(c) == 1 else len(c)
            print(c0, end="")
        print()
    print()


def clean_map(data):
    """
    Template for new map creation
    """
    data_clean = []
    for r in data:
        data_clean.append(["."] * len(r))
    return data_clean


def add_char(data_new, ri, ci, char):
    """
    Add char to desired position
    """
    if ri == len(data_new):
        ri = 0
    if ci == len(data_new[ri]):
        ci = 0
    if data_new[ri][ci] == ".":
        data_new[ri][ci] = char
    else:
        data_new[ri][ci] += char
    return data_new


def move_map(data, data_new):
    """
    Perform single map move
    """
    for row_i in range(len(data)):
        for col_i in range(len(data[row_i])):
            cell = data[row_i][col_i]
            if cell != ".":
                if ">" in cell:
                    data_new = add_char(data_new, row_i, col_i + 1, ">")
                if "<" in cell:
                    data_new = add_char(data_new, row_i, col_i - 1, "<")
                if "^" in cell:
                    data_new = add_char(data_new, row_i - 1, col_i, "^")
                if "v" in cell:
                    data_new = add_char(data_new, row_i + 1, col_i, "v")
    return data_new


def add_map():
    """
    Extend global variable containing maps
    """
    map_bank["last"] += 1
    map_bank[map_bank["last"]] = move_map(
        deepcopy(map_bank[map_bank["last"] - 1]), deepcopy(map_bank["clean"])
    )


def search_path(t, row, col, max_r, max_c, min_time):
    """
    Recursively search for shortest path to lower right corner
    """
    if (row == max_r) and (col == max_c):
        print(f"Found goal in time {t + 1}")
        return t
    if min_time <= t + 1:
        return min_time
    if map_bank["last"] == t:
        add_map()
    if t + 1 not in move_bank:
        move_bank[t + 1] = set()

    # Collect all valid moves from position, perform the move
    # In order left, down, stay, right, up
    moves = []
    for m in [[0, 1], [1, 0], [0, 0], [0, -1], [-1, 0]]:
        r = row + m[0]
        c = col + m[1]
        if (c <= max_c) and (r <= max_r) and (c >= 0) and (r >= 0):
            if map_bank[t + 1][r][c] == ".":
                if (r, c) not in move_bank[t + 1]:
                    moves.append([r, c])
                    move_bank[t + 1].add((r, c))
                    min_time = min(
                        min_time, search_path(t + 1, r, c, max_r, max_c, min_time)
                    )

    return min_time


def find_shortest(data, data_clean):
    """
    Wrapper for path search
    Take into account the shortest path might include waiting in starting point
    for some time
    """
    # Dictionary of all map and position movements
    global move_bank
    global map_bank

    move_bank = dict()
    map_bank = {"clean": data_clean, "last": 0, 0: data}
    time_min = np.inf
    time_cur = 0
    while time_min == np.inf:
        # Search for time when entering the maze is possible
        while map_bank[time_cur][0][0] != ".":
            if time_cur == map_bank["last"]:
                add_map()
            time_cur += 1
        # Search path
        move_bank[time_cur] = {(0, 0)}
        time_min = search_path(
            time_cur, 0, 0, len(data) - 1, len(data[0]) - 1, time_min
        )
        time_cur += 1

    # Add one map adn return best time with lat map
    add_map()
    return time_min + 1, map_bank[time_min + 1]


def rmap(data):
    """
    Reverse the order of the map
    """
    rev_map = {".": ".", ">": "<", "<": ">", "v": "^", "^": "v"}
    out = []
    for row in data[::-1]:
        out_tmp = []
        for cell in row[::-1]:
            out_tmp.append("".join([rev_map[char] for char in cell]))
        out.append(out_tmp)
    return out


def solve(data_path="input"):
    """
    Search for shortest path in a maze
    """
    data = read_and_process(data_path)
    data_clean = clean_map(data)

    # Search for the shortest path from start to end
    time_min_1, last_map = find_shortest(deepcopy(data), deepcopy(data_clean))

    # Search for the shortest path from end to start
    time_min_2, last_map = find_shortest(rmap(deepcopy(last_map)), deepcopy(data_clean))

    # Search for the shortest path from start to end
    time_min_3, _ = find_shortest(rmap(deepcopy(last_map)), deepcopy(data_clean))

    return time_min_1, time_min_1 + time_min_2 + time_min_3


if __name__ == "__main__":
    # Dictionary of all map and position movements
    global move_bank
    global map_bank

    part1, part2 = solve()
    print(f"\nMin minutes to reach the goal is {part1}")
    print(f"Min minutes to reach the goal go back and then to goal is {part2}")
