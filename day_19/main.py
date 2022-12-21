from copy import deepcopy
import numpy as np


def read_and_process(data_path: str):
    """
    Process and prepare input data
    """
    f = open(data_path, "r")
    out = []
    for x in f:
        line = x.strip().split()
        out.append([
            int(line[6]), 
            int(line[12]), 
            [int(line[18]), int(line[21])],
            [int(line[27]), int(line[30])]
            ])
    return out
            

def resources_needed(i: int, bp: list) -> list:
    """
    Returns resources needed for the build of given robot
    """
    if i == 0:
        return [bp[0], 0, 0, 0]
    if i == 1:
        return [bp[1], 0, 0, 0]
    if i == 2:
        return [bp[2][0], bp[2][1], 0, 0]
    if i == 3:
        return [bp[3][0], 0, bp[3][1], 0]


def possible_builds(res: list, bp: list) -> list:
    """
    Identifies if new robots can be build using available resources
    """
    can_build = [False] * 4
    can_build[0] = (res[0] >= bp[0])
    can_build[1] = (res[0] >= bp[1])
    can_build[2] = ((res[0] >= bp[2][0]) and (res[1] >= bp[2][1]))
    can_build[3] = ((res[0] >= bp[3][0]) and (res[2] >= bp[3][1]))
    return can_build


def maximum_robots(bp: list) -> list:
    """
    Places upper limit on robot builds by possible resources spent
    """
    max_rob = [np.inf] * 4
    max_rob[0] = max(bp[0], bp[1], bp[2][0], bp[3][0])
    max_rob[1] = bp[2][1]
    max_rob[2] = bp[3][1]
    return max_rob


def find_max_geode(
        rob: list, rob_new, res: list, ava: list, bp: list,
        t: int, max_t: int) -> int:
    """
    Searches for maximal geode given blueprint
    Apply pruning rules
    - If no robot was built, do not build any of currently available robots next
    - Do not build more robots than needed (max resources)
    """
    if t == max_t:
        return res[-1]
    
    # Collect resources
    for i in range(4):
        res[i] += rob[i]
        
    # Update robots
    if rob_new is not None:
        rob[rob_new] += 1
        
    # Generate list of available robots and maximum number of robots needed
    build_list = possible_builds(res, bp)
    build_max = maximum_robots(bp)
    
    geo_max = 0
    for i in range(4):
        # Limit availability and number of robots
        if build_list[i] and ava[i] and (rob[i] < build_max[i]):
            if (i == 3) or not build_list[3]:
                res_need = resources_needed(i, bp)
                res_new = deepcopy(res)
                res_new = [res_new[i] - res_need[i] for i in range(4)]
                ava_new = [True] * 4
                geo_future = find_max_geode(
                    deepcopy(rob), i, res_new, ava_new, bp, t + 1, max_t
                    )
                geo_max = max(geo_max, geo_future)
            
    # No build - limit the available robots in next iteration
    if not build_list[3]:
        ava_new = [b == 0 for b in build_list]
        geo_future = find_max_geode(
            deepcopy(rob), None, deepcopy(res), ava_new, bp, t + 1, max_t
            )
        geo_max = max(geo_max, geo_future)
    
    return geo_max


def solve(data_path="input", max_time=24) -> int:
    """
    Calculate maximum reachable geode per blueprint
    Combine this to quality score for part 1 and limit to 3 blueprints in 2
    """
    data = read_and_process(data_path)
    max_bp = []
    
    # Search for best blueprint schedule
    q_level = 0
    max_mult = 1
    for i, blueprint in enumerate(data):
        if (i < 3) or (max_time == 24):
            print(blueprint)
            # Starting resources, robots and availability
            resources = [0, 0, 0, 0]
            robots = [1, 0, 0, 0]
            available = [True, True, True, True]
            max_bp.append(find_max_geode(
                robots, None, resources, available, 
                blueprint, t=0, max_t=max_time
                ))
            q_level += (i + 1) * max_bp[i]
            max_mult *= max_bp[i]
        
    if max_time == 24:
        return q_level
    else:
        return max_mult


if __name__ == "__main__":

    print(f"Sum of quality levels of all of the blueprints is {solve()}")
    print(f"Multiplied best geode levels is {solve(max_time=32)}")
