class OrfFinder:
    

    def __init__(self, genome):
        tree = [0, -1,-1,-1,-1, 0]
        self.tree = tree 
        self.gen_suf(tree, genome, 0,0)
        
        print(self.tree)
       
    
    

    def gen_suf(self, cur_depth, genome, i, j):
        
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
            cur_depth[current] = [genome[j], -1,-1,-1,-1, 0]
        cur_depth = cur_depth[current]
        if j == len(genome) - 1:
            cur_depth[5] = '$'
            self.gen_suf(self.tree, genome, i + 1, i + 1)  
        else:
            self.gen_suf(cur_depth, genome, i, j + 1)

       
   
    def find(self, start, end):
        self.find_alg(self.tree, 0, start, end)
    

    def find_alg(self, layer, i, start, end):
        if start[i] == 'A':
            char = 1
        if start[i] == 'B':
            char = 2
        if start[i] == 'C':
            char = 3
        if start[i] == 'D':
            char = 4
        
        if layer[char] == -1:
            return "FAT FUCKING FAIL"
        




a = OrfFinder("ABCDACD")
a.find('ABC', 'A')
[0, ['A', -1, ['B', -1, -1, ['C', -1, -1, -1, ['D', ['A', -1, -1, ['C', -1, -1, -1, ['D', -1, -1, -1, -1, '$'], 0], -1, 0], -1, -1, -1, 0], 0], -1, 0], ['C', -1, -1, -1, ['D', -1, -1, -1, -1, '$'], 0], -1, 0], ['B', -1, -1, ['C', -1, -1, -1, ['D', ['A', -1, -1, ['C', -1, -1, -1, ['D', -1, -1, -1, -1, '$'], 0], -1, 0], -1, -1, -1, 0], 0], -1, 0], ['C', -1, -1, -1, ['D', ['A', -1, -1, ['C', -1, -1, -1, ['D', -1, -1, -1, -1, '$'], 0], -1, 0], -1, -1, -1, '$'], 0], ['D', ['A', -1, -1, ['C', -1, -1, -1, ['D', -1, -1, -1, -1, '$'], 0], -1, 0], -1, -1, -1, '$'], 0]