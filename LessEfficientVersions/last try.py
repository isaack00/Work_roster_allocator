def allocate(preferences, officers_per_org, min_shifts, max_shifts):
    """
		Function description: given a list of workers, with indivudal shift preferences and a list of jobs, with workers required. gives an allocation of where each worker should work

		Approach description: Create a network, source connects to first lot of shifts, and second lot of shifts. These lots represent the min shifts and the max-min shifts (remaining shifts)
        these then connect to the workers, and the workers connect to a set of 30 days, each worker has their own 30 days. Each of the 30 days connects to a day-shift (eg day1 shift 3) given the preferences of the workers
        Each day shift then connects to a single job, as i compiled jobs into 1 thing since they are the same really its shifts that matter. then this job lead to the sink. 
        edge capacity for worker to day is 1 since they can only work once a day, and the edge capacity from worker-day to day-shift is also 1 cos still they can only work once a day. from day-shift to job is an edge capacity equal to how many people are needed at that shift on that day
        the job to the sink is equal to the total amount of workers needed in a day *30. Source to min shifts node is equal to the minmum shifst * workers, and then that connects to the workers with the edge capacity of min shifts
        source connects to remiainng shifts with edge capacity equal to the remianing shifts *30 then to each worker with capacity of reaminingshifts.
        Run ford fulkerson from min shifst edge to sink, then from remaing shift to sink, then from there the residual can be read as the max flow has been found. Also check for everything that needs to be checked along the way, such as if min shifts has been met, and if a allocation is even possible.

		Input: 
			preferences: list of workers and their shift preferences
            officers_per_org: the jobs and how much workers they require in each shift
            min shifts: the minimum amount of shifts each worker should recieve
            Max shifts: the maximum amount of shifts a worker can recieve
		
		Output: big list, each index represtents a worker, each index of that index represents a job, each index of that index represents a day and each index of that index represetns a shift
		
		Time complexity: o(E*Fmax + N*E) where E is workers and fmax is the max flow (less than /equal to workers per a day), n is job

		Time complexity analysis : E*Fmax is simply the fulkerson, then n for jobs constasnt times (including the while loop), constant times there is E for workers. there is also a job*worker, where the while loop is. So E*Fmax + contant*E + constant*N + N*E*constant = E*Fmax +N*E
        Why ford fulkerson instead of EDumond: This is always less than worker*worker*job. There is an if statment that stops the function and returns none if there are less workers thatn shifts in a day.
        This means that when a ford fulkerson is done, it will always have a max flow that is less than worker. 
        Edmond karp would be better where there are less workers than shifts, but since there is an if statment that will cut off this off, as less workers than shifts in a day is impossible.
        But since flow is taken from the amount of workers needed for a day, it will at most be equal to workers. 
        Edges = worker + worker*30 + 30*90 + 2
        vertex = worker + 2 + 30*worker +30*3 + 1 
        edmond would be: worker^2*constants
        ford fulkerson would be: worker*maxFlow. at worst, max flow is equal to worker (constants for both have been removed), because we could if we have not enough workers for a day, it will end the function before the fulkerson. But if there is enough workers, then it will go through with the ford fulkerson, and the max flow will
        be the amount of workers needed in a day, which is either equal to or less than workers in total. cos otherwise itd be impossible, so it premature cuts off. 
        

		Aux Space complexity: O(n*e),  where n is jobs and e is workers

		Aux Space complexity analysis: the allocation array is by far the biggest thing, and is Workers*30*3*jobs, so basically worker*jobs, which is e*n. everyting else is just e size r j size, or constant
		
	"""
    total_per_shift = [0,0,0]
    
    for i in range(len(officers_per_org)):
        total_per_shift[0] += officers_per_org[i][0]
        total_per_shift[1] += officers_per_org[i][1]
        total_per_shift[2] += officers_per_org[i][2]

    if sum(total_per_shift)*30 > len(preferences)*max_shifts:
        return None
    allocations = [[[[0,0,0] for k in range(30)] for i in range(len(officers_per_org))] for j in range(len(preferences))]  
    
    day_shift_graph = [[0 for i in range(len(preferences) + 2 + 30*len(preferences) + 3*30 +3)] for j in range(len(preferences) + 2 + 30*len(preferences) + 3*30 +3)]
    
    
    
    day_shift_graph[0][1] = min_shifts *len(preferences)
    day_shift_graph[0][2] = (max_shifts - min_shifts)*len(preferences)
    for i in range(len(preferences)):
        day_shift_graph[1][i +3] = min_shifts
        day_shift_graph[2][i+3] = max_shifts - min_shifts
        for j in range(30):
            day_shift_graph[i + 3][30*i +len(preferences) + 3 + j] = 1
            if preferences[i][0] == 1:
                day_shift_graph[30*i +len(preferences) + 3 + j][len(preferences)*30 + 3 +len(preferences) + 3*j] = 1
            if preferences[i][1] == 1:
                day_shift_graph[30*i +len(preferences) + 3 + j][len(preferences)*30 + 3 +len(preferences) +1 +3*j] = 1
            if preferences[i][2] ==1:
                day_shift_graph[30*i +len(preferences) + 3 + j][len(preferences)*30 + 3 +len(preferences) +2 +3*j] = 1
    for i in range(30):
        for j in range(1):
            day_shift_graph[30*len(preferences) + 3 + len(preferences) + i*3][30*len(preferences) + 3 + len(preferences) + 90 + j] = total_per_shift[0]
            day_shift_graph[30*len(preferences) + 3 + len(preferences) + i*3 +1][30*len(preferences) + 3 + len(preferences) + 90 + j] = total_per_shift[1]
            day_shift_graph[30*len(preferences) + 3 + len(preferences) + i*3 +2][30*len(preferences) + 3 + len(preferences) + 90 + j] = total_per_shift[2]
            day_shift_graph[len(preferences) + 3 + 30*len(preferences) + 30*3 + j][len(day_shift_graph) - 1] = sum(total_per_shift) * 30
    
    




    
    
    
   
    

    
    
    
    flow1 = ford_fulkerson(day_shift_graph, 1, len(day_shift_graph) - 1)
    
    flow2 = ford_fulkerson(day_shift_graph, 2, len(day_shift_graph) - 1)
    
    

    if flow1 != len(preferences)*min_shifts:
        return None
    if flow1 + flow2 != sum(total_per_shift) *30:
        
        return None
    
    current_job = [[0,0,0], [0,0,0]]
    for i in range(30*3):
        for j in range(len(preferences)):
            for k in range(30):
                if day_shift_graph[3 +len(preferences) + len(preferences)*30 + i][3 + len(preferences) + j*30 + k] == 1:
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



