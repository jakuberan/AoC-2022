class Monkey:
    def __init__(self, data):
        self.number = int(data[0][1][:-1])
        self.divisor = int(data[3][3])
        self.if_true = int(data[4][5])
        self.if_false = int(data[5][5])
        self.opr = data[2][3:]
        self.item_count = 0
        self.modulo = None
        self.items = None
        item_line = " ".join(data[1])
        self.set_starting_items(item_line)

    def set_modulo(self, mod):
        self.modulo = mod

    def set_starting_items(self, line):
        self.items = [int(c) for c in (line.split(": ")[1]).split(", ")]

    def add_item(self, item):
        self.items.append(item)

    def update_item_count(self):
        self.item_count += len(self.items)

    def get_item(self):
        if len(self.items) == 0:
            return None
        else:
            return self.items.pop(0)

    def new_worry(self, worry, part):
        out = worry if self.opr[0] == "old" else int(self.opr[0])
        if self.opr[1] == "+":
            out += worry if self.opr[2] == "old" else int(self.opr[2])
        elif self.opr[1] == "*":
            out *= worry if self.opr[2] == "old" else int(self.opr[2])
        else:
            print("Unknown operation")
        if part == 1:
            return int(out / 3)
        else:
            return out % self.modulo

    def get_next_monkey(self, part):
        item = self.get_item()
        if item is not None:
            new_item = self.new_worry(item, part)
            if new_item % self.divisor == 0:
                return self.if_true, new_item
            else:
                return self.if_false, new_item
        else:
            return None, None

    def get_number(self):
        return self.number

    def get_divisor(self):
        return self.divisor

    def get_if_true(self):
        return self.if_true

    def get_if_false(self):
        return self.if_false

    def print_monkey(self):
        print(f"Monkey {self.number}:")
        print(f"Items: {', '.join([str(i) for i in self.items])}")
        print(f"Operation: {''.join(self.opr)}")
        print(f"Test divisible by: {self.divisor}")
        print(f"If true throw to monkey: {self.if_true}")
        print(f"If false throw to monkey: {self.if_false}")


def read_and_process(data_path: str):
    """
    Process and prepare input data
    """

    f = open(data_path, "r")
    monkeys = {}
    data = []
    for x in f:
        if len(x.strip()) > 0:
            data.append(x.strip().split())
        else:
            monkey = Monkey(data)
            monkeys[monkey.get_number()] = monkey
            data = []
    monkey = Monkey(data)
    monkeys[monkey.get_number()] = monkey

    return monkeys


def solve(data_path="input", rounds=20, part=1):
    """
    Calculates monkey business score, i.e.,
    Multiplication of item counts for two most active monkeys
    """
    monkeys = read_and_process(data_path)

    # Get modulo and apply it to all monkeys
    modulo = 1
    for m in range(len(monkeys)):
        modulo *= monkeys[m].get_divisor()
    for m in range(len(monkeys)):
        monkeys[m].set_modulo(modulo)

    # Make rounds
    for _ in range(rounds):
        # Throw items
        for m in range(len(monkeys)):
            monkeys[m].update_item_count()
            next_monkey, next_worry = monkeys[m].get_next_monkey(part)
            while next_monkey is not None:
                monkeys[next_monkey].add_item(next_worry)
                next_monkey, next_worry = monkeys[m].get_next_monkey(part)

    # Get number of items handled
    item_counts = []
    for m in range(len(monkeys)):
        item_counts.append(monkeys[m].item_count)
    item_counts.sort(reverse=True)

    return item_counts[0] * item_counts[1]


if __name__ == "__main__":

    print(f"Monkey business score for part 1 is {solve()}")
    print(f"Monkey business score for part 2 is {solve(rounds=10000, part=2)}")
