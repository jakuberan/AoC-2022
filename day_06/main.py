
def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = None
    for x in f:
        out = x.strip()
    return out


def identify_marker(stream, marker_len=4):
    """
    Identifies marker of specified length
    """
    for i in range(marker_len, len(stream)):
        if len(set(stream[(i-marker_len):i])) == marker_len:
            return i


def part1(data_path="input"):
    """
    Return position where marker of length 4 appeared
    """
    data = read_and_process(data_path)
        
    return identify_marker(data)


def part2(data_path="input"):
    """
    Return position where marker of length 14 appeared
    """
    data = read_and_process(data_path)
        
    return identify_marker(data, marker_len=14)


if __name__ == "__main__":

    print(f"Marker of length 4 appeared on position {part1()}")
    print(f"Marker of length 14 appeared on position {part2()}")
