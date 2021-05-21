class Heap:
    def __init__(self, data=None):
        self.array = []
        self.size = 0
        self.root = None
        if data is not None:
            for i in data:
                self.insert(i)
                self.size += 1
        self.heapify()

    def heapify(self):
        pass

    def insert(self, vertex):
        if self.root is None:
            self.root = vertex
        else:
            self.insert_helper(vertex, self.root)

    def insert_helper(self, to_be_inserted, vertex_in_heap):
        pass

    def delete(self):
        pass

    def extract(self):
        pass

    def size(self):
        pass

    def min(self):
        pass

    def max(self):
        pass
