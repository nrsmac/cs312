import numpy as np


class State:
    def __init__(self, cost, matrix: np.array, path: []):
        self.cost = cost
        self.matrix = matrix
        self.path = path

    def __repr__(self):
        return f"S_{self.path}: {self.cost}"

    def __lt__(self, other):
        return self.cost < other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __ge__(self, other):
        return self.cost >= other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __eq__(self, other):
        return self.cost == other.cost

    def __ne__(self, other):
        return self.cost != other.cost

