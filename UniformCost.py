import heapq, random

v = [[-1, 0], [1, 0], [0, 1], [0, -1]]

def isValid(map, x, y):
    return 0 <= x < map.n and 0 <= y < map.m

def traceBack(pointMap, destX, destY):
    stack = []
    currX = destX
    currY = destY

    while pointMap[currX][currY].parentX != currX or pointMap[currX][currY].parentY != currY:
        stack.append((currX, currY))
        newX = pointMap[currX][currY].parentX
        newY = pointMap[currX][currY].parentY
        currX = newX
        currY = newY

    stack.append((currX, currY))
    stack.reverse()
    return stack


class Point:
    def __init__(self, x, y, px, py, h):
        self.x = x
        self.y = y
        self.parentX = px
        self.parentY = py
        self.h = h
        self.visited = False


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (priority, _, item) = heapq.heappop(self.heap)
        return priority, item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


def UniformCost(map, startX, startY, destX, destY):
    if map.surface[startX][startY] == 1:
        return []

    pointMap = [[0 for i in range(map.n)] for j in range(map.m)]

    for i in range(map.n):
        for j in range(map.m):
            pointMap[i][j] = Point(i, j, -1, -1, 0)

    pointMap[startX][startY].parentX = startX
    pointMap[startX][startY].parentY = startY
    pointMap[startX][startY].visited = True

    queue = PriorityQueue()

    queue.push(pointMap[startX][startY], 0)
    p = 1
    while not queue.isEmpty():
        (priority, currentNode) = queue.pop()
        x = currentNode.x
        y = currentNode.y
        p += 1
        for pairCoord in v:
            newX = x + pairCoord[0]
            newY = y + pairCoord[1]
            if isValid(map, newX, newY):
                if newX == destX and newY == destY:
                    pointMap[newX][newY].parentX = x
                    pointMap[newX][newY].parentY = y
                    return traceBack(pointMap, destX, destY)

                elif map.surface[newX][newY] == 0 and not pointMap[newX][newY].visited:
                    pointMap[newX][newY].visited = True
                    pointMap[newX][newY].parentX = x
                    pointMap[newX][newY].parentY = y
                    queue.push(pointMap[newX][newY], priority + p)
    return []
