def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    sensors = []
    beacons = []
    for x in f:
        in_line = x.strip().split()
        sensors.append([int(in_line[2][2:-1]), int(in_line[3][2:-1])])
        beacons.append([int(in_line[8][2:-1]), int(in_line[9][2:])])
    return sensors, beacons


def get_distance(sens: list, bea: list) -> int:
    """
    2D Manhattan distance between two points
    """
    return abs(sens[0] - bea[0]) + abs(sens[1] - bea[1])


def add_segment(sens: list, dist: int, line: list, y_crd: int) -> list:
    """
    Add specified line segments where beacon cannot be
    """
    y_dist = abs(sens[1] - y_crd)
    if y_dist <= dist:
        line.append([sens[0] - (dist - y_dist), sens[0] + (dist - y_dist)])
    return line


def segment_length(segments: list) -> int:
    """
    Calculate length of all segments on the line
    """
    total_len = 0
    x_low = segments[0][0]
    x_high = segments[0][1]
    for seg in segments[1:]:
        # Overlap with upper line segment
        if x_high >= seg[0]:
            x_high = max(x_high, seg[1])
        else:
            total_len += x_high - x_low + 1
            x_low = seg[0]
            x_high = seg[1]
    return total_len + (x_high - x_low + 1)


def part1(data_path="input", y_coord=2000000):
    """
    Count the selected row positions which cannot contain a beacon
    """
    sensors, beacons = read_and_process(data_path)
    segments = []

    # Mark line segments where a beacon cannot be
    for i in range(len(sensors)):
        distance = get_distance(sensors[i], beacons[i])
        segments = add_segment(sensors[i], distance, segments, y_coord)

    # Combined segments length
    segments_len = segment_length(sorted(segments))

    # Count beacons on specified y coordinate
    beacon_on_y = set()
    for bc in beacons:
        if bc[1] == y_coord:
            beacon_on_y.add(bc[0])

    return segments_len - len(beacon_on_y)


def get_edges(sens: list, dist: int) -> list:
    """
    Calculate edges of the rhombus, where a beacon cannot be
    """
    up = [sens[0], sens[1] - dist - 1]
    down = [sens[0], sens[1] + dist + 1]
    left = [sens[0] - dist - 1, sens[1]]
    right = [sens[0] + dist + 1, sens[1]]

    return [up, right, left, down]


def do_overlap(ed1: list, ed2: list, drc: int):
    """
    Calculate if two line segments do overlap
    """
    if ed1[0][1] < ed2[3][1]:
        if drc == 1:
            if ed1[1][1] > ed2[2][1]:
                return True
        else:
            if ed1[2][1] > ed2[1][1]:
                return True
    return False


def get_overlap(ed1: list, ed2: list, drc: int) -> list:
    """
    Get overlap of two line segments
    """
    if (ed1[0][0] - drc * ed1[0][1]) == (ed2[3][0] - drc * ed2[3][1]):
        if do_overlap(ed1, ed2, drc):
            # Backward line direction
            if drc == 1:
                up = ed1[0] if (ed1[0][1] > ed2[2][1]) else ed2[2]
                down = ed1[1] if (ed1[1][1] < ed2[3][1]) else ed2[3]
                if (down[1] >= up[1]) and (down[0] >= up[0]):
                    return [up, down]
            # Forward line direction
            else:
                up = ed1[0] if (ed1[0][1] > ed2[1][1]) else ed2[1]
                down = ed1[2] if (ed1[2][1] < ed2[3][1]) else ed2[3]
                if (down[1] >= up[1]) and (down[0] <= up[0]):
                    return [up, down]
    return []


def get_intersection(lb: list, lf: list, lim: int) -> list:
    """
    Intersection between two lines - one forward and one backward
    """

    # Calculate intersection of prolonged lines
    f_sum = lf[0][0] + lf[0][1]
    b_dif = lb[0][0] - lb[0][1]

    # Check if the intersection is within bounds and included in line segments
    if (f_sum % 2) == (b_dif % 2):
        x = int((f_sum + b_dif) / 2)
        y = int((f_sum - b_dif) / 2)
        if (y >= 0) and (y <= lim) and (x >= 0) and (x <= lim):
            if (y > lf[0][1]) and (y < lf[1][1]):
                if (y > lb[0][1]) and (y < lb[1][1]):
                    if (x < lf[0][0]) and (x > lf[1][0]):
                        if (x > lb[0][0]) and (x < lb[1][0]):
                            return [x, y]
    return []


def part2(data_path="input", lim=4000000):
    """
    Count boundary intersections and find empty beacon position
    """
    sensors, beacons = read_and_process(data_path)

    distances = []
    edges = []
    # Calculate distances and rhombuses edges
    for i in range(len(sensors)):
        distances.append(get_distance(sensors[i], beacons[i]))
        edges.append(get_edges(sensors[i], distances[i]))

    # Get line segments
    lines_backward = []
    lines_forward = []
    for i in range(len(edges)):
        for j in range(len(edges)):
            if i != j:
                lb = get_overlap(edges[i], edges[j], 1)
                lf = get_overlap(edges[i], edges[j], -1)
                if len(lb) > 0:
                    lines_backward.append(lb)
                if len(lf) > 0:
                    lines_forward.append(lf)

    # Get line intersections
    intersections = []
    for lb in lines_backward:
        for lf in lines_forward:
            intersection = get_intersection(lb, lf, lim)
            if len(intersection) > 0:
                intersections.append(intersection)

    # Get tuning frequency
    if len(intersections):
        return lim * intersections[0][0] + intersections[0][1]
    else:
        print("Too many intersections!")


if __name__ == "__main__":

    print(f"There are {part1()} positions which cannot contain a beacon")
    print(f"Tuning frequency of distress beacon is {part2()}")
