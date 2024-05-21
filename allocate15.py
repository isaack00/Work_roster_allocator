def allocate(preferences, officers_per_org, min_shifts, max_shifts):
    """
		Function description: given a list of workers, with indivudal shift preferences and a list of jobs, with workers required. gives an allocation of where each worker should work

		Approach description: Create 2 networks, one representing the min shifts, and the other representing the rest of the shifts of the workers, since min and max is same for alll
        Each network connects from source to worker, each worker connects to each of their own set of days, each day connects to a day-shift combo (egday1 shift 2) if the worker can work that type of shift.
        each day-shift converges into one single node, this node is representeive of all workers needed for all jobs, across all months. ill mark in the code where each of these done.
        Each edge between source and worker is given for the first grapgh a min shift amount, then ford fulkerson is run on it
        the residual from that ford fulkerson on min shifts grapgh is used and interpreted. as if a worker is working a day and a shift can be gained from the edges connecting day-worker to day-shift.
        the remainingg shifts grapgh is then cahnged to adjust for the residual of min shifts, eg if worker 1 worked day 2 in his min shifts, then cross out day 2 for the reamining days for that worker. also removed 1 less worker needed for a shift on a certain day if a worker fills it
        check that the flows add up to total workers needed in a day *30.
        allocate by using a system that checks if a job is full and adds to it if not

        

		Input: 
			preferences: list of workers and their shift preferences
            officers_per_org: the jobs and how much workers they require in each shift
            min shifts: the minimum amount of shifts each worker should recieve
            Max shifts: the maximum amount of shifts a worker can recieve
		
		Output: big list, each index represtents a worker, each index of that index represents a job, each index of that index represents a day and each index of that index represetns a shift
		
		Time complexity: o(E*Fmax + N*E) where E is workers and fmax is the max flow (workers per a day * 30), n is job

		Time complexity analysis : E*Fmax is simply the fulkerson, then n for jobs constasnt times (including the while loop), constant times there is E for workers. there is also a job*worker, where the while loop is. So E*Fmax + contant*E + constant*N + N*E*constant = E*Fmax +N*E
        This is always less than worker*worker*job. There is an if statment that stops the function and returns none if there are less workers thatn shifts in a day.
        This means that when a ford fulkerson is done, it will always have a max flow that is less than worker. 
        Edmond karp would be better where there are less workers than shifts, but since there is an if statment that will cut off this off, as less workers than shifts in a day is impossible.
        But since flow is taken from the amount of workers for a day, it will at least be equal to workers. 
        Edges = worker + worker*30 + 30*90 + 2
        vertex = worker + 2 + 30*worker +30*3 + 1 
        edmond would be: worker^2
        ford fulkerson would be: worker*maxFlow. at worst, max flow is equal to worker, because we could if we have not enough workers for a day, it will end the function before the fulkerson. But if there is enough workers, then it will go through with the ford fulkerson, and the max flow will
        be the amount of workers needed in a day, which is either equal to or less than workers in total. cos otherwise itd be impossible, so it premature cuts off.

		Aux Space complexity: O(n*e),  where n is jobs and e is workers

		Aux Space complexity analysis: the allocation array is by far the biggest thing, and is Workers*30*3*jobs, so basically worker*jobs, which is e*n. everyting else is just e size r j size, or constant
		
	"""
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
    
    #MOST IMPORTANT LINE TO JUSTIFY FORD FULKERSON

    if sum(total_per_shift)*30 > len(preferences)*max_shifts:
        return None
    
    

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
                    while True:
                        if officers_per_org[current_job[1][i%3]][i%3] == current_job[0][i%3]:
                            current_job[1][i%3] += 1
                            current_job[0][i%3] = 0
                        if officers_per_org[current_job[1][i%3]][i%3] != 0:
                            current_job[0][i%3] +=1
                            allocations[j][current_job[1][i%3]][k][i%3] = 1
                            break
            
        current_job = [[0,0,0],[0,0,0]]

    


    return allocations
    











def ford_fulkerson(graph, start, end):
    """
		Function description: Ford fulkerson with dfs

		Approach description: Countinousy loop and use dfs to find a path, once a path has been found, take the minimum flow from each edge along that path,
        then just simply adjust the flows on teh grapgh, so if the minimum was 15, then we remove 15 from each flow going in the direction to the source, and add to the direction going to the sink
        repeat until no paths found


		Input: 
			graph: matrix which u wanna find on
            start: the starting point of the grpagh
            end: the ending point of the grapgh u want to fidn the flow for
		
		Output: the max flow, but also its taking the list by reference so it changes the grapgh to a residual too
		
		Time complexity: o(E*Fmax) where E is edges and fmax is the max flow 

		Time complexity analysis : theoritcally, with dfs, the flow could be cahnges by 1 everysingle time on the path to reaching max flow, so therefore worst case its fmax. the e is for dfs since thats just E+v but then simplified to e since e is so much more than v

		aux Space complexity: O(v),  where v is the amount of verticies

		aux Space complexity analysis: theoritcally, a path could contain every vertex, so therefore most is v, that is the most as everything else is editing already existsing space. visted + augmented path, which is v + v = v
		
	"""
    def dfs(graph, start, end, path, visted):
        """
		Function description: depth first search for finding paths

		Approach description: recursively find paths with and set done vertexs as visted, keeps going until no paths remain


		Input: 
			grapgh: matrix which u wanna find on
            start: the starting point of the grpagh
            end: the ending point of the grapgh u want to fidn the flow for
            path: the current path, is increased each time a node is visted
            visted: which nodes have been visted in the path finding
		
		Output: A path to the end from the start
		
		Time complexity: o(e)

		Time complexity analysis : At each node, we look at each edge and cycle through every node, so this is e+v. so since e is much larger than v, it becomes e

		aux Space complexity: O(V),  where v is vertex

		aux Space complexity analysis: theortically, each vertex could be visted once, and added to the array for path, meaning in worst case v is length of path
        
	"""
        if start == end:
            return path
        visted[start] = 1

        for i in range(len(graph[start])):
            if visted[i] == 0 and graph[start][i] > 0:



                cur_path = dfs(graph, i, end, path + [(start, i)], visted)
                if cur_path != None:
                    return cur_path
        return None

    current_flow = 0
    while True:
        
        visted = [0] * len(graph)
        aug_path = dfs(graph, start, end, [], visted)
        print(aug_path)
        print("XXX")
        
        
        if aug_path == None:
            break
        bottleneck = float('inf')
        
        for i in range(len(aug_path)):
            bottleneck = min(graph[aug_path[i][0]][aug_path[i][1]], bottleneck)
        
        
        for i in range(len(aug_path)):
            graph[aug_path[i][0]][aug_path[i][1]] -= bottleneck
            graph[aug_path[i][1]][aug_path[i][0]] += bottleneck
        
        
        current_flow += bottleneck
    
    return current_flow



pref = [[0,0,1],
        [0,1,0],
        [1,0,0],
        [1,1,1],
       
        
]
        


   
        


        
        
    

officer_per = [[1,1,1],
               
               

        
               
 



               
                ]
               


a = allocate(pref, officer_per, 22, 25)
for i in a:
   print(i)
