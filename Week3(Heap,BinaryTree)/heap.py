import heapq

class MinHeap(object):
    def __init__(self):
        self._data = []
        heapq.heapify(self._data)
        self.size = 0

    def add(self, value):
        heapq.heappush(self._data, value)
        self.size += 1

    def pop(self):
        poped = heapq.heappop(self._data)
        self.size -= 1
        return poped

    def smallest(self):
        return heapq.nsmallest(1,self._data)[0]

class MaxHeap(object):
    def __init__(self):
        self._data = []
        heapq.heapify(self._data)
        self.size = 0

    def add(self, value):
        heapq.heappush(self._data, -value)
        self.size += 1

    def pop(self):
        poped = -heapq.heappop(self._data)
        self.size -= 1
        return poped

    def largest(self):
        return -heapq.nsmallest(1,self._data)[0]

def read():
    file = open('Median.txt')
    lines = file.readlines()
    num = [int(line.strip('\n').strip('\r')) for line in lines]
    return num

def get_median(H_low, H_high):
    if H_low.size >= H_high.size:
        return H_low.largest()
    if H_low.size < H_high.size:
        return H_high.smallest()

def median_adder(num):
    '''Compute the median by creating the heap data structure '''

    total = 0
    H_low = MaxHeap() #max heap
    H_high = MinHeap() #min heap

    for i, value in enumerate(num):
        # print("")
        # print("Loop No.", i)
        # print("Next", value)

        if i == 0:
            H_low.add(value)
            median = H_low.largest()
            total += median
            # print("Heap", H_low._data)
            # print("median",median)
        elif i == 1:
            if value < H_low.largest():
                poped = H_low.pop()
                H_high.add(poped)
                H_low.add(value)
            else:
                H_high.add(value)

            # print("Heap", H_low._data, " ", H_high._data)
            median = H_low.largest()
            total += median
            # print("median",median)

        else:
            low_max = H_low.largest()
            high_min = H_high.smallest()

            if value <= low_max:
                H_low.add(value)
            elif value >= high_min:
                H_high.add(value)
            else:
                H_low.add(value)
            if H_low.size - H_high.size >= 2:
                poped = H_low.pop()
                H_high.add(poped)
            if H_high.size - H_low.size >= 2:
                poped = H_high.pop()
                H_low.add(poped)
            # print("Heap", H_low._data, " ", H_high._data)

            median = get_median(H_low, H_high)
            # print("median",median)
            total += median

        total %= 10000

    return total


if __name__ == "__main__":
    num = read()
    total = median_adder(num)
    print(total)



# class MaxHeap(object):
#     def __init__(self):
#         self.heap = []
#         self.size = 0

#     def heap_add(self, value):
#         self.heap.append(value)
#         index = self.heap_len() - 1
#         self.size += 1

#         if index <= 0:
#             pass
#         else:
#             parents = index/2
#             while self.heap[parents] < self.heap[index]:
#                 self.heap[parents], self.heap[index] = self.heap[index], self.heap[parents]
#                 index = parents
#                 parents = parents/2

#     def heap_pop(self):
#         poped = self.heap.pop(0)
#         return poped

#     def heap_len(self):
#         return len(self.heap)
    

# class MinHeap(object):
#     def __init__(self):
#         self.heap = []
#         self.size = 0

#     def heap_add(self, value):
#         self.heap.append(value)
#         index = self.heap_len() - 1
#         self.size += 1

#         if index <= 0:
#             pass
#         else:
#             parents = index/2
#             while self.heap[parents] > self.heap[index]:
#                 self.heap[parents], self.heap[index] = self.heap[index], self.heap[parents]
#                 index = parents
#                 parents = parents/2

#     def heap_pop(self):
#         if len(self.heap) == 0:
#             pass
#         elif len(self.heap) <= 2:
#             return self.heap.pop(0)
#         else:
#             poped = self.heap.pop(0)

#             index = 0
#             c1 = index*2
#             c2 = index*2 + 1

#             if c1 > self.size:
#                 if self.heap[c1] <= self.heap[c2]:
#                     if 

#             while self.heap[index] >= max(self.heap[c1], self.heap[c2]):
#                 if self.heap[c1] <= self.heap[c2]:
#                     self.heap[c1], self.heap[index] = self.heap[index], self.heap[c1]
#                     index = c1
#                 if self.heap[c1] >= self.heap[c2]:
#                     self.heap[c2], self.heap[index] = self.heap[index], self.heap[c2]
#                     index = c2
#                 c1 = index*2
#                 c2 = index*2 + 1

#                 try:
#                     self.heap[c1]
#                 except IndexError:
#                     break

#                 try:
#                     self.heap[c2]
#                 except IndexError:
#                     if self.heap[index] >= self.heap[c1]:
#                         self.heap[c1], self.heap[index] = self.heap[c1], self.heap[index]
#                     break 


#         return poped

#     def heap_len(self):
#         return len(self.heap)

