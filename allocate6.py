def allocate(preferences, officers_per_org, min_shifts, max_shifts):

    total_size = 2 + 30
    total_size += len(preferences)
    total_size += len(officers_per_org) * 3
    graph = [[0 for i in range(total_size)] for j in range(total_size)]
    total_per_day = 0
    for i in range((len(officers_per_org))):
        graph[0][i*3 +1] = officers_per_org[i][0] * 30
        graph[0][i*3 + 2] = officers_per_org[i][1] * 30
        graph[0][i*3+3] = officers_per_org[i][2] * 30
        total_per_day += officers_per_org[i][0] + officers_per_org[i][1] + officers_per_org[i][2]
    
    for workers in range(len(preferences)):
        if preferences[workers][0] == 1:
            for shifts1 in range(len(officers_per_org)):
                graph[1 + shifts1*3][len(officers_per_org)*3 + workers +1] = max_shifts
        if preferences[workers][1] == 1:
            for shifts1 in range(len(officers_per_org)):
                graph[2 + shifts1*3][len(officers_per_org)*3 + workers+ 1] = max_shifts
        if preferences[workers][2] == 1:
            for shifts1 in range(len(officers_per_org)):
                graph[3 + shifts1*3][len(officers_per_org)*3 + workers+ 1] = max_shifts
    for i in range(1+len(officers_per_org)*3, 1+len(officers_per_org)*3 + len(preferences)):
        for j in range(30):
            graph[i][j + 1+len(officers_per_org)*3 + len(preferences)] = 1
    for i in range(1+len(officers_per_org)*3 + len(preferences), len(graph) - 1):
        graph[i][len(graph) - 1] = total_per_day
    
    allocations = [[[[0,0,0] for k in range(30)] for i in range(len(officers_per_org))] for j in range(len(preferences))]
    ford_fulkerson(graph, 0, len(graph) - 1)
    


    day_shift_graph = [[0 for i in range(len(preferences)*3 + 2 + 30)] for j in range(len(preferences)*3 + 2 + 30)]
    for i in range(len(preferences)):
        day_shift_graph[0][i*3 + 1] = graph[len(officers_per_org) * 3 + 1 +i][1]
        day_shift_graph[0][i*3 + 2] = graph[len(officers_per_org) * 3 + 1+ i][2]
        day_shift_graph[0][i*3 + 3] = graph[len(officers_per_org) * 3 + 1+i][3]
    for i in range(1, len(preferences)*3 +1):
        for j in range(30):
            day_shift_graph[i][j + len(preferences)*3 +1] = 1
    for i in range(len(preferences)*3 + 1, len(day_shift_graph) - 1):
        day_shift_graph[i][len(day_shift_graph) - 1] = total_per_day

    #ford_fulkerson(day_shift_graph, 0, len(day_shift_graph) - 1)
    print(len(day_shift_graph))
    for i in day_shift_graph:
        print(i)
    print("XXXXXXXXXXXXXXXXXXXX")



    return allocations
    











def ford_fulkerson(graph, source, sink):
    def dfs(graph, source, sink, path, visited):
        if source == sink:
            return path
        visited[source] = True
        for neighbor, capacity in enumerate(graph[source]):
            if not visited[neighbor] and capacity > 0:
                augmenting_path = dfs(graph, neighbor, sink, path + [(source, neighbor)], visited)
                if augmenting_path is not None:
                    return augmenting_path
        return None

    max_flow = 0
    while True:
        # Find an augmenting path using DFS
        visited = [False] * len(graph)
        augmenting_path = dfs(graph, source, sink, [], visited)
        
        # If no augmenting path exists, terminate
        if augmenting_path is None:
            break
        
        # Find the bottleneck capacity along the augmenting path
        bottleneck = min(graph[u][v] for u, v in augmenting_path)
        
        # Update the residual capacities along the augmenting path
        for u, v in augmenting_path:
            graph[u][v] -= bottleneck
            graph[v][u] += bottleneck
        
        # Increment the max flow by the bottleneck capacity
        max_flow += bottleneck
    
    return max_flow



pref = [[0,0,1],
        [0,1,0],
        [1,0,0],
        [1,1,1],]
        

officer_per = [[1,1,1],
               ]


a = allocate(pref, officer_per, 0, 25)
