import collections

v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


def calcHeuristic(currX, currY, destX, destY):
    return abs(currX - destX) + abs(currY - destY)


def isValid(map, x, y):
    return x >= 0 and y >= 0 and x < map.n and y < map.m


def traceBack(pointMap, destX, destY):
    stack = []
    currX = destX
    currY = destY

    print("Starting")
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


def Greedy(map, startX, startY, destX, destY):
    if map.surface[startX][startY] == 1:
        return []

    pointMap = [[0 for i in range(map.n)] for j in range(map.m)];

    for i in range(map.n):
        for j in range(map.m):
            pointMap[i][j] = Point(i, j, -1, -1, calcHeuristic(i, j, destX, destY))

    pointMap[startX][startY].parentX = startX
    pointMap[startX][startY].parentY = startY

    OrderedDictOpenList = []
    closedList = [[False for i in range(map.n)] for j in range(map.m)];

    OrderedDictOpenList.append((pointMap[startX][startY].h, (startX, startY)))

    foundDest = False

    while len(OrderedDictOpenList) > 0 and not foundDest:
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
                    return traceBack(pointMap, destX, destY)


                elif closedList[newX][newY] == False and map.surface[newX][newY] == 0:

                    OrderedDictOpenList.append((pointMap[newX][newY].h, (newX, newY)))
                    OrderedDictOpenList.sort()

                    pointMap[newX][newY].parentX = x
                    pointMap[newX][newY].parentY = y

    if not foundDest:
        return []
