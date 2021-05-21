from heap import Heap
from operator import attrgetter

class PriorityQueue:
    ARRAY = 0
    HEAP = 1 # TODO make these boolean

    def __init__(self, using=ARRAY):
        self.using = using

        # Init data structure depending on using
        if using == PriorityQueue.ARRAY:
            self.data = []
        elif using == PriorityQueue.HEAP:
            self.data = Heap()
        else:
            raise ValueError("Invalid data structure choice.")

    def insert(self, data):
        if self.using == PriorityQueue.ARRAY:
            self.data.append(data)
            self.sort()
        else:
            self.data.insert(data)

    def pop(self):
        if self.using == PriorityQueue.ARRAY:
            return self.data.pop(0)
        else:
            return self.data.delete(self)

    def update(self, id, value, prev):
        if self.using == PriorityQueue.ARRAY:
            for node_tuple in self.data:
                if node_tuple[0].node_id == id:
                    node_tuple[1] = value
                    node_tuple[2] = prev
            self.sort()
        else:
            pass

    def peek(self):
        if self.using == PriorityQueue.ARRAY:
            return self.data[0]
        else:
            return self.data.root

    def get_distance(self, id):
        if self.using == PriorityQueue.ARRAY:
            for node in self.data:
                if node[0].node_id == id:
                    return node[1]
            return 0
        else:
            pass

    def is_empty(self):
        if self.using == PriorityQueue.ARRAY:
            return len(self.data)\
                   == 0
        else:
            return self.data.root is None

    def sort(self):
        self.data.sort(key=lambda n: n[1])

    def size(self):
        return len(self.data)