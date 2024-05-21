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
        Effiectely this creates a time complexity that is o(start + end + number of characters in final list + number of different sub strings), since number of sub strings will always be less than or equal to length of total sub stringsm and will be out sized by the sub string size by a lot, it is o(start + end + characters in list)

		Aux Space complexity: O(len of end + number of characters in final list)

		aux Space complexity analysis: an array is created that output all posible combos, so therefore length of number of characters, end as well cos a reverse end is amde, which is n for size of list
	"""
        start_ar = self.find_alg(self.tree, start, 0)
        end_ar = self.find_alg(self.evilTree, end[::-1], 0)

        if len(end_ar) == 0 or len(start_ar) == 0:
            return []
        final_list = []
        for i in range(1, len(start_ar)):
            if len(self.genome) - start_ar[i] > end_ar[1]:
                break
            for j in range(1, len(end_ar)):
                if len(self.genome) - start_ar[i] > end_ar[j]:
                    break

                if (len(self.genome)) - (start_ar[i]) <= end_ar[j]:
                    word = ""
                    for k in range(len(self.genome) - start_ar[i] - len(start), end_ar[j] + len(end)):
                        word += self.genome[k]
                    final_list.append(word)
            
                
            
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
        




a = OrfFinder("ABAABCBA")
print(a.find('A', 'BA')) 
print(a.find('A', 'A'))  
print(a.find('A', 'B'))   
