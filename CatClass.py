import maps


class Cat:
    def __init__(self, index, x, y):
        self.x = x
        self.y = y
        self.max = maps.dimensions[index]

    def moveDSF(self, detectedMap, stack):
        stackLen = len(stack)

        if self.x > 0 and (
                detectedMap.surface[self.x - 1][self.y] == 0):
            stack.append([self.x - 1, self.y])
        elif self.y < self.max - 1 and (
                detectedMap.surface[self.x][self.y + 1] == 0):
            stack.append([self.x, self.y + 1])
        elif self.x < self.max - 1 and (
                detectedMap.surface[self.x + 1][self.y] == 0):
            stack.append([self.x + 1, self.y])
        elif self.y > 0 and (
                detectedMap.surface[self.x][self.y - 1] == 0):
            stack.append([self.x, self.y - 1])

        newStackLen = len(stack)

        if stackLen == newStackLen:
            try:
                detectedMap.surface[self.x][self.y] = 3
                newCoordinates = stack.pop()
                # newCoordinates = stack[-1]
                self.x = newCoordinates[0]
                self.y = newCoordinates[1]
            except IndexError:
                print("cat - here 1")
                return 1
        else:
            newCoordinates = None
            try:
                newCoordinates = stack[-1]
            except IndexError:
                print("cat - here 2")
                return 1
            self.x = newCoordinates[0]
            self.y = newCoordinates[1]

    def moveBFS(self, detectedMap, queue):
        if self.x > 0 and (
                detectedMap.surface[self.x - 1][self.y] == 0):
            queue.insert(0, [self.x - 1, self.y])
        if self.y < self.max - 1 and (
                detectedMap.surface[self.x][self.y + 1] == 0):
            queue.insert(0, [self.x, self.y + 1])
        if self.x < self.max - 1 and (
                detectedMap.surface[self.x + 1][self.y] == 0):
            queue.insert(0, [self.x + 1, self.y])
        if self.y > 0 and (
                detectedMap.surface[self.x][self.y - 1] == 0):
            queue.insert(0, [self.x, self.y - 1])
        try:
            newCoordinates = queue.pop(0)
            print(newCoordinates)
            detectedMap.surface[self.x][self.y] = 2
            self.x = newCoordinates[0]
            self.y = newCoordinates[1]
        except IndexError:
            return 1
