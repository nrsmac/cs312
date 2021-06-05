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
        heuristic_tour = self.defaultRandomTour()

        bssf = heuristic_tour['soln']

        heap = []
        heapq.heapify(heap)
        cities = self._scenario.getCities()
        master_matrix = self.createMatrix(cities)

        init_bound, init_matrix = self.ReduceMatrix(np.array(copy.deepcopy(master_matrix)))
        init_node = Node(cities[0], init_matrix, init_bound, cities[1:], bssf.route)
        heapq.heappush(heap, (init_node.bound, init_node))

        while len(heap)!=0 and time.time() - start_time < time_allowance:
            current_node = heapq.heappop(heap)[1]
            if len(current_node.remaining_cities) ==

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
