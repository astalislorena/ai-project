import collections

v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


def calcHeuristic(currX, currY, destX, destY):
    return abs(currX - destX) + abs(currY - destY)


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
        self.g = 10000
        self.h = h
        self.f = 10000


def AStar(map, startX, startY, destX, destY):
    if map.surface[startX][startY] == 1:
        return []

    pointMap = [[0 for i in range(map.n)] for j in range(map.m)];

    for i in range(map.n):
        for j in range(map.m):
            pointMap[i][j] = Point(i, j, -1, -1, calcHeuristic(i, j, destX, destY))

    pointMap[startX][startY].parentX = startX
    pointMap[startX][startY].parentY = startY
    pointMap[startX][startY].f = 0

    OrderedDictOpenList = []
    closedList = [[False for i in range(map.n)] for j in range(map.m)];

    OrderedDictOpenList.append((0, (startX, startY)))

    foundDest = 0

    while (len(OrderedDictOpenList) > 0 and foundDest == False):
        currentNode = OrderedDictOpenList.pop(0)
        x = currentNode[1][0]
        y = currentNode[1][1]
        closedList[x][y] = True

        for pairCoord in v:
            newX = x + pairCoord[0]
            newY = y + pairCoord[1]
            if isValid(map, newX, newY):
                if newX == destX and newY == destY:
                    foundDest = True
                    pointMap[newX][newY].parentX = x
                    pointMap[newX][newY].parentY = y
                    pointMap[newX][newY].g = pointMap[x][y].g + 1
                    return traceBack(pointMap, destX, destY)

                elif not closedList[newX][newY] and map.surface[newX][newY] == 0:
                    gNew = pointMap[x][y].g + 1
                    hNew = pointMap[newX][newY].h
                    fNew = gNew + hNew

                    if pointMap[newX][newY].f > fNew or pointMap[newX][newY].f == 10000:
                        OrderedDictOpenList.append((fNew, (newX, newY)))
                        OrderedDictOpenList.sort()
                        pointMap[newX][newY].parentX = x
                        pointMap[newX][newY].parentY = y
                        pointMap[newX][newY].g = gNew
                        pointMap[newX][newY].h = hNew
                        pointMap[newX][newY].f = fNew
    if not foundDest:
        return []
