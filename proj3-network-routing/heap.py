class Heap:

    def __init__(self, size):
        blank_entry = HeapEntry(None, 0, None)
        self.list = [blank_entry]*(size+1)
        self.list[0] = None  # A zero will screw up indexing
        self.size = 0

    def insert(self, node):
        self.size += 1
        self.list[self.size ] = node
        i = self.size
        while (self.list[i//2] is not None and self.list[i] is not None) and self.list[i].weight < self.list[i//2].weight:
            self.list[i], self.list[(i-1)//2] = self.list[(i-1)//2], self.list[i]

    def heapify(self, i):
        l = (i*2)
        r = (i*2) + 1

        if not (i >= self.size//2 and i <= self.size):
            if self.list[i].weight > self.list[r].weight or self.list[i].weight > self.list[r].weight:
                if self.list[l].weight < self.list[r].weight:
                    self.list[i], self.list[l] = self.list[l], self.list[i]
                    self.heapify(l)
                else:
                    self.list[i], self.list[r] = self.list[r], self.list[i]
                    self.heapify(r)


    def pop(self):
        if len(self.list) <= 1:
            raise ValueError("No items in heap")

        deleted = self.list[1]
        self.list[1] = self.list[self.size]
        self.size -= 1
        self.heapify(1)
        return deleted

    def peek(self):
        return self.list[1]


class HeapEntry:

    def __init__(self, node, weight=0, previous=None):
        self.node = node
        self.weight = weight
        self.previous = previous

    def __repr__(self):
        return repr("Node: " + str(self.node) + " weight: " + str(self.weight) + " previous: " + str(self.previous))
