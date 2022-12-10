
def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = []
    for x in f:
        out_temp = x.strip().split()
        if len(out_temp) == 1:
            out.append(['n'])
        else:
            out.append(['a', int(out_temp[1])])
    return out


def move_and_record(time: int, times: list, out: dict, x: int):
    """
    Move time and record signal if this time is interesting
    """
    time += 1
    if time in times:
        out[time] = x
        
    return time, out


def get_signal_strengths(program: list, times: list):
    """
    Signal strength at pre-defined times
    """
    x = 1
    time = 0
    out = {}
    for p in program:
        time, out = move_and_record(time, times, out, x)
        if p[0] == 'a':
            time, out = move_and_record(time, times, out, x)
            x += p[1]
    return out
        

def move_and_draw(time: int, x: int, line: list, crt: list, width: int):
    """
    Draw, move time and move to new line, if needed
    """
    if abs(time - x) < 2:
        line[time] = '#'
    time += 1
    if time % width == 0:
        crt.append(line)
        line = ['.'] * width
        time = 0
    return time, line, crt

       
def draw_crt(program: list, width=40):
    """
    Draw crt
    """
    crt = []
    line = ['.'] * width
    x = 1
    time = 0
    for p in program:
        time, line, crt = move_and_draw(time, x, line, crt, width)
        if p[0] == 'a':
            time, line, crt = move_and_draw(time, x, line, crt, width)
            x += p[1]
    return crt
        

def print_crt(crt):
    """
    Print crt
    """
    for r in range(len(crt)):
        print(''.join(crt[r]))


def part1(data_path="input"):
    """
    Sum of signal strengths
    """
    data = read_and_process(data_path)
    time_values = get_signal_strengths(data, [20, 60, 100, 140, 180, 220])
    sum_at_cycles = sum([k * v for k, v in time_values.items()])
        
    return sum_at_cycles


def part2(data_path="input"):
    """
    Draw and print out CRT
    """
    data = read_and_process(data_path)
    crt = draw_crt(data)
    print_crt(crt)


if __name__ == "__main__":

    print(f"\nSum of signal strengths is {part1()}\n")
    part2()
