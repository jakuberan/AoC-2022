from string import ascii_lowercase as low, ascii_uppercase as up


def read_and_process(data_path: str) -> list:
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = []
    for x in f:
        out.append(x.strip())
    return out


def get_compartments(rucksack: list) -> list:
    """
    Split rucksack to compartments
    """
    n_items = len(rucksack)
    return [rucksack[: int(n_items / 2)], rucksack[int(n_items / 2) :]]


def get_score(char: chr) -> int:
    """
    Calculate score of a single item
    """
    return low.find(char) + up.find(char) + 2 + 26 * (up.find(char) >= 0)


def part1(data_path="input") -> int:
    """
    Identify misplaced item and calculate score
    """
    data = read_and_process(data_path)
    out = 0
    for d in data:
        d_comp = get_compartments(d)
        misplaced = (set(d_comp[0]).intersection(set(d_comp[1]))).pop()
        out += get_score(misplaced)

    return out


def get_badge(group: list) -> str:
    """
    Calculates the common element in the whole group
    """
    gr12 = set(group[0]).intersection(set(group[1]))
    badge = (gr12.intersection(set(group[2]))).pop()
    return badge


def part2(data_path="input"):
    """
    Identify groups of three and calculate score
    """
    data = read_and_process(data_path)
    out = 0
    group = []
    for d in data:
        group.append(d)
        if len(group) == 3:
            out += get_score(get_badge(group))
            group = []

    return out


if __name__ == "__main__":

    print(f"Sum of scores of misplaced items is {part1()}")
    print(f"Sum of scores of group badges is: {part2()}")
