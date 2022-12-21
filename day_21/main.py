
def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = dict()
    for x in f:
        line = x.strip().split()
        if len(line) > 2:
            out[line[0][:-1]] = [line[1], line[2], line[3]]
        else:
            out[line[0][:-1]] = int(line[1])
    return out


def walk_tree(tree: dict, node: str) -> float:
    """
    Walk the tree and calculate number in the root
    """
    if type(tree[node]) is int:
        return tree[node]
    else:
        num1 = walk_tree(tree, tree[node][0])
        num2 = walk_tree(tree, tree[node][2])
        # Apply operations
        if tree[node][1] == '+':
            return num1 + num2
        elif tree[node][1] == '-':
            return num1 - num2
        elif tree[node][1] == '*':
            return num1 * num2
        elif tree[node][1] == '/':
            return num1 / num2
        else:
            print("Unrecognized operation")
            
            
def part1(data_path="input") -> int:
    """
    Traverse the monkey tree and find root s answer
    """
    data = read_and_process(data_path)
        
    return int(walk_tree(data, 'root'))


def simplify_tree(tree: dict, node: str, hmn: str):
    """
    Simplify the tree so that only the unknown nodes remain
    """
    if node == hmn:
        return hmn, tree
    elif type(tree[node]) is int:
        num_out = tree[node]
        del tree[node]
        return num_out, tree
    else:
        tree[node][0], tree = simplify_tree(tree, tree[node][0], hmn)
        tree[node][2], tree = simplify_tree(tree, tree[node][2], hmn)
        if (type(tree[node][0]) is str) or (type(tree[node][2]) is str):
            return node, tree
        # Apply operations where both numbers are available
        else:
            num_out = None
            if tree[node][1] == '+':
                num_out = tree[node][0] + tree[node][2]
            elif tree[node][1] == '-':
                num_out = tree[node][0] - tree[node][2]
            elif tree[node][1] == '*':
                num_out = tree[node][0] * tree[node][2]
            elif tree[node][1] == '/':
                num_out = tree[node][0] / tree[node][2]
            else:
                print("Unrecognized operation")
            del tree[node]
            return num_out, tree
        
        
def make_equal(tree: dict, hmn: str) -> float:
    """
    Search for number in selected node which makes the output in root equal
    """
    node = 'root'
    want = None
    while node != hmn:
        num_id = 0 if (type(tree[node][2]) is str) else 2
        num = tree[node][num_id]
        if node == 'root':
            want = num
        else:
            # Apply reverse operations
            if tree[node][1] == '+':
                want = want - num
            elif tree[node][1] == '-':
                if num_id == 0:
                    want = num - want
                else:
                    want = num + want
            elif tree[node][1] == '*':
                want = want / num
            elif tree[node][1] == '/':
                if num_id == 0:
                    want = num / want
                else:
                    want = num * want
            else:
                print("Unrecognized operation") 
        node = tree[node][2 - num_id]
    return want
    

def part2(data_path="input", human_node='humn') -> int:
    """
    Simplify and then apply reverse operations
    """
    data = read_and_process(data_path)
    
    # Simplify the tree and evaluate all possible nodes
    _, tree = simplify_tree(data, 'root', human_node)

    return int(make_equal(tree, human_node))


if __name__ == "__main__":

    print(f"Root monkey will yell the number is {part1()}")
    print(f"Number to yell to pass root's equality test is {part2()}")
