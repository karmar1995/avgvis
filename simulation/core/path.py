class Path:
    def __init__(self, path, cost, collisions):
        self.path = path
        self.cost = cost
        self.collisions = collisions

    def __gt__(self, other):
        return self.cost > other.cost

    def __lt__(self, other):
        return other > self

    def __eq__(self, other):
        return not self > other and not other > self