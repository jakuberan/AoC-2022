def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    for x in f:
        return [True if c == ">" else False for c in x.strip()]


def extend_field(field: list, width: int, rows_to_add=10000) -> list:
    """
    Extend the field (from the end) by specified number of rows
    """
    for i in range(rows_to_add):
        field.append([True] + [False] * width + [True])
    return field


def mark_in_field(rock: list, field: list) -> list:
    """
    Mark the stable rock in the field
    """
    for i in range(len(rock[0])):
        field[rock[0][i]][rock[1][i]] = True
    return field


def move_down(rock: list, field: list):
    """
    Identify if a given rock can move down
        If yes - move the rock
        If no  - mark the field by the rock
    """
    for i in range(len(rock[0])):
        if field[rock[0][i] - 1][rock[1][i]]:
            return False, rock, mark_in_field(rock, field)
    return True, [[r - 1 for r in rock[0]], rock[1]], field


def move_lr(rock: list, field: list, direct: bool) -> list:
    """
    Identify if a given rock can move right / left, if so, move it
    """
    for i in range(len(rock[0])):
        if field[rock[0][i]][rock[1][i] + (2 * direct - 1)]:
            return rock
    return [rock[0], [r + (2 * direct - 1) for r in rock[1]]]


def rock_bank() -> dict:
    """
    Generate objects - pair of list as deviations from [0, 0] coordinate
    """
    return {
        "-": [[0, 0, 0, 0], [3, 4, 5, 6]],
        "+": [[0, 1, 1, 1, 2], [4, 3, 4, 5, 4]],
        "J": [[0, 0, 0, 1, 2], [3, 4, 5, 5, 5]],
        "|": [[0, 1, 2, 3], [3, 3, 3, 3]],
        "O": [[0, 0, 1, 1], [3, 4, 3, 4]],
    }


def print_field(field: list, top: int, bottom=0):
    """
    Print few top lines of the field
    """
    for i in range(top, bottom - 1, -1):
        print("".join(["#" if f else "." for f in field[i]]))
    print()


def part1(data_path="input", width=7):
    """
    Calculate tower height after pre-specified number of rocks fall
    """
    to_right = read_and_process(data_path)
    top_pos = 0
    step = 0
    field = extend_field([[True] * (width + 2)], width)

    # Iterate over rocks
    for i in range(int(2022 / 5) + 1):
        rocks = rock_bank()
        for rock_name in rocks:
            rock = rocks[rock_name]
            can_move = True
            rock[0] = [r + top_pos + 4 for r in rock[0]]
            while can_move:
                # Left / right move then down move, update position if rest
                rock = move_lr(rock, field, to_right[step % len(to_right)])
                step += 1
                can_move, rock, field = move_down(rock, field)
            top_pos = max(top_pos, max(rock[0]))

            # Stopping condition
            if (i == int(2022 / 5)) and (rock_name == "+"):
                return top_pos


if __name__ == "__main__":

    print(f"After 2022 rocks, the tower height will be {part1()}")
