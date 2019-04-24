class CharMatrix():
    def __init__(self,matrix,n_rows,n_cols):
        self.matrix = matrix
        self.n_rows = n_rows
        self.n_cols = n_cols
    
    def get_at(self,row,col):
        if not 0 <= row < self.n_rows:
            return None
        if not 0 <= col < self.n_cols:
            return None

        return self.matrix[row*self.n_cols+col]
    
def smart_get(smart_storage,string):
    n = len(string)
    if not n in smart_storage:
        return -1
    
    if not string in smart_storage[n]:
        return -1
        
    smart_storage[n].remove(string)
    
    while not smart_storage.get(n,None) and n > 0 :
        n-=1
    
    return n
    
DIRECTIONS = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
def find_all(actual,matrix,used,storage,acumulated,max_len,found):
    char = matrix.get_at(actual[0],actual[1])
    if not char:
        return
    
    acumulated += char
    acum_len = len(acumulated)
    
    #print(acumulated,storage)
    
    if acum_len > max_len[0]:
        return

    n = smart_get(storage,acumulated)
    
    if n >= 0:
        found.append(acumulated)
    
    if n == 0:
        return
    
    if acum_len > n > 0 and acum_len == max_len:
        max_len[0] = n
        
    for i,j in DIRECTIONS:
        new_point = actual[0]+i,actual[1]+j

        if new_point in used:
            continue
        
        used.add(new_point)
        find_all(new_point,matrix,used,storage,acumulated,max_len,found)
        used.remove(new_point)
    
def main():
    cases = int(input())
    for _ in range(cases):
        input()
        words = set(input().split())
        s_storage = {}
        max_n = 0
        
        for word in words:
            n = len(word)
            s_storage[n] = s_storage.get(n,set())
            s_storage[n].add(word)
            max_n = max(max_n,n)
            
        rows,columns = [ int(x) for x in input().split() ]
        matrix = CharMatrix(input().split(),rows,columns)
        
        max_len = [max_n]
        found = []
        for i in range(0,rows):
            for j in range(0,columns):
                find_all((i,j),matrix,set([(i,j)]),s_storage,"",max_len,found)
    
        if found:
            found.sort()
            print(" ".join(found))    
        else:
            print("-1")
main()
