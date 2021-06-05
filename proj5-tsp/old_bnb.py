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
    bssf = default_tour['soln']  # update if we find a solution better than the current BSSF

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
            node = Node(city, matrix, bound, currentNode.remaining_cities.remove(city),
                        current_path)  # FIXME path parameter is whack
            total += 1
            heapq.heappush(heap, (node.bound, init_node))
            path = current_path  # only if solution better than current BSsf
            count += 1

    end_time = time.time()
    bssf = TSPSolution(path)

    results['cost'] = bssf.cost
    results['time'] = end_time - start_time
    results['count'] = count  # the number of single candidate solutions better than the last
    results['soln'] = bssf
    results['max'] = None  # max queue size
    results['total'] = None  # total number of nodes created
    results['pruned'] = pruned

    return results