import collections

v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


def isValid(map, x, y):
    return 0 <= x < map.n and 0 <= y < map.m

def isAtDest(x, y, destination):
    if destination[0] == x and destination[1] == y:
        return True


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
    print(stack)
    return stack


class Point:
    def __init__(self, x, y, px, py, visited):
        self.x = x
        self.y = y
        self.parentX = px
        self.parentY = py
        self.visited = visited


def BFS(map, startX, startY, destX, destY):
    if map.surface[startX][startY] == 1:
        return []
    destinations = [[destX, destY], [0, 0], [9, 0]]
    pointMap = [[0 for i in range(map.n)] for j in range(map.m)];

    for i in range(map.n):
        for j in range(map.m):
            pointMap[i][j] = Point(i, j, -1, -1, False)

    pointMap[startX][startY].parentX = startX
    pointMap[startX][startY].parentY = startY
    pointMap[startX][startY].visited = True

    queue = [pointMap[startX][startY]]

    foundDest = False

    while len(queue) > 0 and not foundDest:
        currentNode = queue.pop(0)
        x = currentNode.x
        y = currentNode.y

        for pairCoord in v:
            newX = x + pairCoord[0]
            newY = y + pairCoord[1]
            if isValid(map, newX, newY) and map.surface[newX][newY] != 1:
                if newX == destX and newY == destY:
                    foundDest = True
                    pointMap[newX][newY].parentX = x
                    pointMap[newX][newY].parentY = y
                    return traceBack(pointMap, destX, destY)
                elif not pointMap[newX][newY].visited:
                    pointMap[newX][newY].visited = True
                    pointMap[newX][newY].parentX = x
                    pointMap[newX][newY].parentY = y
                    queue.append(pointMap[newX][newY])
    if not foundDest:
        return []
