#!/usr/bin/python3


from CS312Graph import *
import time
from priority_queue import *


class NetworkRoutingSolver:
    def __init__( self ):
        self.distances = {}

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
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
        dest_node_entry = self.distances[destNode.node_id]
        total_length = self.get_path(dest_node_entry, total_length, path_nodes)

        ##TODO return list of GraphEdges!!
        at_dest = False
        while not at_dest:
            node = path_nodes.pop()
            if node is destNode:
                at_dest = True
            for edge in node.neighbors:
                if edge.dest in path_nodes:
                    path_edges.append(edge)

        path_edge_tuples = []

        while len(path_edges) > 0:
            edge = path_edges.pop()
            path_edge_tuples.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))

        return {'cost':total_length, 'path':path_edge_tuples}

    def get_path(self, dist_entry, length, path):
        if dist_entry[1] is None:  # Base case, node has no previous
            return 0
        length += dist_entry[0]
        path.append(self.network.nodes[dist_entry[1]])
        return length + self.get_path(self.distances[dist_entry[1]], length, path)

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()

        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        nodes = self.network.nodes.copy()
        queue = PriorityQueue()
        srcNode = nodes.pop(srcIndex)
        queue.insert([srcNode, 0, None])
        distances = {srcNode.node_id: [0, None]}

        for node in nodes:
            queue.insert([node, float("inf"), None])
            distances[node.node_id] = [float("inf"), None]

        while not queue.is_empty():
            u = queue.pop()[0]
            for edge in u.neighbors:
                v = edge.dest
                weight = edge.length
                if distances[v.node_id][0] > distances[u.node_id][0] + weight:
                    distances[v.node_id][0] = distances[u.node_id][0] + weight
                    distances[v.node_id][1] = u.node_id

        self.distances = distances.copy()
        t2 = time.time()
        return (t2-t1)