def valid_allocation(allocation, preferences, officers_per_org, min_shifts, max_shifts) -> bool:
    # Calculate total shifts per worker
    worker_shifts = [sum(shift for company in worker for day in company for shift in day) for worker in allocation]
    
    # Check if each worker has a valid number of shifts
    for shifts in worker_shifts:
        if shifts < min_shifts or shifts > max_shifts:
            raise ValueError("Worker has too many or too few shifts")
    
    # Check the allocation of shifts to each company
    num_companies = len(officers_per_org)
    num_days = 30
    num_shifts_per_day = 3
    
    for company in range(num_companies):
        for day in range(num_days):
            for shift in range(num_shifts_per_day):
                desired_shifts = officers_per_org[company][shift]
                total_shifts = sum(allocation[worker][company][day][shift] for worker in range(len(preferences)))
                
                if total_shifts != desired_shifts:
                    raise ValueError("Wrong amount of shifts given to company")
    
    return True

pref = [[1,1,0], [1,1,0], [0,0,1], [1,1,1], [1,0,0], [0,1,0], [1,0,1], [1,1,1]]
org = [[2,3,3]]
minim = 26
max = 30
for i in allocate(pref, org, minim, max):

    print(i)
print(valid_allocation(allocate(pref, org, minim, max), pref, org, minim, max))