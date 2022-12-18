import numpy as np
from copy import deepcopy


def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = []
    for x in f:
        out.append([int(c) for c in x.strip().split(',')])
    return out


def num_neighbors(c, cube_set) -> int:
    """
    Check number of neighbors in specified cube set
    """
    neigh_num = 0
    if (c[0] - 1, c[1], c[2]) in cube_set:
        neigh_num += 1
    if (c[0] + 1, c[1], c[2]) in cube_set:
        neigh_num += 1
    if (c[0], c[1] - 1, c[2]) in cube_set:
        neigh_num += 1
    if (c[0], c[1] + 1, c[2]) in cube_set:
        neigh_num += 1
    if (c[0], c[1], c[2] - 1) in cube_set:
        neigh_num += 1
    if (c[0], c[1], c[2] + 1) in cube_set:
        neigh_num += 1
    return neigh_num


def part1(data_path="input"):
    """
    Calculate overall surface of lava droplet
    """
    cubes = read_and_process(data_path)
    cube_set = set([tuple(c) for c in cubes])
    
    side_sub = 0
    # Calculate neighboring sides
    for c in cubes:
        side_sub += num_neighbors(c, cube_set)
        
    return 6 * len(cubes) - side_sub


def identify_inside(minmax: list, cube_set: set):
    """
    Identifies inside area of the cube by creating outside cover
    """
    outside = set()
    inside = set()
    
    # First layer
    for x in range(minmax[0][0] - 1, minmax[1][0] + 2):
        for y in range(minmax[0][1] - 1, minmax[1][1] + 2):
            outside.add((x, y, minmax[0][2] - 1))
                
    # Layer by layer check cubes
    for z in range(minmax[0][2], minmax[1][1] + 2):
        # Create layer
        layer = []
        for x in range(minmax[0][0] - 1, minmax[1][0] + 2):
            for y in range(minmax[0][1] - 1, minmax[1][1] + 2):
                layer.append((x, y, z))

        # While no movement in layer add respective cubes to outside
        cubes_remaining = deepcopy(layer)
        cubes_to_check = []
        while len(cubes_to_check) != len(cubes_remaining):
            cubes_to_check = deepcopy(cubes_remaining)
            cubes_remaining = []
            for c in cubes_to_check:
                if c not in cube_set:
                    if num_neighbors(c, outside):
                        outside.add(c)
                    else:
                        cubes_remaining.append(c)
                        
        # Add remaining cubes to inside set
        for c in cubes_remaining:
            inside.add(c)
            
    # Remove from inside if it has neighbor outside
    before_len = len(inside)
    after_len = 0
    while before_len > after_len:
        before_len = len(inside)
        inside_list = list(inside)
        for c in inside_list:
            if num_neighbors(c, outside):
                outside.add(c)
                inside.remove(c)
        after_len = len(inside)
         
    return inside


def part2(data_path="input"):
    """
    Calculate overall exterior surface of lava droplet
    """
    cubes = read_and_process(data_path)
    cube_set = set([tuple(c) for c in cubes])
    
    # Calculate min and max in each direction
    minmax = [[np.inf, np.inf, np.inf], [-np.inf, -np.inf, -np.inf]]
    for i in range(len(cubes)):
        for j in range(3):
            minmax[0][j] = min(minmax[0][j], cubes[i][j])
            minmax[1][j] = max(minmax[1][j], cubes[i][j])
            
    # Create inside set of cubes
    inside = identify_inside(minmax, cube_set)
    
    # Calculate neighboring cubes and cubes inside the cube set
    side_sub = 0
    for c in cubes:
        side_sub += num_neighbors(c, cube_set)
        side_sub += num_neighbors(c, inside)
        
    return 6 * len(cubes) - side_sub


if __name__ == "__main__":

    print(f"Surface area of the scanned lava droplet is {part1()}")
    print(f"Exterior surface area of the scanned lava droplet is {part2()}")
