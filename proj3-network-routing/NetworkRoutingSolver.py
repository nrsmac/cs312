#!/usr/bin/python3


from CS312Graph import *
import time
from heap import *


class NetworkRoutingSolver:
    def __init__(self):
        self.distances = {}

    def initializeNetwork(self, network):
        assert (type(network) == CS312Graph)
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex

        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE

        path_edges = []
        total_length = 0
        # node = self.network.nodes[self.source]
        # edges_left = 3
        #
        # nodes = self.network.nodes
        destNode = self.network.nodes[destIndex]
        path_nodes = []
        path_nodes.insert(0, destNode)

        node = destNode
        while node is not None:
            path_nodes.append(node)
            node = self.distances[node][1]

        at_dest = False
        while not at_dest:
            node = path_nodes.pop()
            if node is destNode:
                at_dest = True
            for edge in node.neighbors:
                if edge.dest in path_nodes:
                    path_edges.append(edge)

        for edge in path_edges:
            total_length += edge.length

        path_edge_tuples = []

        while len(path_edges) > 0:
            edge = path_edges.pop()
            path_edge_tuples.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))

        return {'cost': total_length, 'path': path_edge_tuples}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()

        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        if not use_heap:
            self.dijkstra_array(srcIndex)
        else:
            self.dijkstra_heap(srcIndex)
        t2 = time.time()
        return (t2 - t1)

    def dijkstra_heap(self, srcIndex):
        nodes = self.network.nodes.copy()
        heap = Heap(len(nodes)+1)
        srcNode = nodes.pop(srcIndex)
        table = {}

        visited = []

        for node in nodes:
            table[node] = [float("inf"), None]

        table[srcNode] = [0, None]
        node = srcNode
        heap.insert(HeapEntry(node, 0, None))

        while heap.size != 0:
            popped = heap.pop()
            visited.append(popped.node)
            for edge in popped.node.neighbors:
                new_distance = table[popped.node][0] + edge.length
                if new_distance < table[edge.dest][0]:
                    table[edge.dest] = [new_distance, popped.node]
                    heap.insert(HeapEntry(edge.dest, new_distance, popped.node))

        self.distances = table.copy()

    def dijkstra_array(self, srcIndex):
        nodes = self.network.nodes.copy()
        srcNode = nodes.pop(srcIndex)
        table = {srcNode: [0, None], }
        visited = []
        unvisited = [srcNode]
        for node in nodes:
            unvisited.append(node)
            table[node] = [float("inf"), None]
        node = srcNode
        while len(unvisited) != 0:
            for neighbor_edge in [n for n in node.neighbors if n not in visited]:
                neighbor = neighbor_edge.dest
                new_distance = table[node][0] + neighbor_edge.length
                if new_distance < table[neighbor][0]:
                    table[neighbor] = [new_distance, node]
            visited.append(node)
            unvisited.remove(node)

            min_node = None
            min_distance = float('inf')
            for node in unvisited:
                if table[node][0] <= min_distance:
                    min_node = node
                    min_distance = table[node][0]

            node = min_node
        self.distances = table.copy()
