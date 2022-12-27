def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = []
    for x in f:
        a = [c.split("-") for c in x.strip().split(",")]
        out.append([int(c) for c in (a[0] + a[1])])
    return out


def overlap_full(pair: list) -> bool:
    """
    Identifies full overlap
    """
    if (pair[0] == pair[2]) or (pair[1] == pair[3]):
        return True
    elif pair[0] > pair[2]:
        if pair[1] < pair[3]:
            return True
    else:
        if pair[1] > pair[3]:
            return True
    return False


def overlap_partial(pair: list) -> bool:
    """
    Identifies full overlap
    """
    if (pair[1] < pair[2]) or (pair[0] > pair[3]):
        return False
    else:
        return True


def part1(data_path="input"):
    """
    Count full overlap
    """
    data = read_and_process(data_path)
    overlap_full_cnt = 0

    # Count overlaps
    for d in data:
        overlap_full_cnt += overlap_full(d)

    return overlap_full_cnt


def part2(data_path="input"):
    """
    Count full overlap
    """
    data = read_and_process(data_path)
    overlap_partial_cnt = 0

    # Count overlaps
    for d in data:
        overlap_partial_cnt += overlap_partial(d)

    return overlap_partial_cnt


if __name__ == "__main__":

    print(f"Number of full overlaps is {part1()}")
    print(f"Number of partial overlaps is {part2()}")
