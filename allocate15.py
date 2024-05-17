def allocate(preferences, officers_per_org, min_shifts, max_shifts):
    import copy
    total_per_shift = [0,0,0]
    for i in range(len(officers_per_org)):
        total_per_shift[0] += officers_per_org[i][0]
        total_per_shift[1] += officers_per_org[i][1]
        total_per_shift[2] += officers_per_org[i][2]
    total_size = 2
    total_size += len(preferences)
    total_size += 1 * 3

    allocations = [[[[0,0,0] for k in range(30)] for i in range(len(officers_per_org))] for j in range(len(preferences))]  
    
    day_shift_graph = [[0 for i in range(len(preferences) + 2 + 30*len(preferences) + 3*30 +1)] for j in range(len(preferences) + 2 + 30*len(preferences) + 3*30 +1)]
    
    for i in range(len(preferences)):
        day_shift_graph[0][i +1] = max_shifts - min_shifts
        for j in range(30):
            day_shift_graph[i + 1][30*i +len(preferences) + 1 + j] = 1
            if preferences[i][0] == 1:
                day_shift_graph[30*i +len(preferences) + 1 + j][len(preferences)*30 + 1 +len(preferences) + 3*j] = 1
            if preferences[i][1] == 1:
                day_shift_graph[30*i +len(preferences) + 1 + j][len(preferences)*30 + 1 +len(preferences) +1 +3*j] = 1
            if preferences[i][2] ==1:
                day_shift_graph[30*i +len(preferences) + 1 + j][len(preferences)*30 + 1 +len(preferences) +2 +3*j] = 1
    for i in range(30):
        for j in range(1):
            day_shift_graph[30*len(preferences) + 1 + len(preferences) + i*3][30*len(preferences) + 1 + len(preferences) + 90 + j] = total_per_shift[0]
            day_shift_graph[30*len(preferences) + 1 + len(preferences) + i*3 +1][30*len(preferences) + 1 + len(preferences) + 90 + j] = total_per_shift[1]
            day_shift_graph[30*len(preferences) + 1 + len(preferences) + i*3 +2][30*len(preferences) + 1 + len(preferences) + 90 + j] = total_per_shift[2]
            day_shift_graph[len(preferences) + 1 + 30*len(preferences) + 30*3 + j][len(day_shift_graph) - 1] = sum(total_per_shift) * 30 - min_shifts*len(preferences)
    





    min_shifts_graph = copy.deepcopy(day_shift_graph)
    min_shifts_graph[len(preferences) + 1 + 30*len(preferences) + 30*3][len(day_shift_graph) - 1] = min_shifts * 30
    for i in range(len(preferences)):
        min_shifts_graph[0][i +1] = min_shifts
    
    min_shifts_flow = ford_fulkerson(min_shifts_graph, 0, len(day_shift_graph) - 1)
    for i in min_shifts_graph:
        print(i)

    for i in range(30*3):
        for j in range(len(preferences)):
            for k in range(30):
                if min_shifts_graph[1 +len(preferences) + len(preferences)*30 + i][1 + len(preferences) + j*30 + k] == 1:
                    day_shift_graph[1 + j][1 +len(preferences) + j*30 + k] = 0
                    day_shift_graph[1 +len(preferences) +len(preferences)*30 + i][1 +len(preferences) +len(preferences)*30 + 30*3] -= 1



    
    flow = ford_fulkerson(day_shift_graph, 0, len(day_shift_graph) - 1)
    print(flow, min_shifts_flow)
    if flow + min_shifts_flow != sum(total_per_shift) *30:
        return None
    for i in range(len(preferences)):
        if min_shifts_graph[1 + i][0] != min_shifts:
            return None
    current_job = [[0,0,0], [0,0,0]]
    for i in range(30*3):
        for j in range(len(preferences)):
            for k in range(30):
                if min_shifts_graph[1 +len(preferences) + len(preferences)*30 + i][1 + len(preferences) + j*30 + k] == 1 or day_shift_graph[1 +len(preferences) + len(preferences)*30 + i][1 + len(preferences) + j*30 + k] == 1:
                    
                    if officers_per_org[current_job[1][i%3]][i%3] == current_job[0][i%3]:
                        current_job[1][i%3] += 1
                        current_job[0][i%3] = 0
                        allocations[j][current_job[1][i%3]][k][i%3] = 1
                    else:
                        current_job[0][i%3] +=1
                        allocations[j][current_job[1][i%3]][k][i%3] = 1
        current_job =[[0,0,0], [0,0,0]]

    


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



pref = [[1,0,1],
        [1,1,0],
        [1,0,0],
        [1,1,1],
        [1,1,1],
        [1,1,1],
        [1,1,1],
        [1,1,1],
        [1,0,1],
        


        
        ]
        

officer_per = [[1,0,0]
                ]
               


a = allocate(pref, officer_per, 1, 4)
for i in a:
    print(i)