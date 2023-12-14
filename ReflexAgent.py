from GameState import *
from search import *

class ReflexAgent:
    def __init__(self, searchFunction):
        self.searchFunction = searchFunction
        self.total_nodes_explored = 0

    def getAction(self, game_state):
        searchProblem = SnakeSearchProblem(game_state)
        search_result = self.searchFunction(searchProblem)

        if search_result:
            solution, nodes_explored = search_result
            self.total_nodes_explored += nodes_explored
            if solution:
                return solution[0]
        return None 

    def getNodesExplored(self):
        return self.total_nodes_explored

    def getFood(self, game_state):
        searchProblem = SnakeSearchProblem(game_state)
        return searchProblem.goal_state
