class Directory:
    def __init__(self, name, up):
        self.name = name
        self.up = up
        self.down = {}
        self.size = 0

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size


class FileSystem:
    def __init__(self):
        self.current = Directory("/", None)
        self.root = self.current

    def get_root(self):
        return self.root

    def move_to_dir(self, directory):
        self.current = directory

    def move_up(self):
        self.current = self.current.up

    def add_dir(self, dir_name):
        self.current.down[dir_name] = Directory(dir_name, self.current)

    def move_down(self, dir_name):
        if dir_name in self.current.down:
            self.current = self.current.down[dir_name]
        else:
            print(f"Directory {dir_name} not found!")

    def add_size(self, file_size):
        self.current.size += file_size


def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    out = []
    for x in f:
        out.append(x.strip().split())

    return out


def build_fs(commands):
    """
    Build the File System together with actual and total size
    """

    fs = FileSystem()

    for c in commands[1:]:
        if c[0] == "dir":
            fs.add_dir(c[1])
        elif c[0] == "$":
            if c[1] == "cd":
                if c[2] == "..":
                    fs.move_up()
                else:
                    fs.move_down(c[2])
        else:
            fs.add_size(int(c[0]))

    return fs


def sizes_from_curr_dir(fs):
    """
    List of absolute sizes viewed from current directory and sizes of subdirectories
    """
    size_abs_cur = fs.current.get_size()
    size_list = []
    if len(fs.current.down) == 0:
        return size_abs_cur, [size_abs_cur]
    else:
        for d in fs.current.down:
            fs.move_down(d)
            subdir_size, all_sizes = sizes_from_curr_dir(fs)
            fs.move_up()
            size_abs_cur += subdir_size
            size_list += all_sizes
        return size_abs_cur, size_list + [size_abs_cur]


def part1(data_path="input", threshold=100000):
    """
    Builds file system and return sum of dir sizes under threshold
    """
    data = read_and_process(data_path)
    fs = build_fs(data)

    # Calculate sizes of all directories
    fs.move_to_dir(fs.root)
    all_sizes = sizes_from_curr_dir(fs)[1]

    return sum([s for s in all_sizes if s <= threshold])


def part2(data_path="input", total_space=70000000, needed_space=30000000):
    """
    Find the smallest directory which deletion will free up enough space
    """
    data = read_and_process(data_path)
    fs = build_fs(data)

    # Calculate sizes of all directories
    fs.move_to_dir(fs.root)
    all_sizes = sizes_from_curr_dir(fs)[1]

    # Find size which deletion will free up enough space
    all_sizes.sort(reverse=True)
    i = 0
    while total_space - needed_space > all_sizes[0] - all_sizes[i + 1]:
        i += 1

    return all_sizes[i]


if __name__ == "__main__":

    print(f"Sum of directory sizes below threshold is {part1()}")
    print(f"Smallest dictionary enough to delete is {part2()}")
