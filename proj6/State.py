import math
import numpy as np


class State:
    def __init__(self, cost, matrix: np.array, path: []):
        self.cost = cost
        self.matrix = matrix
        self.path = path

    def get_h(self):
        if self.cost != math.inf:
            return self.cost - (20 * len(self.path))
        else:
            return math.inf

    def __repr__(self):
        return f"S_{self.path}: {self.cost}"

    def __lt__(self, other):
        return self.get_h() < other.get_h()

    def __gt__(self, other):
        return self.get_h() > other.get_h()

    def __ge__(self, other):
        return self.get_h() >= other.get_h()

    def __le__(self, other):
        return self.get_h() <= other.get_h()

    def __eq__(self, other):
        return self.get_h() == other.get_h()

    def __ne__(self, other):
        return self.get_h() != other.get_h()
