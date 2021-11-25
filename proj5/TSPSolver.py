#!/usr/bin/python3

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

    def branchAndBound(self, time_allowance=60.0):
        results = {}
        cities = self._scenario.getCities()
        n_cities = len(cities)
        foundTour = False
        start_index = 0
        bssf = State(math.inf, None, "")
        start_time = time.time()
        pruned = 0
        count = 0
        max_heap_size = 0

        initial_matrix, initial_lb = generate_initial_matrix(cities)
        s_0 = State(initial_lb, initial_matrix, [0])
        heap = [s_0]
        heapq.heapify(heap)

        while len(heap):
            s_n = heapq.heappop(heap)
            if s_n.cost < bssf.cost:  # Expand
                cities_not_visited = [city for city in cities if city._index not in s_n.path]
                for city in cities_not_visited:  # Create matrices for cities not yet visited
                    s_i = travel(s_n, city._index, bssf.cost)
                    if s_i.cost < bssf.cost and len(s_i.path) == n_cities:
                        bssf = s_i
                        count += 1
                        foundTour = True
                    elif s_i.cost < bssf.cost:
                        heapq.heappush(heap, s_i)
                        if max_heap_size > len(heap): max_heap_size = len(heap)
                    else:
                        pruned += 1
            else:
                pruned += 1

        solution_cities = []
        for city_index in bssf.path:  # Get cities from bssf list of indices
            solution_cities.append(cities[city_index])

        solution = TSPSolution(solution_cities)
        solution.cost = bssf.cost

        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['soln'] = solution
        results['max'] = None
        results['total'] = None
        results['count'] = count
        results['pruned'] = pruned
        return results


def generate_initial_matrix(cities):  # Returns lb and reduced matrix
    n_cities = len(cities)
    matrix = np.empty((n_cities, n_cities))
    matrix.fill(np.inf)
    for from_index, from_city in enumerate(cities):
        for to_index, to_city in enumerate(cities):
            if from_index != to_index:
                dist = from_city.costTo(to_city)
                matrix[from_index, to_index] = dist

    return reduce_matrix(matrix)


def reduce_matrix(matrix):
    # Reduce by row
    residual = 0
    for i in range(len(matrix)):
        min_value = min(matrix[i])  # min of row
        if min_value != 0 and min_value != math.inf:
            matrix[i] = matrix[i] - min_value
            residual += min_value
    # Reduce by column
    matrix = matrix.T
    for j in range(len(matrix)):
        min_value = min(matrix[j])  # min of col
        if min_value != 0 and min_value != math.inf:
            matrix[j] = matrix[j] - min_value
            residual += min_value
            matrix = matrix.T
    return matrix, residual


def travel(S: State, dest: int, bssf_cost):
    src = int(S.path[-1])
    new_matrix = S.matrix.copy()
    new_matrix[src] = np.array([math.inf] * len(S.matrix))
    new_matrix[:, dest] = np.array([math.inf] * len(S.matrix))
    new_matrix[dest, src] = math.inf

    new_matrix, new_cost = reduce_matrix(new_matrix)
    new_cost += S.cost
    new_path = S.path.copy()
    new_path.append(dest)

    return State(new_cost, new_matrix, new_path)
