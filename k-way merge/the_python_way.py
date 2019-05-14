import heapq
import random

def merger(k,l):

    base = [ x for x in range(l) ]
    random.shuffle(base)

    lists = []

    for i in range(k):
        lists.append(sorted(base[(l//k)*i:(l//k)*(i+1)]))
        
    result = []

    for i in range(k):
        print("list",i,lists[i])
    print("result:",result)

    heap = []
  
    for l in lists:
        heapq.heappush(heap,(l[0],l))
	
    while(heap):
        print("Heap content:")
        for _,l in heap:
            print("->",l)
        print("result:",result)
        input()

        _,actual_list = heapq.heappop(heap)
        result.append(actual_list.pop(0))

        if actual_list:
            heapq.heappush(heap,(actual_list[0],actual_list))

    for l in lists:
        print("lists",l)
    print("result:",result)


merger(7,155)

