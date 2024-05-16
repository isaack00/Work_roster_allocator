def allocate(preferences, officers_per_org, min_shifts, max_shifts):
    import copy
    total_size = 2
    total_size += len(preferences)
    total_size += len(officers_per_org) * 3
    graph = [[0 for i in range(total_size)] for j in range(total_size)]
    for i in range(1, len(preferences)+ 1):
        graph[0][i] = 1
    for i in range(len(preferences)):
        if preferences[i][0] == 1:
            for j in range(len(officers_per_org)):
               graph[1 + i][len(preferences) + 3*j + 1] = 1
        if preferences[i][1] == 1:
            for j in range(len(officers_per_org)):
               graph[1 + i][len(preferences) + 3*j + 2] = 1 
        if preferences[i][2] == 1:
            for j in range(len(officers_per_org)):
               graph[1 + i][len(preferences) + 3*j + 3] = 1 

    for i in range(len(officers_per_org)):
        graph[len(preferences) + 1 + i*3][len(graph) - 1] = officers_per_org[i][0]
        graph[len(preferences) + 1 + i*3 + 1][len(graph) - 1] = officers_per_org[i][1]
        graph[len(preferences) + 1 + i*3+2][len(graph) - 1] = officers_per_org[i][2]
    allocations = [[[[0,0,0] for k in range(30)] for i in range(len(officers_per_org))] for j in range(len(preferences))]
    
    employee_status = [0 for i in range(len(preferences))]
    
    for day in range(30):
        graph_new_day = copy.deepcopy(graph)
        for i in range(len(employee_status)):
            if employee_status[i] == max_shifts:
                graph_new_day[0][i + 1] = 0
        ford_fulkerson(graph_new_day, 0, len(graph) - 1)
        for worker in range(1, len(preferences) + 1):
            for job_shifts in range(len(preferences) + 1, len(graph) - 1):
                if graph_new_day[job_shifts][worker] == 1: 
                    allocations[worker - 1][int((job_shifts - (len(preferences) + 1))/3)][day][(job_shifts - len(preferences) - 1) % 3] = 1
                    employee_status[worker - 1] += 1
        

    

    for i in graph:
        print(i)
    print(employee_status)
    for i in graph_new_day:
        print(i)
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
        [1,1,1]]
        

officer_per = [[1,1,1]]


a = allocate(pref, officer_per, 0, 25)
for i in a:
    print(i)