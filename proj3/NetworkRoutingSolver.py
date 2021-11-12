#!/usr/bin/python3
import math

from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__(self):
        self.dijsktra_result = {}

    def initializeNetwork(self, network):
        assert (type(network) == CS312Graph)
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex
        dest_node = self.network.nodes[destIndex]
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL
        #       NEED TO USE
        total_length = 0
        path_edges = []
        # node = self.network.nodes[self.source]
        # edges_left = 3
        # while edges_left > 0:
        #     edge = node.neighbors[2]
        #     path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
        #     total_length += edge.length
        #     node = edge.dest
        #     edges_left -= 1
        # Assemble edges
        p = dest_node
        while p != None:
            prev = self.dijsktra_result[p][1]
            if p.node_id != self.source and p is not None:
                l = self.dijsktra_result[p][0]
                total_length += l
                path_edges.append((p.loc, prev.loc, '{:.0f}'.format(l)))
            p = prev
        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        src = self.network.nodes[srcIndex]
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        self.dijkstra(src, use_heap)
        t2 = time.time()
        return (t2 - t1)

    def dijkstra(self, src, use_heap):
        # Create queue
        if use_heap:
            H = PriorityHeap()
        else:
            H = PriorityQueue()

        nodes = self.network.nodes

        the_table = {src: (0, None)}  # Format is Node:(Distance, Previous)
        dists = []  # To be passed to the heap
        dists.append((src, 0))

        for node in nodes:  # O(n)
            if node is not src:
                the_table[node] = (math.inf, None)
                dists.append((node, math.inf))

        H.make_queue(dists)  # O(n log n) for array, O(log n) for heap if it needs to be swapped

        while not H.is_empty():
            u, u_l = H.delete_min()  # O(1) for array as it's already sorted,
            for neighbor_edge in u.neighbors:  # O(neighbors) for any node
                if the_table[neighbor_edge.dest][0] > the_table[u][0] + neighbor_edge.length:
                    the_table[neighbor_edge.dest] = (the_table[u][0] + neighbor_edge.length, u)
                    H.decrease_key(neighbor_edge.dest, the_table[u][0] + neighbor_edge.length)

        self.dijsktra_result = the_table


class PriorityQueue:
    def __init__(self):
        self.array = []

    def __str__(self):
        print(__name__ + " : " + self.array)

    def make_queue(self, array_of_tuples):  # O(n log n)
        self.array = array_of_tuples.copy()
        self.array.sort(key=lambda x: x[1])  # Timsort is O(n log n)

    def insert(self, node, distance):  # O(n log n)
        self.array.append((node, distance))
        self.array.sort(key=lambda x: x[1])  # Timsort is O(n log n)

    def delete_min(self):
        return self.array.pop(0)  # O(1)

    def decrease_key(self, node_name, new_value):  # O(n)
        for tup in self.array:
            if tup[0] == node_name:
                new_tuple = (tup[0], new_value)
                self.array.remove(tup)
                self.insert(new_tuple[0], new_tuple[1])

    def length(self):
        return len(self.array)

    def is_empty(self):
        return len(self.array) == 0


class PriorityHeap:
    def __init__(self):
        # makequeue happens here
        self.maxsize = 1000001
        self.size = 0
        self.map = {}
        self.array = [(None, -math.inf)] * self.maxsize
        self.array[0] = (None, -math.inf)  # A zero will screw up indexing

    def is_empty(self):
        return self.size == 0

    def parent(self, i):
        return i // 2

    def left_child(self, i):
        return 2 * i

    def right_child(self, i):
        return (2 * i) + 1

    def swap(self, i, j):  # O(1)
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def is_leaf(self, i):
        if (self.size // 2) <= i <= len(self.array):
            return True
        return False

    def pop(self): # O(log n)
        if len(self.array) <= 1:
            raise ValueError("No items in heap")

        popped = self.array[1]
        self.array[1] = self.array[self.size]
        self.heapify(1) #O(log n)
        self.size -= 1
        return popped

    def peek(self):
        return self.array[1]

    def heapify(self,
                i):  # O(log n), as the tree height is O(log n) and at worst will need to be bubbled up the entire height
        if not self.is_leaf(i):
            if self.array[i][1] > self.array[self.left_child(i)][1] or self.array[i][1] > \
                    self.array[self.right_child(i)][1]:

                # left side recursive call
                if self.array[self.left_child(i)][1] < self.array[self.right_child(i)][1]:  # left child swap
                    self.swap(i, self.left_child(i))
                    self.heapify(self.left_child(i))

                # right side recursive call
                else:
                    self.swap(i, self.right_child(i))
                    self.heapify(self.right_child(i))

    def insert(self, node, distance):  # O(log n)
        if self.size >= self.maxsize:
            return
        self.size += 1
        self.array[self.size] = (node, distance)
        p = self.size

        while self.array[p][1] < self.array[self.parent(p)][1]:
            self.swap(p, self.parent(p))
            p = self.parent(p)
        self.map[node] = p

    def make_queue(self, elements):  # O(n)
        # build a priority queue out of given elements
        for tup in elements:
            self.insert(tup[0], tup[1])

    def delete_min(self):  # O(1)
        # Return element with the smallest key and remove it from the
        return self.pop()

    def decrease_key(self, node_name, new_value):  # O(log n), at worst will need to descend the entire tree
        i = self.map[node_name]
        self.array[i] = (node_name, new_value)
        while i > 1:
            if self.array[i][1] < self.array[i // 2][1]:
                self.swap(i, i // 2)
                i = i // 2
            else:
                break
        self.map[node_name] = i
