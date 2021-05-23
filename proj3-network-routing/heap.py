class Heap:

    def __init__(self):
        self.list = []
        self.list.append(None)  # A zero will screw up indexing
        self.size = 0

    def insert(self, node):
        self.list.append(node)
        self.size += 1
        self.move_up()

    def move_up(self):
        i = self.size

        node = self.list[i]
        parent = self.list[i // 2]
        while i // 2 > 0:  # Stop if we hit the root at 0
            if node.weight > parent.weight:
                node, parent = parent, node
            i = i // 2

    def move_down(self):

        i = 1  # Start at root

        while (i*2) <= self.size:

            min_index = self.get_min_child(i)

            current_node = self.list[i]
            min_node = self.list[min_index]

            if current_node.weight > min_node.weight:
                min_node, current_node = current_node,
            i = min_index

    def get_min_child(self, i):

        if (i * 2) + 1 > self.size:
            return i * 2
        else:
            if self.list[i * 2].weight < self.list[(i * 2) + 1].weight:
                return i * 2
            else:
                return (i * 2) + 1

    def delete(self):

        if len(self.list) < 1:
            raise ValueError("No items in heap")
        deleted = self.list[self.size]
        self.list[1] = self.list[self.size]
        self.list.pop(self.size)
        self.size -= 1
        self.move_down()
        return deleted


class HeapEntry:

    def __init__(self, node, weight=0, previous=None):
        self.node = node
        self.weight = weight
        self.previous = previous
