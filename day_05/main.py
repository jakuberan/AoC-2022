from string import ascii_uppercase as letters


def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    stack = [[] for _ in range(9)]
    moves = []
    fill_stack = True
    for x in f:
        if len(x.strip()) == 0:
            fill_stack = False
        if fill_stack:
            i = 0
            while len(x) > (i * 4) + 1:
                pos = (i * 4) + 1
                if x[pos] in letters:
                    stack[i].append(x[pos])
                i += 1
        elif len(x.strip()) > 0:
            m = x.strip().split()
            moves.append([int(m[1]), int(m[3]), int(m[5])])

    # Clean up stack
    for i in range(len(stack) - 1, 0, -1):
        if len(stack[i]) == 0:
            stack.pop(i)
    return stack, moves


def move_crate9001(stack: list, move: list) -> list:
    """
    Performs one single move of crane 9001
    """
    to_move = stack[move[1] - 1][: move[0]]
    stack[move[2] - 1] = to_move + stack[move[2] - 1]
    stack[move[1] - 1] = stack[move[1] - 1][move[0] :]
    return stack


def move_crate9000(stack: list, move: list) -> list:
    """
    Performs one single move of crane 9000
    """
    for _ in range(move[0]):
        stack[move[2] - 1].insert(0, stack[move[1] - 1].pop(0))
    return stack


def part1(data_path="input"):
    """
    Crate move by crane 9000
    """
    stack, moves = read_and_process(data_path)

    for m in moves:
        stack = move_crate9000(stack, m)

    return "".join([s[0] for s in stack])


def part2(data_path="input"):
    """
    Crate move by crane 9001
    """
    stack, moves = read_and_process(data_path)

    for m in moves:
        stack = move_crate9001(stack, m)

    return "".join([s[0] for s in stack])


if __name__ == "__main__":

    print(f"Solution part 1: {part1()}")
    print(f"Solution part 2: {part2()}")
