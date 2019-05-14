class MinHeap:
  def __init__(self):
    self.heap = []
    
  def push(self,data):
    self.heap.append(data)
    i = len(self.heap)-1
    
    prev = ( (i + 1) // 2 ) - 1

    while i and self.heap[i] < self.heap[prev]:
        self.heap[i],self.heap[prev] = self.heap[prev],self.heap[i]
        i = prev
        prev = ( (i + 1) // 2 ) - 1

        
  def is_empty(self):
    return len(self.heap) == 0
  
  def pop(self):
    self.heap[0],self.heap[-1] = self.heap[-1],self.heap[0]
    result = self.heap.pop()
    used = len(self.heap)-1
    
    i = 0
    
    while (i <= used):
      left = (i * 2) + 1
      right = (i *2) + 2

      if left >= len(self.heap) or left <= i:
        break
      
      if right >= len(self.heap):
        if (self.heap[left] < self.heap[i]):
          self.heap[i],self.heap[left] = self.heap[left],self.heap[i]          
        break
      
      if self.heap[i] < self.heap[left] and self.heap[i] < self.heap[right]:
        break
      
      if self.heap[right] < self.heap[left]:
        self.heap[right],self.heap[i] = self.heap[i],self.heap[right]
        i = right
        continue
      
      self.heap[left],self.heap[i] = self.heap[i],self.heap[left]
      i = left
  
    return result

import random

def merger(k,l):

  base = [ x for x in range(l) ]
  random.shuffle(base)

  lists = []

  for i in range(k):
    lists.append(sorted(base[(l//k)*i:(l//k)*(i+1)]))
  
  indexes = [0 for _ in range(l)]

  result = []

  for i in range(k):
    print("list",i,lists[i])
  print("result:",result)

  heap = MinHeap()
  
  for i in range(k):
    heap.push((lists[i].pop(0),i))

  while(not heap.is_empty()):
    for i in range(k):
        print("list",i,lists[i])
    print("Heap content:", [ x[0] for x in heap.heap])
    print("result:",result)
    input()

    value,index = heap.pop()
    result.append(value)
    indexes[index] += 1

    if lists[index]:
      heap.push((lists[index].pop(0),index))

  for l in lists:
    print("lists",l)
  print("result:",result)


merger(7,155)

