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





class OrfFinder:
    

    def __init__(self, genome):
        """
		Function description: This initialises the suffix arrays. which is two cos my approach was to create a normal one for the word, and an inverse one for the word. The forward one is for start and the backward one is for end

		Approach description: Basically creating two suffixes for the same word, one that starts at the start, and one that starts at the end. this is done so that finding a starting sequence can be done easily, as well as this, an ending sequence can be found easily with the reversed suffix

		Input: 
			genome: ABCD type genome, what the full string is
		
		Output: none, just initialises
		
		Time complexity: O(n*n) where is the size of the string

		Time complexity analysis : the algrothim gen_suf is n*n, it is called twice, therefore n*n + n*n, and the reverse is alos n*n, so therefore 3*n*n, which is just n*n

		Space complexity: O(n*n),  where n is the length of the string

		Space complexity analysis: at most, for each indicidual sequence of words, a new list of size 5 is made, say this is for every single formation of the word. then this would still be n*n, since its len amount of 5 elemment arrays for the first, then len-1, then len-2 and so on, until there is no length, all those minus numbers are constant so it is in fact len*len which is n*n for the length of the string
		
	"""
        tree = [0, -1,-1,-1,-1, 0] 
        self.evilTree = [0,-1,-1,-1,-1,0] #base evil tree, which is the reversed
        self.tree = tree #base tree
        self.genome = genome
        self.gen_suf(tree, genome, 0,0, self.tree) #call this function for n*n for len string
        reverse = genome[::-1]#call this function for n*n for len string. this just reverse the string cos thats needed for an reverse suffix
        self.gen_suf(self.evilTree, reverse,0,0, self.evilTree)#call this function for n*n for len string

       
    
    

    def gen_suf(self, cur_depth, genome, i, j, tree):
        """
		Function description: The idea here is to create a function that will recurseively place lists into eleemnts, each list represents a letter, and can link to more letters. so A can link to B and/or C. and if u follow the link to C, then ur got AC. then this C can link to more letters. I used a -1 to represent there no link so far. and dollar signs to show end of link. The most important thing tho is the list at the start, that shows what depth its starts at. eg, ABCDEFG, if we go DEFG, the D list will have a 3, and the D in ABCDEFG will also have a 3, but in a different spot.

		Approach description: Use recursion to place list, each list is 5 elemnts, the last being a dollar sign, the first being a depth indicater and the middle 4 relating to the 4 letters of the albphabet ABCD. it recurses following a link until it finds a -1, or doesnt at all, once at the end, it either adds a list for that letter, with a $, or adds a $ to an existsing list. this shows a sequence ends here

		Input: 
			cur_depth: what level of depth in the list of lists we are
            Genome: genome ABCD
            i: the letter we started on. so say we had ABCD, and we were up to BCD, then i would be 1
            j: the letter we are currently on for the current iteration of suffix. So say we were doing BCD and we were placing C, i would be 2
            tree. the tree that we are performing suffixication on 
		
		Output: none, cos list by reference
		
		Time complexity: O(n*n) where is the size of the string

		Time complexity analysis : this function ends when j has exceeded the end of the string. for this to happen, i has to meet the length of the list an amount of times equal to the length of the list. this basically means i goes through the entire list, the j moves up 1. then i goes from j to the rest of the list, then j moves up again, this keeps going until j has exceeded the entire lsit itself. each iteration of j is done after len - j amount of iteration. so this is effectively the len of the string squared

		aux Space complexity: O(n*n),  where n is the length of the string

		aux Space complexity analysis: a list at most is added for every unique combo, AT MOST there may be n*n unique combos when shortening the suffix by 1. cos if every combo is different, then we have len(string)+(len(string) -1)+(len(string) -2)...+(len(string)-len(string)+1), and all those integers are constant, so its effectively lenstring*lenString
	"""
        if i > len(genome) - 1:
            return
        current = genome[j]
        if current == 'A':
            current = 1
        if current == 'B':
            current = 2
        if current == 'C':
            current = 3
        if current == 'D':
            current = 4
        if cur_depth[current] == -1:
            cur_depth[current] = [[genome[j]], -1,-1,-1,-1, 0]
        cur_depth = cur_depth[current]
        if j == len(genome) - 1:
            cur_depth[5] = '$'
            cur_depth[0].append(len(genome) - (1+j))
            self.gen_suf(tree, genome, i + 1, i + 1, tree)  
        else:
            cur_depth[0].append(len(genome) - (1+j))
            self.gen_suf(cur_depth, genome, i, j + 1, tree)

       
   
    def find(self, start, end):
        """
		Function description: find where the start sequence is in the suffix arrays, both evil and normal. the evil suffix array represents the end, and the normal will be used for finding start

		Approach description: locates where the first instance list of a start and end sequence is, say we have ACBD and start is A and end is C. then it will get the A depth list, and the C list, but for that C list, it will go through an invetsed tree, so D then B then finally C and take that lists depth counter

		Input: 
			Start: the sequence that will be the recurring pattern in all substrings
            end: the sequence that will be consistent acrros all sub strings ends
            
		
		Output: list of all possible sub strings starting with start and ending with start
		
		Time complexity: o(start + end + number of characters in final list)

		Time complexity analysis : so, the two first lines are simply linear for both start and end, this is explained further in that function. 
        When each list is retrived from the function, it gives a list, showing all points on the list where a sequence of start/end is. So we will have two of said lists.
        These lists are naturally ordered, as when inputted the longest substring is inputted then one less and ones less, until the shorted sub tsring is inputted
        Therefore, we can compare the start array to the end array and cut off when a single instance of non compatible start seq location and end seq location start. 
        For example say we have our start array as [1,4,7] (this has been flipped, but there is some o(1) arithemtics to caluclate these)and our end as [9,6,3,2]. 
        it will check that the first eleemnt of start array is bigger than the first eleemnt of end. otherwise, it will terminate the entire function adn return, this is because no other combo will exists, since the integers are oredered.
        then say we are mid check, for example we are up to 4 on the start array. it will get up to 3, see that string location 4->3 is impossible and therefore terminate that loop for 4, since no other combo can be valid since they are ordered.
        Effiectely this creates a time complexity that is o(start + end + number of characters in final list). in simple words, due to the lists being ordered, the algorthim cuts off when the last possible combo is done

		Aux Space complexity: O(len of end + number of characters in final list)

		aux Space complexity analysis: an array is created that output all posible combos, so therefore length of number of characters, end as well cos a reverse end is amde, which is n for size of list
	"""
        start_ar = self.find_alg(self.tree, start, 0)
        end_ar = self.find_alg(self.evilTree, end[::-1], 0)
        count = 0
        if len(end_ar) == 0 or len(start_ar) == 0:
            return []
        final_list = []
        for i in range(1, len(start_ar)):
            if len(self.genome) - start_ar[i] > end_ar[1]:
                break
            for j in range(1, len(end_ar)):

                if (len(self.genome)) - (start_ar[i]) <= end_ar[j]:
                    word = ""
                    for k in range(len(self.genome) - start_ar[i] - len(start), end_ar[j] + len(end)):
                        
                        count = count +1
                        word += self.genome[k]
                    final_list.append(word)
                else:
                    break
                if j != len(end_ar) - 1:
                    if (len(self.genome)) - (start_ar[i]) > end_ar[j + 1]:
                        break
            if i != len(start_ar) - 1:

                if (len(self.genome) - (start_ar[i + 1])) > end_ar[1]:
                    break
                    
            
                
            
        return final_list
    
    def find_alg(self, tree, start, i):
        """
		Function description: just uses recursion to go to the depth of what sequence was erquested, and returns the corresponding string for where that sequence starts

		Approach description: recurse through list of lists using each letter as which next list to go to, when done, either return none cos it dont exist that sequence, or return the array that represents all the locations where the list starts

		Input: 
			tree: the tree which we are recursing through
            start: honestly this is poorly named, it should just be string, it just means the string that we are performing this search on
            i: the index we are up to for that tsring
            
		
		Output: a list that was found in the suffix array, that represents where the start sequence is at in the list
		
		Time complexity: o(n) where n is the length of the string

		Time complexity analysis : it just recurse for each letter in the string, so if the string is ABCD, it would do it 4 times
        
		Aux Space complexity: o(1)

		aux Space complexity analysis: nothing new created, excepted an empty list if not found, otherwise it deos nth, cos the tree is by reference, it already existed
	"""
        if start[i] == 'A':
            char = 1
        if start[i] == 'B':
            char = 2
        if start[i] == 'C':
            char = 3
        if start[i] == 'D':
            char = 4
        
        if tree[char] == -1:
            return []
        if i == len(start) - 1:
            return tree[char][0]
        else:
            return self.find_alg(tree[char], start, i+1)
        
result = allocate([[1,1,0], [1,1,0], [0,0,1], [1,1,1], [1,0,0], [0,1,0], [1,0,1]], [[1,1,1], [1,2,0]], 25,26)
for i in result:
    print(i)