def allocate(preferences, officers_per_org, min_shifts, max_shifts):

    total_size = 2
    total_size += len(preferences)
    total_size += len(officers_per_org) * 3
    graph = [[0 for i in range(total_size)] for j in range(total_size)]
    total_per_shift = [0,0,0]
    for i in range(1, len(preferences)+ 1):
        graph[0][i] = max_shifts
    for i in range(len(preferences)):
        if preferences[i][0] == 1:
            for j in range(len(officers_per_org)):
               graph[1 + i][len(preferences) + 3*j + 1] = 30 
        if preferences[i][1] == 1:
            for j in range(len(officers_per_org)):
               graph[1 + i][len(preferences) + 3*j + 2] = 30 
        if preferences[i][2] == 1:
            for j in range(len(officers_per_org)):
               graph[1 + i][len(preferences) + 3*j + 3] = 30 

    for i in range(len(officers_per_org)):
        graph[len(preferences) + 1 + i*3][len(graph) - 1] = officers_per_org[i][0] * 30
        total_per_shift[0] += officers_per_org[i][0]
        graph[len(preferences) + 1 + i*3 + 1][len(graph) - 1] = officers_per_org[i][1] * 30
        total_per_shift[1] += officers_per_org[i][1]
        graph[len(preferences) + 1 + i*3+2][len(graph) - 1] = officers_per_org[i][2] * 30
        total_per_shift[2] += officers_per_org[i][2]
    for i in graph:
        print(i)
    allocations = [[[[0,0,0] for k in range(30)] for i in range(len(officers_per_org))] for j in range(len(preferences))]
    flow = ford_fulkerson(graph, 0, len(graph) - 1)
    employee_status = [0 for i in range(len(preferences))]
    job_filled = [[0 for i in range(len(officers_per_org) * 3)] for j in range(30)]
    
    for job_shifts in range(len(preferences) + 1, len(graph) - 1):
        current = 0
        for worker in range(1, len(preferences) + 1):
            current += employee_status[worker - 1]
            for day in range(graph[job_shifts][worker]):
                allocations[worker - 1][int((job_shifts - 1 -(len(preferences)))/3)][((current) + employee_status[worker - 1]) %30][(job_shifts - len(preferences) - 1) % 3] = 1
                current += 1            
            employee_status[worker - 1] += graph[job_shifts][worker]


    day_shift_graph = [[0 for i in range(len(preferences) + 2 + 30*len(preferences) + 3*30 +len(officers_per_org)*3)] for j in range(len(preferences) + 2 + 30*len(preferences) + 3*30 +len(officers_per_org)*3)]
    
    
    for i in range(len(preferences)):
        day_shift_graph[0][i +1] = max_shifts
        for j in range(30):
            day_shift_graph[i + 1][30*i +len(preferences) + 1 + j] = 1
            if preferences[i][0] == 1:
                day_shift_graph[30*i +len(preferences) + 1 + j][len(preferences)*30 + 1 +len(preferences) + 3*j] = 1
            if preferences[i][1] == 1:
                day_shift_graph[30*i +len(preferences) + 1 + j][len(preferences)*30 + 1 +len(preferences) +1 +3*j] = 1
            if preferences[i][2] ==1:
                day_shift_graph[30*i +len(preferences) + 1 + j][len(preferences)*30 + 1 +len(preferences) +2 +3*j] = 1
    for i in range(30):
        for j in range(len(officers_per_org)):
            day_shift_graph[30*len(preferences) + 1 + len(preferences) + i*3][30*len(preferences) + 1 + len(preferences) + 90 + j +0] = total_per_shift[0]
            day_shift_graph[30*len(preferences) + 1 + len(preferences) + i*3 +1][30*len(preferences) + 1 + len(preferences) + 90 + j +1] = total_per_shift[1]
            day_shift_graph[30*len(preferences) + 1 + len(preferences) + i*3 +2][30*len(preferences) + 1 + len(preferences) + 90 + j +2] = total_per_shift[2]
            day_shift_graph[len(preferences) + 1 + 30*len(preferences) + 30*3 + j + 0][len(day_shift_graph) - 1] = total_per_shift[0] * 30
            day_shift_graph[len(preferences) + 1 + 30*len(preferences) + 30*3 + j+1][len(day_shift_graph) - 1] = total_per_shift[1] * 30
            day_shift_graph[len(preferences) + 1 + 30*len(preferences) + 30*3 + j+2][len(day_shift_graph) - 1] = total_per_shift[2] * 30
    
    
    ford_fulkerson(day_shift_graph, 0, len(day_shift_graph) - 1)
    for i in day_shift_graph:
        print(i)
    for i in range(30*3):
        for j in range(len(preferences)):
            for k in range(30):
                if day_shift_graph[1 +len(preferences) + len(preferences)*30 + i][1 + len(preferences) + j*30 + k] == 1:
                   

                    print("employee " + str(j) + " is working shift " + str(i%3) + " on day " + str(k))
                
                

    print(len(day_shift_graph))
    [1,1,1]
    [0,0,1]
    [1,0,1]


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



pref = [[1,1,1],
        [1,1,1],
        [1,1,1],
        [1,1,1],
        [1,1,1],
        [1,1,1]]
        

officer_per = [[1,1,1],
               [1,0,0]]


a = allocate(pref, officer_per, 0, 25)
