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

from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class TSPSubtask:
    priority: int
    item: Any=field(compare=False)


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

    '''
    Cheapest Insertion also begins with two cities.
    It then finds the city not already in the tour that when placed between two connected cities in the subtour will
    result in the shortest possible tour.
    It inserts the city between the two connected cities, and repeats until there are no more insertions left.

    - Start from a random city.
    - Find the city which insertion in the tour causes the smallest increase in length,
        i.e the city k which minimizes d(i, k)  + d(k, j) - d(i, j) with (i, j) an edge in the partial tour.
    - Insert k between i and j.
    - Repeat until every city has been visited.
    '''
    def fancy(self, time_allowance=60.0):
        cities = list(self._scenario.getCities())

        # # Track time
        start_time = time.time()
        end_time = time.time()

        # P = [] # Path
        # V = cities.copy()  # Cities list
        # Z = 0  # Cost?

        # Psuedocode from Saturday night.

        # Initialization -- arbitrarily choose first vertex 'r'. Tour P = [r], Z=0
        # While |P| < |V| (while path is incomplete)
            # For each vertex i in V not in P, find the cheapest insertion between any j and k in P; and neighboring in P
                # * Use a Priority Queue to find cheapest insertion
            # find vertex i* in V not in P that can be inserted the cheapest;
            # insert i* at cheapest position j* and k*
            # P = {r, ..., j*, i*, k*,...} and set
            # Z = Z - (c_(j*k*) + c_(j*i*) + c_(i*k*))


        # Cheapest Insertion (John's version)
        # =================================================
        # Start with one point
        # While path incomplete:
            # For each eligible root node r (start with last point added, allow up to n neighbors)
            # (skip the neighbors part for now and just allow all nodes)
                # For each node NOT in the path j
                    # For each node NOT in the path k (that is not j)
                        # Try connecting r to j, j to k and k to r - measure total path length
                        # Save if min
            # Apply solution

        iterations = 0

        firstNode = cities[0]
        remainingCities = cities.copy()
        remainingCities.remove(firstNode)
        state = {
            "path": [ firstNode ],
            "remaining": remainingCities,
            "sol": None, # A TSP Solution will later go here.
            "cost": np.inf
        }
        while len(state["path"]) < len(cities): # While path is incomplete
            # Iterate backwards through the current path
            # We could hypothetically limit this to n possiblities to make the algo faster.
            minState = {
                "cost": np.inf
            }
            # Try to find the lowest possible state that can result from another edge added.
            for R in reversed(state["path"]): # Runs 1..n times (n/2 on average)
                # Go through every possible edge (pair of nodes)
                # Note: this does consider every edge forwards and backwards,
                # which is inefficient on easy (symmetrical) mode,
                # but exactly what we want for hard (asym) mode
                for j in state["remaining"]: # Runs n..1 times
                    for k in state["remaining"]: # Runs n..1 times
                        if j == k: continue # Ignore the instance where they're the same
                        # Consider the new edges: r->j, j->k, k->r (k->r is actually implied; we don't actually add it)
                        # R won't always be the last node added. We need to figure
                        # out what position it's at in the path so that we can insert j,k after it.
                        newPath = state["path"].copy()
                        rIndex = newPath.index(R) + 1
                        newPath.insert(rIndex, j)
                        newPath.insert(rIndex+1, k)
                        newSol = TSPSolution(newPath)
                        if newSol.cost < minState["cost"]:
                            # We found a new "lowest" newState
                            # Store a bunch of info about it
                            newRemaining = state["remaining"].copy()
                            newRemaining.remove(j)
                            newRemaining.remove(k)
                            minState = {
                                "path": newPath,
                                "remaining": newRemaining,
                                "cost": newSol.cost,
                                "sol": newSol
                            }
                        # Otherwise, just let the iteration end
                        # so the next combination can be tried.

                        # This is just to figure out the time complexity - remove later
                        iterations += 1

            # Once all possibilities of R, j and k have been tried,
            # The state becomes the minState and we go on to add the next node.
            if minState["cost"] == np.inf:
                raise Exception("Got stuck; no paths left at this point.")
            state = minState

            print("Finished an iteration. Path is now:",[str(x) for x in state["path"]],"and cost is now:",state["cost"])


        print("Total iterations of inner-most loop:",iterations)

        # solution = TSPSolution(P)
        solution = state["sol"]
        cost = state["cost"]
        return {
            'cost': cost,
            'time': end_time - start_time,
            'count': 1,
            'soln': solution,
            'max': None,
            'total': None,
            'pruned': None
        }

    def greedy(self, time_allowance=60.0):
        # Track time
        start_time = time.time()
        # Init variables before starting.
        numCities = len(self._scenario.getCities())
        count = 0
        bssf = None

        for i in range(numCities):
            if time.time() - start_time >= time_allowance:
                break

            cities = list(self._scenario.getCities())
            start = cities.pop(i)
            route = [start]
            while len(cities):
                nextCity = None
                shortestPath = np.inf
                for city in cities:
                    dist = route[-1].costTo(city)
                    if dist < shortestPath:
                        shortestPath = dist
                        nextCity = city
                if shortestPath == np.inf:
                    break
                route.append(nextCity)
                cities.remove(nextCity)

            if len(route) == numCities:
                # Found a solution
                sol = TSPSolution(route)
                count += 1
                if bssf is None or sol.cost < bssf.cost:
                    bssf = sol

        end_time = time.time()

        return {
            'cost': bssf.cost if bssf else None,
            'time': end_time - start_time,
            'count': count,
            'soln': bssf,
            'max': None,
            'total': None,
            'pruned': None
        }

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
