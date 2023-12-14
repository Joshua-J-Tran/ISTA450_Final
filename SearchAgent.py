from GameState import *
from search import *

class SearchAgent:
    def __init__(self, searchFunction):
        self.searchFunction = searchFunction
        self.total_nodes_explored = 0

    def getAction(self, game_state):
        searchProblem = SnakeSearchProblem(game_state)
        solution, self.nodes_explored = self.searchFunction(searchProblem) 
        print("DFS Solution:", solution) 
        return solution[0] if solution else None
    
    def getPath(self, game_state):
        searchProblem = SnakeSearchProblem(game_state)
        if self.searchFunction(searchProblem) :
            result, nodes_explored = self.searchFunction(searchProblem) 
            self.total_nodes_explored += nodes_explored
            return result
        else:
            pass

    
    def getNodesExplored(self):
        return self.total_nodes_explored
    
    def getFood(self, game_state):
        searchProblem = SnakeSearchProblem(game_state)
        return searchProblem.goal_state

class RightTurnAgent:
    def __init__(self):
        self.move_count = 0  

    def getAction(self, game_state):
        self.move_count += 1
        if self.move_count % 3 == 0:
            current_direction = game_state.direction
            next_direction = self.turn_right(current_direction)
            print("Action: Turn Right")
            return next_direction

        return game_state.direction

    def turn_right(self, current_direction):
        right_turns = {"UP": "RIGHT", "RIGHT": "DOWN", "DOWN": "LEFT", "LEFT": "UP"}
        return right_turns.get(current_direction, "UP")