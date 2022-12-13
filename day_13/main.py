import ast
from copy import deepcopy


def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    pairs = []
    l1 = None
    for x in f:
        if len(x.strip()) > 0:
            if l1 is None:
                l1 = ast.literal_eval(x.strip())
            else:
                pairs.append([l1, ast.literal_eval(x.strip())])
                l1 = None
    return pairs


def compare_pair(left, right):
    """
    Compares left and right package
    """
    out = None
    while out is None:
        try:
            r0 = right.pop(0)
            try:
                l0 = left.pop(0)
                if type(l0) is int:
                    if type(r0) is int:
                        if l0 > r0:
                            out = False
                        elif l0 < r0:
                            out = True
                    else:
                        out = compare_pair([l0], r0)
                elif type(r0) is int:
                    out = compare_pair(l0, [r0])
                else:
                    out = compare_pair(l0, r0)
            except IndexError:
                return True
        except IndexError:
            if len(left) == 0:
                return None
            else:
                return False
    return out

    
def part1(data_path="input"):
    """
    Calculate sum of indices of OK pairs
    """
    pairs = read_and_process(data_path)
    
    # Calculate sum of OK pair indices
    out = 0
    for i in range(len(pairs)):
        if compare_pair(pairs[i][0], pairs[i][1]):
            out += 1 + i
        
    return out


def part2(data_path="input"):
    """
    Calculates the number of OK pairs and thus decoder key 
    """
    pairs = read_and_process(data_path)
    
    # Calculate decode key
    before = [0, 0]
    for i in range(len(pairs)):
        for j in range(2):
            if compare_pair(deepcopy(pairs[i][j]), [[2]]):
                before[0] += 1
            elif compare_pair(deepcopy(pairs[i][j]), [[6]]):
                before[1] += 1
     
    return (before[0] + 1) * (before[0] + before[1] + 2)
                              

if __name__ == "__main__":

    print(f"Sum of indices of OK pairs is {part1()}")
    print(f"Decoder key is {part2()}")

 