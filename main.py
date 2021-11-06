
# import the pygame module, so you can use it
import pickle
import sys
import pygame
from pygame.locals import *
from random import random, randint
import numpy as np
import time

# Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50 ,120 ,120)
RED   = (255, 0, 0)
GREEN = (173 ,255 ,47)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class Environment():
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.__surface = np.zeros((self.__n, self.__m))

    def randomMap(self, fill = 0.2):
        for i in range(self.__n):
            for j in range(self.__m):
                if random() <= fill :
                    self.__surface[i][j] = 1

    def __str__(self):
        string =""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j]))
            string = string + "\n"
        return string

    def readUDMSensors(self, x ,y):
        readings =[0 ,0 ,0 ,0]
        # UP
        xf = x - 1
        while ((xf >= 0) and (self.__surface[xf][y] == 0)):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while ((xf < self.__n) and (self.__surface[xf][y] == 0)):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while ((yf < self.__m) and (self.__surface[x][yf] == 0)):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.__surface[x][yf] == 0)):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1

        return readings

    def saveEnvironment(self, numFile):
        with open(numFile ,'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadEnvironment(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.__n = dummy.__n
            self.__m = dummy.__m
            self.__surface = dummy.__surface
            f.close()

    def image(self, colour = BLUE, background = WHITE):
        imagine = pygame.Surface((420 ,420))
        brick = pygame.Surface((20 ,20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.__n):
            for j in range(self.__m):
                if (self.__surface[i][j] == 1):
                    imagine.blit(brick, ( j * 20, i * 20))

        return imagine


class DMap():
    def __init__(self):
        self.currentNodeCount =10
        self.__n = 20
        self.__m = 20
        self.surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.surface[i][j] = -1


    def markDetectedWalls(self, e, x, y):
        #   To DO
        # mark on this map the wals that you detect

        wals = e.readUDMSensors(x, y)

        # if self.surface[x][y]>10:
        #     self.surface[x][y] = 2
        #     return None

        self.currentNodeCount+=0.5
        self.surface[x][y] = self.currentNodeCount



        i = x - 1
        if wals[UP] > 0:
            while (( i>=0) and (i >= x - wals[UP])):
                if self.surface[i][y] ==-1:
                    self.surface[i][y] = 0
                i = i - 1
        if ( i>=0):
            self.surface[i][y] = 1

        i = x + 1
        if wals[DOWN] > 0:
            while ((i < self.__n) and (i <= x + wals[DOWN])):
                if self.surface[i][y] == -1:
                    self.surface[i][y] = 0
                i = i + 1
        if (i < self.__n):
            self.surface[i][y] = 1

        j = y + 1
        if wals[LEFT] > 0:
            while ((j < self.__m) and (j <= y + wals[LEFT])):
                if self.surface[x][j] == -1:
                    self.surface[x][j] = 0
                j = j + 1
        if (j < self.__m):
            self.surface[x][j] = 1

        j = y - 1
        if wals[RIGHT] > 0:
            while ((j >= 0) and (j >= y - wals[RIGHT])):
                if self.surface[x][j] == -1:
                    self.surface[x][j] = 0
                j = j - 1
        if (j >= 0):
            self.surface[x][j] = 1

        return None

    def image(self, x, y):

        imagine = pygame.Surface((420, 420))
        imagine.fill(GRAYBLUE)

        brick = pygame.Surface((20, 20))
        brick.fill(BLACK)

        empty = pygame.Surface((20, 20))
        empty.fill(WHITE)

        defaultVisited = pygame.Surface((20, 20))
        defaultVisited.fill(GREEN)

        for i in range(self.__n):
            for j in range(self.__m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                elif self.surface[i][j] == 0:
                    imagine.blit(empty, (j * 20, i * 20))
                elif self.surface[i][j] == 2:
                    imagine.blit(defaultVisited, (j * 20, i * 20))
                elif self.surface[i][j] > 10:
                    visited = pygame.Surface((20, 20))
                    # visited.fill((255, 246 - 0.5 * self.surface[i][j], 246 - 0.5 * self.surface[i][j]))
                    cheese = pygame.image.load("cheese.png")
                    imagine.blit(cheese, (j * 20, i * 20))

        mouse = pygame.image.load("mouse.png")
        imagine.blit(mouse, (y * 20, x * 20))
        return imagine


class Mouse():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def moveDSF(self, detectedMap, stack):
        print("moving ", len(stack), " \n")
        stackLen = len(stack)

        if self.x > 0 and detectedMap.surface[self.x - 1][self.y] == 0:
            stack.append([self.x - 1, self.y])
        elif self.y < 19 and detectedMap.surface[self.x][self.y + 1] == 0:
            stack.append([self.x, self.y + 1])
        elif self.x < 19 and detectedMap.surface[self.x + 1][self.y] == 0:
            stack.append([self.x + 1, self.y])
        elif self.y > 0 and detectedMap.surface[self.x][self.y - 1] == 0:
            stack.append([self.x, self.y - 1])
        newStackLen = len(stack)

        # if stackLen!=newStackLen:
        #     stack.insert(-2,[self.x,self.y])

        if stackLen == newStackLen:
            try:
                detectedMap.surface[self.x][self.y] = 2
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


def main():
    # we create the environment
    e = Environment()
    e.loadEnvironment("test2.map")

    stack = []
    # we create the map
    m = DMap()

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("mouse cheese and cat")

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    stack.append([x, y])
    # cream drona
    d = Mouse(x, y)

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode((800, 400))
    screen.fill(WHITE)
    screen.blit(e.image(), (0, 0))

    # define a variable to control the main loop
    running = True

    # main loop
    m.markDetectedWalls(e, d.x, d.y)
    while running:
        # event handling, gets all event from the event stack
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        time.sleep(0.3)
        if d.moveDSF(m, stack) == 1:
            break
        m.markDetectedWalls(e, d.x, d.y)
        screen.blit(m.image(d.x, d.y), (400, 0))
        pygame.display.flip()

    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()