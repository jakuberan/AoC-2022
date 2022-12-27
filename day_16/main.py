import numpy as np


def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = dict()
    for x in f:
        line = x.strip().split()
        out[line[1]] = [int(line[4][5:-1]), (" ".join(line[9:])).split(", ")]
    return out


def get_distance_matrix(valvinfo, valves):
    """
    Creates distance matrix from valves graph using floyd
    """
    # Initialize distance matrix
    dist = np.full((len(valves), len(valves)), np.inf)
    for i, valve in enumerate(valves):
        for neigh in valvinfo[valve][1]:
            dist[i, valves.index(neigh)] = 1

    # Fill distance matrix
    for k in range(len(valves)):
        for i in range(len(valves)):
            for j in range(len(valves)):
                if dist[i, j] > dist[i, k] + dist[k, j]:
                    dist[i, j] = dist[i, k] + dist[k, j]

    # Remove diagonal
    for i in range(len(valves)):
        dist[i, i] = 0

    return dist


def max_output(valvinfo, valves, dists, so_far, time, flow, flow_best, max_time=30):
    """
    Finds recursively the optimal path to start the valves
    """
    node = so_far[-1]
    node_i = valves.index(node)
    for neigh in valves:
        if neigh not in so_far:
            dist_cur = dists[node_i, valves.index(neigh)]
            # Open valve only in case the time was not exceeded
            if 1 + dist_cur + time <= max_time:
                fcur = (max_time - 1 - dist_cur - time) * valvinfo[neigh][0]
                flow_future = max_output(
                    valvinfo,
                    valves,
                    dists,
                    so_far + [neigh],
                    time + 1 + dist_cur,
                    flow + fcur,
                    flow_best,
                )
                flow_best = max(flow_best, flow_future, flow + fcur)
    return flow_best


def part1(data_path="input", max_time=30, start="AA"):
    """
    Highest possible pressure to be released in case of a signle worker
    """
    valvinfo = read_and_process(data_path)
    valves = list(valvinfo.keys())

    # Create distance matrix
    dist = get_distance_matrix(valvinfo, valves)
    dstart = dist[valves.index(start)]

    # Remove valves of zero flow from distance matrix
    for i in range(len(valves) - 1, -1, -1):
        if valvinfo[valves[i]][0] == 0:
            valves.pop(i)
            dist = np.delete(np.delete(dist, i, 0), i, 1)

    # Find the best path from start
    fbest = 0
    for i, neigh in enumerate(valvinfo.keys()):
        if neigh in valves:
            tcur = dstart[i] + 1
            fcur = valvinfo[neigh][0] * (max_time - tcur)
            fbest = max(
                fbest, max_output(valvinfo, valves, dist, [neigh], tcur, fcur, fcur)
            )
    return int(fbest)


def max_output_2p(
    valvinfo, valves, dists, so_far, time, prev, flow, flow_best, max_time=26
):
    """
    Finds recursively the optimal path to start the valves when two workers
    """
    # Find index of lower time
    idx = 0 if time[0] < time[1] else 1
    time_temp = time[idx]
    node_temp = prev[idx]
    node_i = valves.index(node_temp)
    for neigh in valves:
        if neigh not in so_far:
            time[idx] = time_temp + 1 + dists[node_i, valves.index(neigh)]
            # Open valve only in case the time was not exceeded
            if time[idx] <= max_time:
                fcur = (max_time - time[idx]) * valvinfo[neigh][0]
                prev[idx] = neigh
                flow_future = max_output_2p(
                    valvinfo,
                    valves,
                    dists,
                    so_far + [neigh],
                    time,
                    prev,
                    flow + fcur,
                    flow_best,
                )
                flow_best = max(flow_best, flow_future, flow + fcur)
    prev[idx] = node_temp
    time[idx] = time_temp
    return flow_best


def part2(data_path="input", max_time=26, start="AA"):
    """
    Highest possible pressure to be released in case of two workers
    """
    valvinfo = read_and_process(data_path)
    valves = list(valvinfo.keys())

    # Create distance matrix
    dist = get_distance_matrix(valvinfo, valves)
    dstart = dist[valves.index(start)]

    # Remove valves of zero flow from distance matrix
    for i in range(len(valves) - 1, -1, -1):
        if valvinfo[valves[i]][0] == 0:
            valves.pop(i)
            dist = np.delete(np.delete(dist, i, 0), i, 1)

    # Find the best path from start
    fbest = 0
    for i1 in range(len(valvinfo)):
        neigh1 = list(valvinfo.keys())[i1]
        if neigh1 in valves:
            tcur1 = dstart[i1] + 1
            print(f"{neigh1} for elephant explored. Best value so-far {fbest}")
            for i2 in range(len(valvinfo)):
                neigh2 = list(valvinfo.keys())[i2]
                if (neigh2 in valves) and (i1 > i2):
                    tcur2 = dstart[i2] + 1
                    fcur = valvinfo[neigh1][0] * (max_time - tcur1)
                    fcur += valvinfo[neigh2][0] * (max_time - tcur2)
                    fbest = max(
                        fbest,
                        max_output_2p(
                            valvinfo,
                            valves,
                            dist,
                            [neigh1, neigh2],
                            [tcur1, tcur2],
                            [neigh1, neigh2],
                            fcur,
                            fcur,
                        ),
                    )
    return int(fbest)


if __name__ == "__main__":

    print(f"Most pressure to be released alone is {part1()}")
    print(f"Most pressure to be released with elephant is {part2()}")
