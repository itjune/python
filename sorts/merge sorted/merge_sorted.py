data = open('input.txt').read().split('\n')
n = int(data[0].split(' ')[0])
m = int(data[0].split(' ')[1])
arrays = [[] for i in range(n)]
for i in range(1,n+1):
    arrays[i-1] = [int(x) for x in data[i].split(' ')]

import heapq as hq 

heap = []
for i in range(n):
    hq.heappush(heap, [arrays[i][0], i, 1])

result = []
for k in range(n*m):
    element, i, j = hq.heappop(heap)
    result.append(element)
    if j < m:
        hq.heappush(heap, [arrays[i][j], i, j + 1])
print (*result)