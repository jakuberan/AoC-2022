import numpy as np
from scipy.signal import convolve2d


def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = []
    for x in f:
        out.append([1 if c == "#" else 0 for c in x.strip()])
    return np.array(out)


def print_array(array):
    """
    Helper function for printing out the array
    """
    for r in array:
        print("".join(["#" if c == 1 else "." for c in r]))
    print()


def restrict_map(map_new):
    """
    Remove all trailing and leading zero rows and columns
    """
    while sum(map_new[0, :]) == 0:
        map_new = np.delete(map_new, 0, 0)
    while sum(map_new[-1, :]) == 0:
        map_new = np.delete(map_new, -1, 0)
    while sum(map_new[:, 0]) == 0:
        map_new = np.delete(map_new, 0, 1)
    while sum(map_new[:, -1]) == 0:
        map_new = np.delete(map_new, -1, 1)

    return map_new


def create_kernels():
    """
    Create kernels for convolution
    """
    kernels = dict()
    for i in range(4):
        kernels[i] = np.reshape(
            [
                4 ** ((1 - i) % 4) + 4 ** ((3 - i) % 4),
                4 ** ((1 - i) % 4),
                4 ** ((1 - i) % 4) + 4 ** ((2 - i) % 4),
                4 ** ((3 - i) % 4),
                4 ** 4,
                4 ** ((2 - i) % 4),
                4 ** ((0 - i) % 4) + 4 ** ((3 - i) % 4),
                4 ** ((0 - i) % 4),
                4 ** ((0 - i) % 4) + 4 ** ((2 - i) % 4),
            ],
            (3, 3),
        )
    return kernels


def proposed_moves(map_neigh, d):
    """
    Propose a move for each elf
    Mark in temporary array and build a dictionary of proposals
    """
    # Create outputs
    elves_remain = np.where(map_neigh > 256)
    map_temp = np.zeros(map_neigh.shape)

    # Check where the elf is about to move, mark in array
    elves_next = dict()
    for i in range(len(elves_remain[0])):
        elf = (elves_remain[0][i], elves_remain[1][i])
        elves_next[elf] = elf
        elf_num = map_neigh[elf]
        for t in range(4):
            if elf_num % 4 == 0:
                elf_next = (
                    elf[0] - ((0 - d) % 4 == t) + ((1 - d) % 4 == t),
                    elf[1] - ((2 - d) % 4 == t) + ((3 - d) % 4 == t),
                )
                elves_next[elf] = elf_next
                map_temp[elf_next] += 1
                break
            else:
                elf_num = int((elf_num - (elf_num % 4)) / 4)
    return map_temp, elves_next, elves_remain


def move_to_free(elves_remain, elves_next, map_neigh, map_temp):
    """
    Move elves to new position
    """

    # Create new map, add stable elves
    map_new = np.zeros(map_neigh.shape)
    map_new[np.where(map_neigh == 256)] = 1

    # Move remaining elves
    for i in range(len(elves_remain[0])):
        elf = (elves_remain[0][i], elves_remain[1][i])
        next_pos = elves_next[elf]
        if map_temp[next_pos] == 1:
            map_new[next_pos] = 1
        else:
            map_new[elf] = 1
    return map_new


def solve(data_path="input"):
    """
    Perform moves of the elves
    In each move, first the stable elves are defined
    Then for each remaining elf, their desired location is calculated
    Finally, if this location is empty, the elf moves there
    """

    # Define elves, their preferred step
    elf_map = read_and_process(data_path)

    # Define kernels for different starting directions
    kernels = create_kernels()

    turn = 0
    empty_fields_10 = None
    while True:
        d = turn % 4
        turn += 1

        # Define kernel for the given round and apply it to calculate neighbors
        kernel = kernels[d]
        elf_map_neigh = convolve2d(elf_map, kernel, mode="full")

        # Check where the elf is about to move
        elf_map_temp, elves_next, elves_remain = proposed_moves(elf_map_neigh, d)

        # Move elves to new positions
        elf_map_new = move_to_free(
            elves_remain, elves_next, elf_map_neigh, elf_map_temp
        )

        # Restrict map size - empty rows and columns
        elf_map_new = restrict_map(elf_map_new)

        # If the position is stable, end the simulation
        if np.array_equal(elf_map, elf_map_new):
            return empty_fields_10, turn
        else:
            elf_map = elf_map_new

        # Return if the number of turns was reached
        if turn == 10:
            empty_fields_10 = sum(sum(elf_map == 0))


if __name__ == "__main__":

    part1, part2 = solve()
    print(f"Empty ground tiles of the smallest rectangle: {part1}")
    print(f"Number of the first round where no Elf moves is {part2}")
