def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")

    # Read map and instructions
    out_instr = []
    out_map = []
    read_map = True
    c_temp = None
    for x in f:
        if len(x.strip()) == 0:
            read_map = False
        elif read_map:
            out_map.append([c for c in x[:-1]])
        else:
            c_temp = ""
            for c in x.strip():
                if (c == "R") or (c == "L"):
                    out_instr.append(int(c_temp))
                    out_instr.append(c)
                    c_temp = ""
                else:
                    c_temp += c
    if c_temp != " ":
        out_instr.append(int(c_temp))

    return out_map, out_instr


def move_pos(mmap, row, col, drc, move):
    """
    Determines the position and direction after move is performed
    """
    for i in range(move):
        c_temp = col
        r_temp = row
        # Move right
        if drc == 0:
            c_temp = col + 1
            if len(mmap[r_temp]) == c_temp:
                c_temp = 0
            while mmap[r_temp][c_temp] == " ":
                c_temp += 1
        # Move left
        elif drc == 2:
            c_temp = col - 1
            if c_temp < 0:
                c_temp = len(mmap[r_temp]) - 1
            while mmap[r_temp][c_temp] == " ":
                c_temp -= 1
        # Move down
        elif drc == 1:
            r_temp = row + 1
            if len(mmap) == r_temp:
                r_temp = 0
            while (len(mmap[r_temp]) <= c_temp) or (mmap[r_temp][c_temp] == " "):
                if len(mmap) == r_temp + 1:
                    r_temp = 0
                else:
                    r_temp += 1
        # Move up
        elif drc == 3:
            r_temp = row - 1
            if r_temp < 0:
                r_temp = len(mmap) - 1
            while (len(mmap[r_temp]) <= c_temp) or (mmap[r_temp][c_temp] == " "):
                if r_temp == 0:
                    r_temp = len(mmap) - 1
                else:
                    r_temp -= 1
        else:
            print("Direction not recognized")
        # Check the existing position
        if mmap[r_temp][c_temp] == "#":
            return row, col
        else:
            row = r_temp
            col = c_temp
    return row, col


def part1(data_path="input"):
    """
    Calculate the password on plane
    """
    mmap, moves = read_and_process(data_path)

    # Get start
    drc = 0
    r_pos = 0
    c_pos = None
    for i in range(len(mmap[r_pos])):
        if mmap[r_pos][i] == ".":
            c_pos = i
            break

    # Move in map
    for move in moves:
        if move == "R":
            drc = (drc + 1) % 4
        elif move == "L":
            drc = (drc - 1) % 4
        else:
            r_pos, c_pos = move_pos(mmap, r_pos, c_pos, drc, move)

    return 1000 * (r_pos + 1) + 4 * (c_pos + 1) + drc


def move_pos_cube(mmap, row, col, drc, move, dim=50):
    """
    Determines the position and direction after move in cube is performed
    """
    for i in range(move):
        c_temp = col
        r_temp = row
        drc_temp = drc
        # Move right
        if drc == 0:
            c_temp = col + 1
            if (len(mmap[r_temp]) == c_temp) or (mmap[r_temp][c_temp] == " "):
                if r_temp < dim:
                    c_temp = 2 * dim - 1
                    r_temp = 3 * dim - 1 - r_temp
                    drc_temp = 2
                elif r_temp < 2 * dim:
                    c_temp = r_temp + dim
                    r_temp = dim - 1
                    drc_temp = 3
                elif r_temp < 3 * dim:
                    c_temp = 3 * dim - 1
                    r_temp = 3 * dim - 1 - r_temp
                    drc_temp = 2
                else:
                    c_temp = r_temp - (2 * dim)
                    r_temp = 3 * dim - 1
                    drc_temp = 3
        # Move left
        elif drc == 2:
            c_temp = col - 1
            if (c_temp < 0) or (mmap[r_temp][c_temp] == " "):
                if r_temp < dim:
                    c_temp = 0
                    r_temp = 3 * dim - 1 - r_temp
                    drc_temp = 0
                elif r_temp < 2 * dim:
                    c_temp = r_temp - dim
                    r_temp = 2 * dim
                    drc_temp = 1
                elif r_temp < 3 * dim:
                    c_temp = dim
                    r_temp = 3 * dim - 1 - r_temp
                    drc_temp = 0
                else:
                    c_temp = r_temp - (2 * dim)
                    r_temp = 0
                    drc_temp = 1
        # Move down
        elif drc == 1:
            r_temp = row + 1
            if (
                (len(mmap) == r_temp)
                or (len(mmap[r_temp]) <= c_temp)
                or (mmap[r_temp][c_temp] == " ")
            ):
                if c_temp < dim:
                    c_temp = c_temp + (2 * dim)
                    r_temp = 0
                    drc_temp = 1
                elif c_temp < 2 * dim:
                    r_temp = c_temp + (2 * dim)
                    c_temp = dim - 1
                    drc_temp = 2
                else:
                    r_temp = c_temp - dim
                    c_temp = 2 * dim - 1
                    drc_temp = 2
        # Move up
        elif drc == 3:
            r_temp = row - 1
            if (
                (r_temp < 0)
                or (len(mmap[r_temp]) <= c_temp)
                or (mmap[r_temp][c_temp] == " ")
            ):
                if col < dim:
                    r_temp = c_temp + dim
                    c_temp = dim
                    drc_temp = 0
                elif col < 2 * dim:
                    r_temp = c_temp + (2 * dim)
                    c_temp = 0
                    drc_temp = 0
                else:
                    c_temp = c_temp - (2 * dim)
                    r_temp = 4 * dim - 1
                    drc_temp = 3
        else:
            print("Direction not recognized")
        if mmap[r_temp][c_temp] == "#":
            return row, col, drc
        else:
            col = c_temp
            row = r_temp
            drc = drc_temp
    return row, col, drc


def part2(data_path="input"):
    """
    Calculate the password on cube
    """
    mmap, moves = read_and_process(data_path)

    # Get start
    drc = 0
    r_pos = 0
    c_pos = None
    for i in range(len(mmap[r_pos])):
        if mmap[r_pos][i] == ".":
            c_pos = i
            break

    # Move in map
    for move in moves:
        if move == "R":
            drc = (drc + 1) % 4
        elif move == "L":
            drc = (drc - 1) % 4
        else:
            r_pos, c_pos, drc = move_pos_cube(mmap, r_pos, c_pos, drc, move)

    return 1000 * (r_pos + 1) + 4 * (c_pos + 1) + drc


if __name__ == "__main__":

    print(f"Final password on plane is {part1()}")
    print(f"Final password on cube is {part2()}")
