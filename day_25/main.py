def read_and_process(data_path: str):
    """
    Process and prepare input data
    """
    convert_chars = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}

    f = open(data_path, "r")
    out = []
    for x in f:
        for i, c in enumerate(x.strip()[::-1]):
            if len(out) == i:
                out.append(0)
            out[i] += convert_chars[c]
    return out


def convert_sums_to_snafu(num: list) -> str:
    """
    Convert num with decimal sums to snafu format
    """
    convert_chars_rev = {0: "0", 1: "1", 2: "2", -1: "-", -2: "="}
    out = ""
    num.append(0)
    # Convert to SNAFU range, keep out the auxiliary leading zero
    for i in range(len(num) - 1):
        if int(num[i] / 5) != 0:
            num[i + 1] += int(num[i] / 5)
            num[i] -= int(num[i] / 5) * 5
        if num[i] > 2:
            num[i + 1] += 1
            num[i] = num[i] - 5
        elif num[i] < -2:
            num[i + 1] += -1
            num[i] = num[i] + 5
        out = convert_chars_rev[num[i]] + out

    # Auxiliary first digit - convert in case of non-zero
    if num[len(num) - 1] != 0:
        out = convert_chars_rev[num[len(num) - 1]] + out
    return out


def part1(data_path="input") -> str:
    """
    Takes number in decimal sums format and converts it to SNAFU format
    """
    return convert_sums_to_snafu(read_and_process(data_path))


if __name__ == "__main__":

    print(f"Output in SNAFU format is: {part1()}")
