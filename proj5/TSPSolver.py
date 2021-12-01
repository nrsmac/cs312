#!/usr/bin/python3
from copy import deepcopy

from which_pyqt import PYQT_VER
import numpy as np

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time
import numpy as np
from TSPClasses import *
from State import State
import heapq
import itertools


class TSPSolver:
    def __init__(self, gui_view):
        self._scenario = None

    def setupWithScenario(self, scenario):
        self._scenario = scenario

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

    def greedy_bssf(self, time_allowance=60.0):
        cost = 0
        path_of_cities = []
        path = []
        cities = self._scenario.getCities()
        current = cities[0]

        while len(path_of_cities) < len(cities):
            min_neighbor = None
            min_cost = math.inf
            for city in cities:
                neighbor_cost = current.costTo(city)
                if city not in path_of_cities and neighbor_cost < min_cost:
                    min_neighbor = city
                    min_cost = neighbor_cost
            current = min_neighbor
            path_of_cities.append(current)
            path.append(current._index)
            cost += min_cost

        return State(cost, None, path)  # Not returning a matrix, irrelevant

    def branchAndBound(self, time_allowance=60.0):
        results = {}  # Initializing variables
        cities = self._scenario.getCities()
        n_cities = len(cities)
        start_index = 0
        start_time = time.time()
        pruned = 0
        count = 0
        total = 1  # Starting with initial node
        max_heap_size = 0

        bssf = self.greedy_bssf(cities)

        initial_matrix, initial_lb = generate_initial_matrix(
            cities)  # Generate a reduced adjacency matrix & lower bound

        s_0 = State(initial_lb, initial_matrix, [0])  # s_0 is the initial matrix

        heap = [s_0]  # Push initial value to heap
        heapq.heapify(heap)

        while len(heap) and time.time() - start_time < time_allowance:  # While our heap is not empty
            s_n = heapq.heappop(heap)  # s_n <- heap.pop(), O(log n)
            if s_n.get_h() < bssf.get_h():  # Expand s_n
                cities_not_visited = [city for city in cities if city._index not in s_n.path]
                for city in cities_not_visited:  # Create matrices for cities not yet visited
                    s_i = travel(s_n, city._index)  # s_i is a neighbor of s_n
                    total += 1
                    if s_i.cost < bssf.cost and len(s_i.path) == n_cities:  # we found a less costly leaf node
                        bssf = s_i  # Set our best solution to be s_i
                        count += 1
                    elif s_i.cost < bssf.cost:  # we found a less costly solution, but not a leaf node
                        heapq.heappush(heap, s_i)  # O(log n)
                    else:  # we found a more costly solution, time to prune
                        pruned += 1

                    if len(heap) > max_heap_size:
                        max_heap_size = len(heap)
            else:
                pruned += 1

        solution_cities = []
        for city_index in bssf.path:  # Get cities from bssf list of indices
            solution_cities.append(cities[city_index])

        solution = TSPSolution(solution_cities)
        solution.cost = bssf.cost
        TSPSolver._bssf = solution
        end_time = time.time()
        results['cost'] = bssf.cost
        results['time'] = end_time - start_time
        results['soln'] = solution
        results['max'] = max_heap_size
        results['total'] = total
        results['count'] = count
        results['pruned'] = pruned
        return results


def generate_initial_matrix(cities):  # Returns lb and reduced matrix from a list of cities, O(n^2)
    n_cities = len(cities)
    matrix = np.empty((n_cities, n_cities))
    matrix.fill(np.inf)
    for from_index, from_city in enumerate(cities):
        for to_index, to_city in enumerate(cities):
            if from_index != to_index:
                dist = from_city.costTo(to_city)
                matrix[from_index, to_index] = dist

    return reduce_matrix(matrix)


def reduce_matrix(matrix):  # O(n^2), linear subtraction n times
    # Reduce by row
    cost = 0
    for i in range(len(matrix)):  # O(n)
        min_value = min(matrix[i])  # min of row
        if min_value != math.inf:
            matrix[i] = matrix[i] - min_value  # O(n)
            cost += min_value

    # Reduce by column
    for j in range(len(matrix)):  # O(n)
        min_value = min(matrix.T[j])  # min of col
        if min_value != math.inf:
            matrix.T[j] = matrix.T[j] - min_value
            cost += min_value

    return matrix, cost


def travel(S: State, dest: int):  # Given a state, expand to given destination. O(n)
    src = int(S.path[-1])
    new_matrix = S.matrix.copy()
    new_cost = new_matrix[src,dest]
    new_matrix[src] = np.array([math.inf] * len(S.matrix))  # Infinity out the source row
    new_matrix[:, dest] = np.array([math.inf] * len(S.matrix))  # Infinity out the destination column
    new_matrix[dest, src] = math.inf  # Infinity out dest -> src

    new_matrix, n = reduce_matrix(new_matrix)  # O(n)
    new_cost += n + S.cost
    new_path = S.path.copy()
    new_path.append(dest)

    return State(new_cost, new_matrix, new_path)
