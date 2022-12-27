from string import ascii_lowercase as letters
import numpy as np


def read_and_process(data_path: str):
    """
    Process and prepare input data, search for start
    """

    f = open(data_path, "r")
    out = []
    i = 0
    end = None
    start = None
    for x in f:
        line = x.strip()
        if line.find("S") >= 0:
            start = [i, line.find("S")]
        if line.find("E") >= 0:
            end = [i, line.find("E")]
        i += 1
        out.append([c for c in line])
    return out, start, end


def print_maze(maze):
    """
    Maze printing function
    """
    for i in range(len(maze)):
        print("".join([("  " + str(c))[-3:] for c in maze[i]]))


def search_path(
    maze: list, maze_len: list, len_prev: int, lowest_possible: int, row: int, col: int
) -> list:
    """
    Searches for shortest path from given point
    """

    # Outside of maze
    if (row < 0) or (row >= len(maze)):
        return maze_len
    if (col < 0) or (col >= len(maze[row])):
        return maze_len

    # Height is ok
    height = letters.find(maze[row][col])
    if height < lowest_possible:
        return maze_len

    # Is this the shortest path
    if maze_len[row][col] <= len_prev:
        return maze_len
    else:
        maze_len[row][col] = len_prev

    # Move in all possible directions
    maze_len = search_path(maze, maze_len, len_prev + 1, height - 1, row + 1, col)
    maze_len = search_path(maze, maze_len, len_prev + 1, height - 1, row - 1, col)
    maze_len = search_path(maze, maze_len, len_prev + 1, height - 1, row, col + 1)
    maze_len = search_path(maze, maze_len, len_prev + 1, height - 1, row, col - 1)
    return maze_len


def solve(data_path="input"):
    """
    Shortest path from end to all points
    """
    maze, start, end = read_and_process(data_path)

    # Create maze of the shortest paths
    maze_len = []
    for i in range(len(maze)):
        maze_len.append([np.inf] * len(maze[i]))

    # Modify start and end heights
    maze[start[0]][start[1]] = "a"
    maze[end[0]][end[1]] = "z"

    # Search for shortest path from end
    maze_len = search_path(maze, maze_len, 0, 24, end[0], end[1])

    # Find the lowest point with the shortest path
    min_so_far = np.inf
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == "a":
                min_so_far = min(min_so_far, maze_len[r][c])

    return maze_len[start[0]][start[1]], min_so_far


if __name__ == "__main__":

    p1, p2 = solve()
    print(f"Shortest path from start to goal is {p1}")
    print(f"Shortest path from any lowest point to goal is {p2}")
