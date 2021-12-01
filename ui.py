# import the pygame module, so you can use it
import random, pygame, time
from random import random, randint
from Cat import Cat
from Domain import Map
from Domain import Agent
from Controller import Controller
# Creating some colors
BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
YELLOW = (255,255,0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class UserInterface:

    def __init__(self, controller):
        self.controller = controller
        level = self.askUserInputLevel()
        self.initMapAndMouse(level)
        self.initPyGame(level)
        level -= 1
        self.startX = level
        self.startY = 0
        self.finishX = 0
        self.finishY = level
        path = self.askUserInputAnCalculatePath()

        self.runGame(path)

    def displayWithPath(self, image, path):
        mark = pygame.Surface((20, 20))
        mark.fill(GREEN)
        for move in path:
            image.blit(mark, (move[1] * 20, move[0] * 20))
        return image

    def moveSet(self, list):
        for item in list:
            yield item

    def initPyGame(self, level):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Mouse")

        self.screen = pygame.display.set_mode((level * 20, level * 20))
        self.screen.fill(WHITE)

    def initMapAndMouse(self, level):
        self.m = Map(level, level)
        self.m.randomMap()
        x = level - 1
        y = level - 1
        self.d = Agent(x, y)

    def askUserInputLevel(self):
        choice = int(input("1. Level 1 (maze of 20)\n2. Level 2 (maze of 40)\n3. Level 3 (maze of 50)\n4.Exit\n"))
        if choice == 1:
            return 20
        elif choice == 2:
            return 40
        elif choice == 3:
            return 50
        elif choice == 4:
            exit()
        return 20

    def askUserInputAnCalculatePath(self):
        choice = int(input("1.A*\n2.Uniform Cost\n3.DFS\n4.BFS\n5.Exit\n"))
        start_time = time.time()
        if choice == 1:
            path = self.controller.searchAStar(self.m, self.startX, self.startY, self.finishX, self.finishY)
        if choice == 2:
            path = self.controller.uniformCost(self.m, self.startX, self.startY, self.finishX, self.finishY)
        if choice == 3:
            path = self.controller.BFS(self.m, self.startX, self.startY, self.finishX, self.finishY)
        if choice == 4:
            path = self.controller.DFS(self.m, self.startX, self.startY, self.finishX, self.finishY)
        if choice == 5:
            exit()
        print("--- %s seconds ---" % (time.time() - start_time))
        return path

    def runGame(self, path):

        pathLength = len(path)
        stepNumber = 0
        self.m.surface[self.startX][self.startY] = -1
        self.m.surface[self.finishX][self.finishY] = -1
        cat = Cat(3, 10)
        catStack = [[3, 10]]
        catMap = self.m
        catProgress = 10
        running = True
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

            stepNumber += 1
            if stepNumber > pathLength - 1:
                break
            if cat.moveDSF(catMap, catStack) == 1:
                print("cat broken")
            catProgress += 0.5
            catMap.surface[cat.x][cat.y] = catProgress
            self.d.x = path[stepNumber][0]
            self.d.y = path[stepNumber][1]
            self.m.surface[self.d.x][self.d.y] = 2
            time.sleep(0.1)
            self.screen.blit(self.d.mapWithMouse(self.m.image()), (0, 0))
            catImg = pygame.image.load("cat.png")
            self.screen.blit(catImg, (cat.y * 20, cat.x * 20))
            if cat.x == self.d.x and cat.y == self.d.y:
                print("CAT WINS")
            pygame.display.flip()

        self.screen.blit(self.displayWithPath(self.m.image(), path), (0, 0))

        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
