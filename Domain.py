import random

import numpy as np

import pygame, pickle

BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
YELLOW = (255,255,0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mapWithMouse(self, mapImage):
        mouse = pygame.image.load("mouse.png")
        mapImage.blit(mouse, (self.y * 20, self.x * 20))
        return mapImage



class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random.random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def image(self, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((self.n * 20, self.m * 20))
        brick = pygame.Surface((20, 20))
        path = pygame.Surface((20, 20))
        cheese = pygame.image.load("cheese.png")
        brick.fill(BLUE)
        path.fill(YELLOW)
        imagine.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                if self.surface[i][j] == 2:
                    imagine.blit(path, (j * 20, i * 20))
                if self.surface[i][j] == -1:
                    imagine.blit(cheese, (j * 20, i * 20))

        return imagine

