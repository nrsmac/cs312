#!/usr/bin/python3
import copy

from PyQt5.QtCore import QLineF, QPointF

import time
import numpy as np

from TSPClasses import *
import heapq
import itertools


class TSPSolver:
    def __init__(self, gui_view):
        self._scenario = None

    ''' <summary>
        This is the entry point for the default solver
        which just finds a valid random tour.  Note this could be used to find your
        initial BSSF.
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of solution, 
        time spent to find solution, number of permutations tried during search, the 
        solution found, and three null values for fields not used for this 
        algorithm</returns> 
    '''

    def createMatrix(self, cities):
        matrix = [[float('inf') for x in cities] for x in cities]
        for i in cities:
            for j in cities:
                if self._scenario._edge_exists[i._index][j._index]:
                    first = cities[i._index]
                    second = cities[j._index]
                    pathcost = first.costTo(second)
                    matrix[i._index][j._index] = pathcost
        return matrix

    def defaultRandomTour(self, time_allowance=60.0):
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None
        start_time = time.time()
        while not foundTour and time.time() - start_time < time_allowance:
            # create a random permutation
            perm = np.random.permutation(ncities)
            route = []
            # Now build the route using the random permutation
            for i in range(ncities):
                route.append(cities[perm[i]])
            bssf = TSPSolution(route)
            count += 1
            if bssf.cost < np.inf:
                # Found a valid route
                foundTour = True
        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    def greedy(self, time_allowance=60.0):
        start_time = time.time()
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0

        currentSpot = count
        masterMatrix = self.createMatrix(cities)
        path = []
        cityMatrix = np.array(copy.deepcopy(masterMatrix))
        cityMatrix[0, :] = float('inf')
        for city in cities:
            path.append(currentSpot)  # add first spot

            # what if all infinity?
            min_in_column = np.min(cityMatrix, axis=0)
            min_index_column = np.argmin(cityMatrix, axis=0)
            min_spot = min_index_column[currentSpot]
            cityMatrix[currentSpot][min_spot] = float('inf')
            cityMatrix[:, currentSpot] = float('inf')
            cityMatrix[min_spot, :] = float('inf')

            currentSpot = min_spot

        route = []
        for i in range(ncities):
            route.append(cities[path[i]])

        bssf = TSPSolution(route)

        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else float('inf')
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None

        return results

    def ReduceMatrix(self, matrix: np.array) -> (int, np.array):
        bound = 0
        reduced_row_matrix = []
        reduced_col_matrix = []

        for row in matrix:
            minimum = min(row)
            if minimum != float('inf'):
                assert (minimum >= 0)
                bound += minimum
                reduced_row_matrix.append(row - minimum)

        for column in np.array(reduced_row_matrix).T:
            minimum = min(column)
            if minimum != float('inf'):
                assert (minimum >= 0)
                bound += minimum
                reduced_col_matrix.append(column - minimum)

        return bound, np.array(reduced_col_matrix).T

    def branchAndBound(self, time_allowance=60.0):
        start_time = time.time()
        results = {}
        # greedy = self.greedy()
        default_tour = self.defaultRandomTour()
        lowest_cost = default_tour['cost']
        num_updates = 0
        max_heap_len = 1
        pruned = 0
        total = 1
        num_sul = 0
        count = 0
        foundTour = False
        bssf = default_tour['soln'] # update if we find a solution better than the current BSSF

        cities = self._scenario.getCities()

        heap = []
        heapq.heapify(heap)

        masterMatrix = self.createMatrix(cities)
        mutationMatrix = np.array(copy.deepcopy(masterMatrix))
        cities = self._scenario.getCities()

        # create a Node with first reduced matrix -> this is where we start
        # push Node onto heap
        # make sure it is sorted by the bound set heapq.heappush(heap,(my_node.bound, my_node))
        init_bound, mutationMatrix, = self.ReduceMatrix(mutationMatrix)
        init_node = Node(cities[0], mutationMatrix, init_bound, cities[1:], path)
        heapq.heappush(heap, (init_node.bound, init_node))
        path.append(init_node.current_city)

        while len(heap) and time.time() - start_time < time_allowance:
            # pop heap and expand it
            currentNode = heapq.heappop(heap)[1]
            if currentNode.bound > bssf._costOfRoute():
                pruned += 1
                continue

            for city in currentNode.remaining_cities:
                matrix = currentNode.RCM  # todo deepcopy, pointer
                matrix[currentNode.current_city._index, :] = float('inf')
                matrix[:, city._index] = float('inf')
                bound, matrix = self.ReduceMatrix(matrix)
                current_path = path.copy()
                current_path.append(city)
                node = Node(city, matrix, bound, currentNode.remaining_cities.remove(city), current_path) # FIXME path parameter is whack
                total += 1
                heapq.heappush(heap, (node.bound, init_node))
                path = current_path  #only if solution better than current BSsf
                count += 1


        end_time = time.time()
        bssf = TSPSolution(path)

        results['cost'] = bssf.cost
        results['time'] = end_time - start_time
        results['count'] = count  # the number of single candidate solutions better than the last
        results['soln'] = bssf
        results['max'] = None  # max queue size
        results['total'] = None # total number of nodes created
        results['pruned'] = pruned

        return results

    def fancy(self, time_allowance=60.0):
        pass

    def setupWithScenario(self, scenario):
        self._scenario = scenario


class Node:
    def __init__(self,
                 current_city=None,
                 RCM=None,
                 bound=None,
                 remaining_cities=None,
                 path=None):
        self.current_city = current_city
        self.RCM = RCM
        self.bound = bound
        self.remaining_cities = remaining_cities
        self.path = path

    def __lt__(self, other):
        if self.bound < other.bound:
            return True
        else:
            return False
