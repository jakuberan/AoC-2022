
def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = []
    for x in f:
        out_temp = x.strip().split()
        out.append([out_temp[0], int(out_temp[1])])
    return out


def knot_fix(kn, off):
    """
    Fix a knot position, return if change was made
    """
    if (abs(off[0]) > 1) or (abs(off[1]) > 1):
        if abs(off[0]) == 1:
            kn[0] += off[0]
            kn[1] += int(off[1]/2)
        elif abs(off[1]) == 1:
            kn[0] += int(off[0]/2)
            kn[1] += off[1]
        else:
            kn[0] += int(off[0]/2)
            kn[1] += int(off[1]/2)                
        return kn, True
    else:
        return kn, False


def make_head(move, head):
    """
    Make single head move
    """
    m = {'R': [0, 1], 'L': [0, -1], 'U': [-1, 0], 'D': [1, 0]}
    
    return [head[i] + m[move][i] for i in range(2)]


def part1(data_path="input", num_knots=2):
    """
    Move head, record the last knot position
    """
    data = read_and_process(data_path)
    
    # Initialize a knot list and visited positions
    knots = [[0, 0] for _ in range(num_knots)]
    visited_positions = {(0, 0)}
    
    for move in data:
        for i in range(move[1]):
            # Move head
            knots[0] = make_head(move[0], knots[0])
            was_change = True
            
            # Fix remaining tails (if there are any)
            for k in range(num_knots - 1):
                if was_change:
                    offset = [knots[k][i] - knots[k + 1][i] for i in range(2)]
                    knots[k + 1], was_change = knot_fix(knots[k + 1], offset)
            
            # Record unseen position
            visited_positions.add((knots[-1][0], knots[-1][1]))
        
    return len(visited_positions)


if __name__ == "__main__":

    print(f"Number of distinct positions visited by tail is {part1()}")
    print(f"Number of distinct positions visited by last tail is {part1(num_knots=10)}")
