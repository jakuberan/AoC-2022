def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = []
    out_temp = 0
    for x in f:
        if len(x.strip()) > 0:
            out_temp += int(x.strip())
        else:
            out.append(out_temp)
            out_temp = 0
    return out


def part1(data_path="input"):
    """
    Get max calories from the list of all calories
    """
    calories = read_and_process(data_path)

    return max(calories)


def part2(data_path="input"):
    """
    Get sum of three largest calories from the list of all calories
    """
    calories = read_and_process(data_path)
    calories.sort(reverse=True)

    return sum(calories[:3])


if __name__ == "__main__":

    print(f"Max calories: {part1()}")
    print(f"Sum of three largest calories: {part2()}")
