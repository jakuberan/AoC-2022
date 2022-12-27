def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = []
    for x in f:
        out.append([c for c in x.strip().split()])
    return out


def assign_score(sel):
    """
    Assign score to the selected round
    """
    selection_map = {"X": 1, "Y": 2, "Z": 3}
    win_map_rev = {"X": "C", "Y": "A", "Z": "B"}
    draw_map_rev = {"X": "A", "Y": "B", "Z": "C"}
    if win_map_rev[sel[1]] == sel[0]:
        return selection_map[sel[1]] + 6
    elif draw_map_rev[sel[1]] == sel[0]:
        return selection_map[sel[1]] + 3
    else:
        return selection_map[sel[1]]


def choose_turn(sel):
    """
    Choose turn according to opponents turn
    """
    win_map = {"C": "X", "A": "Y", "B": "Z"}
    draw_map = {"A": "X", "B": "Y", "C": "Z"}
    lose_map = {"C": "Y", "A": "Z", "B": "X"}
    outcomes = {"X": lose_map, "Y": draw_map, "Z": win_map}

    return outcomes[sel[1]][sel[0]]


def part1(data_path="input"):
    """
    Calculates sum of scores for played games
    """
    data = read_and_process(data_path)
    out = 0
    for d in data:
        out += assign_score(d)

    return out


def part2(data_path="input"):
    """
    Calculates sum of scores for tweaked games
    """
    data = read_and_process(data_path)
    out = 0
    for d in data:
        out += assign_score([d[0], choose_turn(d)])

    return out


if __name__ == "__main__":

    print(f"Sum of scores is {part1()}")
    print(f"Solution part 2: {part2()}")
