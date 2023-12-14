from util import *
import util

class SnakeSearchProblem:
    def __init__(self, snake_game_state):
        self.initial_state = snake_game_state
        self.start_state = snake_game_state.snake[0]

        self.goal_states = [food.get_position() for food in snake_game_state.food_items]
        self.goal_state = self.goal_states[0]
        self.walls = snake_game_state.walls

    def getStartState(self):
        return self.start_state

    def isGoalState(self, state):
        return state in self.goal_states

    def getSuccessors(self, state, current_direction):
        successors = []
        x, y = state

        opposite_direction = self.getOppositeDirection(current_direction)

        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        if opposite_direction:
            directions.remove(opposite_direction)

        for direction in directions:
            next_state = self.simulateMove(state, direction)
            if next_state and next_state not in self.walls:
                successors.append((next_state, direction, 1))

        return successors

    def getOppositeDirection(self, current_direction):
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        return opposites.get(current_direction)

    def getCostOfActions(self, actions):

        if actions is None: return 999999
        x,y = self.getStartState()
        cost = 0
        for action in actions:

            cost += 1
            dx, dy = actionToVector(action)
            x, y = x + dx, y + dy
            if (x,y) in self.walls or (x,y) in self.initial_state.snake:
                return 999999  
        return cost

    def simulateMove(self, state, direction):
        x, y = state
        if direction == "UP":
            y -= 1
        elif direction == "DOWN":
            y += 1
        elif direction == "LEFT":
            x -= 1
        elif direction == "RIGHT":
            x += 1

        new_head = (x, y)
        if new_head in self.initial_state.snake[1:]:
            return None 
        return new_head

def depthFirstSearch(problem):
    stack = util.Stack()
    initial_direction = problem.initial_state.direction  
    stack.push((problem.getStartState(), [], 0, initial_direction)) 
    nodes_explored = 0 
    visited = set()
    max_depth = 100000
    while not stack.isEmpty():
        state, path, depth, current_direction = stack.pop()  
        if depth > max_depth:
            continue
        if problem.isGoalState(state):
            return path, nodes_explored
        if state not in visited:
            visited.add(state)
            nodes_explored += 1
            for successor, action, _ in problem.getSuccessors(state, current_direction):
                new_path = path + [action]
                new_direction = action  
                stack.push((successor, new_path, depth + 1, new_direction))
    return [], nodes_explored


def breadthFirstSearch(problem):
    queue = util.Queue()
    initial_direction = problem.initial_state.direction
    queue.push((problem.getStartState(), [], initial_direction))
    nodes_explored = 0
    visited = set()

    while not queue.isEmpty():
        state, path, current_direction = queue.pop()

        if problem.isGoalState(state):
            return path, nodes_explored

        if state not in visited:
            visited.add(state)
            nodes_explored += 1
            for successor, action, _ in problem.getSuccessors(state, current_direction):
                new_path = path + [action]
                new_direction = action
                queue.push((successor, new_path, new_direction))

    return [], nodes_explored

def actionToVector(action):
    if action == 'UP':
        return (0, -1)
    elif action == 'DOWN':
        return (0, 1)
    elif action == 'LEFT':
        return (-1, 0)
    elif action == 'RIGHT':
        return (1, 0)
    else:
        raise ValueError("Invalid action:", action)
    

def aStarSearch(problem):
    priorityQueue = util.PriorityQueue()
    initial_direction = problem.initial_state.direction
    startState = problem.getStartState()
    priorityQueue.push((startState, [], initial_direction), 0)
    nodes_explored = 0
    visited = set() 
    while not priorityQueue.isEmpty():
        state, path, current_direction = priorityQueue.pop()
        if problem.isGoalState(state):
            return path, nodes_explored
        if state not in visited:
            visited.add(state)
            nodes_explored += 1
            for successor, action, _ in problem.getSuccessors(state, current_direction):
                if successor not in visited:
                    new_path = path + [action]
                    new_direction = action
                    cost = problem.getCostOfActions(new_path) + min(manhattanDistance(successor, goal) for goal in problem.goal_states)
                    priorityQueue.push((successor, new_path, new_direction), cost)

    return []

def heuristicSearch(problem):
    priorityQueue = util.PriorityQueue()
    initial_direction = problem.initial_state.direction
    startState = problem.getStartState()
    priorityQueue.push((startState, [], initial_direction), 0)
    nodes_explored = 0
    visited = set()

    while not priorityQueue.isEmpty():
        state, path, current_direction = priorityQueue.pop()
        if problem.isGoalState(state):
            return path, nodes_explored
        if state not in visited:
            visited.add(state)
            nodes_explored += 1
            for successor, action, _ in problem.getSuccessors(state, current_direction):
                if successor not in visited:
                    new_path = path + [action]
                    new_direction = action

                    heuristic_cost = min(manhattanDistance(successor, goal) for goal in problem.goal_states)
                    priorityQueue.push((successor, new_path, new_direction), heuristic_cost)

    return []

