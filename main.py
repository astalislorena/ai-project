# import the pygame module, so you can use it
import pygame
from random import randint
import time
import maps

# Creating some colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (173, 255, 47)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class DMap:
    def __init__(self, index):
        self.n = maps.dimensions[index]
        self.surface = maps.maps[index]

    def image(self, mouseX, mouseY, catX, catY):

        imagine = pygame.Surface((20 * self.n, 20 * self.n - 1))

        brick = pygame.Surface((20, 20))
        brick.fill(BLACK)

        empty = pygame.Surface((20, 20))
        empty.fill(WHITE)

        cheese = pygame.image.load("cheese.png")

        for i in range(self.n):
            for j in range(self.n):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                elif self.surface[i][j] == 0:
                    imagine.blit(empty, (j * 20, i * 20))
                elif self.surface[i][j] == -1:
                    imagine.blit(cheese, (j * 20, i * 20))
                elif self.surface[i][j] >= 2:
                    imagine.blit(empty, (j * 20, i * 20))

        mouse = pygame.image.load("mouse.png")
        imagine.blit(mouse, (mouseY * 20, mouseX * 20))
        cat = pygame.image.load("cat.png")
        imagine.blit(cat, (catY * 20, catX * 20))
        return imagine


class Mouse:
    def __init__(self, index, x, y):
        self.x = x
        self.y = y
        self.max = maps.dimensions[index]

    def moveDSF(self, detectedMap, stack):
        stackLen = len(stack)
        print(self.x, self.y)
        if self.x > 0 and (
                detectedMap.surface[self.x - 1][self.y] == 0 or detectedMap.surface[self.x - 1][self.y] == -1):
            stack.append([self.x - 1, self.y])
        elif self.y < self.max - 1 and (
                detectedMap.surface[self.x][self.y + 1] == 0 or detectedMap.surface[self.x][self.y + 1] == -1):
            stack.append([self.x, self.y + 1])
        elif self.x < self.max - 1 and (
                detectedMap.surface[self.x + 1][self.y] == 0 or detectedMap.surface[self.x + 1][self.y] == -1):
            stack.append([self.x + 1, self.y])
        elif self.y > 0 and (
                detectedMap.surface[self.x][self.y - 1] == 0 or detectedMap.surface[self.x][self.y - 1] == -1):
            stack.append([self.x, self.y - 1])
        newStackLen = len(stack)

        if stackLen == newStackLen:
            try:
                # detectedMap.surface[self.x][self.y] = 2
                newCoordinates = stack.pop()
                newCoordinates = stack[-1]
                self.x = newCoordinates[0]
                self.y = newCoordinates[1]

            except IndexError:
                return 1
        else:
            newCoordinates = None
            try:
                newCoordinates = stack[-1]
            except IndexError:
                return 1
            self.x = newCoordinates[0]
            self.y = newCoordinates[1]


class Cat:
    def __init__(self, index, x, y):
        self.x = x
        self.y = y
        self.max = maps.dimensions[index]

    def moveDSF(self, detectedMap, stack):
        stackLen = len(stack)

        if self.x > 0 and (
                detectedMap.surface[self.x - 1][self.y] == 0 or detectedMap.surface[self.x - 1][self.y] == -1):
            stack.append([self.x - 1, self.y])
        elif self.y < self.max - 1 and (
                detectedMap.surface[self.x][self.y + 1] == 0 or detectedMap.surface[self.x][self.y + 1] == -1):
            stack.append([self.x, self.y + 1])
        elif self.x < self.max - 1 and (
                detectedMap.surface[self.x + 1][self.y] == 0 or detectedMap.surface[self.x + 1][self.y] == -1):
            stack.append([self.x + 1, self.y])
        elif self.y > 0 and (
                detectedMap.surface[self.x][self.y - 1] == 0 or detectedMap.surface[self.x][self.y - 1] == -1):
            stack.append([self.x, self.y - 1])
        newStackLen = len(stack)

        newStackLen = len(stack)

        if stackLen == newStackLen:
            try:
                newCoordinates = stack.pop()
                newCoordinates = stack[-1]
                self.x = newCoordinates[0]
                self.y = newCoordinates[1]
            except IndexError:
                return 1
        else:
            newCoordinates = None
            try:
                newCoordinates = stack[-1]
            except IndexError:
                return 1
            self.x = newCoordinates[0]
            self.y = newCoordinates[1]


def main(index):

    # we create the map
    m = DMap(index)

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("mouse, cheese and cat")

    # we position the mouse somewhere in the area
    mouseStack = []
    mouseX = randint(0, m.n - 1)
    mouseY = randint(0, m.n - 1)

    mouseStack.append([mouseX, mouseY])
    mouse = Mouse(index, mouseX, mouseY)

    cheese = 2

    # we position the cat somewhere in the area
    catStack = []
    catX = randint(0, m.n - 1)
    catY = randint(0, m.n - 1)

    catStack.append([catX, catY])
    cat = Cat(index, catX, catY)

    screen = pygame.display.set_mode((20 * (m.n - 1), 20 * m.n))
    screen.fill(WHITE)

    # define a variable to control the main loop
    running = True

    # main loop
    mouseCurrentNodeCount = 10
    while running:
        # event handling, gets all event from the event stack
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                running = False
        time.sleep(0.3)
        if mouse.moveDSF(m, mouseStack) == 1:
            break
        if cat.moveDSF(m, catStack) == 1:
            break
        if cat.x == mouse.x and cat.y == mouse.y:
            print("CAT WINS")
            running = False
        if m.surface[mouse.x][mouse.y] == -1:
            if cheese == 0:
                print("MOUSE WINS")
                running = False
            else:
                cheese -= 1
        mouseCurrentNodeCount += 0.5
        m.surface[mouse.x][mouse.y] = mouseCurrentNodeCount
        screen.blit(m.image(mouse.x, mouse.y, cat.x, cat.y), (0, 0))
        pygame.display.flip()

    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main(1)
