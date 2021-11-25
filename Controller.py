
from AStar import AStar
from Greedy import Greedy
from BFS import BFS
from DFS import DFS
from UniformCost import UniformCost

class Controller:

    def searchAStar(self, mapM, initialX, initialY, finalX, finalY):
        list = AStar(mapM, initialX, initialY, finalX, finalY)
        return list

    def searchGreedy(self, mapM, initialX, initialY, finalX, finalY):
        list = Greedy(mapM, initialX, initialY, finalX, finalY)
        return list

    def BFS(self, mapM, initialX, initialY, finalX, finalY):
        list = BFS(mapM, initialX, initialY, finalX, finalY)
        return list

    def DFS(self, mapM, initialX, initialY, finalX, finalY):
        list = DFS(mapM, initialX, initialY, finalX, finalY)
        return list

    def uniformCost(self, mapM, initialX, initialY, finalX, finalY):
        list = UniformCost(mapM, initialX, initialY, finalX, finalY)
        return list
