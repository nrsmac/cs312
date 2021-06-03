#!/usr/bin/python3

from PyQt5.QtCore import QLineF, QPointF

import time
import numpy as np
from numpy import copy

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

    ''' <summary>
        This is the entry point for the greedy solver, which you must implement for 
        the group project (but it is probably a good idea to just do it for the branch-and
        bound project as a way to get your feet wet).  Note this could be used to find your
        initial BSSF.
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of best solution, 
        time spent to find best solution, total number of solutions found, the best
        solution found, and three null values for fields not used for this 
        algorithm</returns> 
    '''

    def greedy(self, time_allowance=60.0):
        start_time = time.time()
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None

        currentSpot = count
        masterMatrix = self.createMatrix(cities)
        path = []
        cityMatrix = np.array(copy.deepcopy(masterMatrix))
        cityMatrix[0, :] = float('inf')
        for city in cities:
            path.append(currentSpot)  # add first spot

            # what if all infinity?
            col_min = np.min(cityMatrix, axis=0)
            col_min_index = np.argmin(cityMatrix, axis=0)
            min_spot = col_min_index[currentSpot]
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
            bound += minimum
            assert (minimum >= 0)
            reduced_row_matrix.append(row - minimum)

        for column in np.array(reduced_row_matrix).T:
            minimum = min(column)
            bound += minimum
            assert (minimum >= 0)
            reduced_col_matrix.append(column - minimum)

        return bound, np.array(reduced_col_matrix).T

    def branchAndBound(self, time_allowance=60.0):
        start_time = time.time()
        results = {}
        greedy = self.greedy()
        lowest_cost = greedy['cost']
        num_updates = 0
        max_heap_len = 1
        pruned = 0
        num_sul = 0
        total_created = 0
        bssf = greedy['soln']

        cities = self._scenario.getCities()

        heap = []
        heapq.heapify(heap)

        masterMatrix = self.createMatrix()
        mutationMatrix = copy.deepcopy(masterMatrix)

        cities = self._scenario.getCities()
        # Create master matrix
        # Copy master matrix into a matrix you can mutate
        # Call your reduction function on matrix

        path = []
        # create a node with first reduced matrix -> this is where we start
        # push node onto heap
        # make sure it is sorted by the bound set heapq.heappush(heap,(my_node.bound, my_node))

        while len(heap) and time.time() - start_time < time_allowance:
            # pop heap and expand it
            # if you make it, all remaining cities you can access from this city
            # check node out of class
            # check if bound is less than your current lowest cost
            # start expanding, pruning, all bnb stuff
            # (maybe a helper to reduce matrix based on next city / path to take)
            # ReduceMatrix will reduce the whole matrix and wont help you again. make another
            # ReduceMatrix only reduces for the path
            pass



    def fancy(self, time_allowance=60.0):
        pass

    def setupWithScenario(self, scenario):
        self._scenario = scenario
