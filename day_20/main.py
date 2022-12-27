def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = []
    for x in f:
        out.append(int(x.strip()))
    return out


def solve(data_path="input", dkey=1, rounds=1):
    """
    Shuffling list of numbers
    """
    data = read_and_process(data_path)

    # Create the pair of position and value
    pairs = [[i, d] for i, d in enumerate(data)]

    # Mixing for all pairs in sequence given by first element
    length = len(data)
    for _ in range(rounds):
        for i_rel in range(len(pairs)):
            for i_abs in range(len(pairs)):
                if pairs[i_abs][0] == i_rel:
                    pair = pairs.pop(i_abs)
                    i_new = (i_abs + pair[1] * dkey) % (length - 1)
                    pairs.insert(i_new, pair)
                    break

    # Search for element 0
    i_abs = None
    for i_abs in range(len(pairs)):
        if pairs[i_abs][1] == 0:
            break

    # Find groove numbers
    out = 0
    for groove in [1000, 2000, 3000]:
        out += pairs[(i_abs + groove) % length][1] * dkey

    return out


if __name__ == "__main__":

    print(f"Grove coordinates sum is {solve()}")
    print(f"Grove coordinates sum is {solve(dkey=811589153, rounds=10)}")
