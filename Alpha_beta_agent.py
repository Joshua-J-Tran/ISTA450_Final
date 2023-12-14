from GameState import *
class AlphaBetaAgent:
    def __init__(self, depth, evaluationFunction):
        self.depth = depth
        self.evaluationFunction = evaluationFunction
        self.nodes_explored = 0

    def getAction(self, gameState):
        self.nodes_explored = 0
        log_file = open("log.txt", "a")  

        def log(message):
            log_file.write(message + "\n")

        def max_value(gameState, alpha, beta, depth):
            self.nodes_explored += 1
            if gameState.game_over or depth == self.depth:
                return self.evaluationFunction(gameState)

            v = float("-inf")
            for action in gameState.getLegalActions("Snake"):
                new_v = value(gameState.generateSuccessor("Snake", action), alpha, beta, depth + 1, "Food")
                v = max(v, new_v)
                if v > beta:                
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(gameState, alpha, beta, depth, agent):
            self.nodes_explored += 1
            if gameState.game_over or depth == self.depth or not gameState.food_items:
                return self.evaluationFunction(gameState)
            v = float("inf")
            for action in gameState.getLegalActions(agent):
                new_v = value(gameState.generateSuccessor(agent, action), alpha, beta, depth, "Snake")
                v = min(v, new_v)
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        def value(gameState, alpha, beta, depth, agent):
            if agent == "Snake":
                return max_value(gameState, alpha, beta, depth)
            else:
                return min_value(gameState, alpha, beta, depth, agent)
            
        alpha = float("-inf")
        beta = float("inf")
        bestAction = None
        bestScore = float("-inf")

        for action in gameState.getLegalActions("Snake"):
            successorState = gameState.generateSuccessor("Snake", action)
            score = value(successorState, alpha, beta, 1, "Food")
            if score > bestScore:
                bestScore = score
                bestAction = action
            alpha = max(alpha, score)
        log(f"WTF THE BEST ACTION IS: {bestAction}")
        log_file.close() 
        return bestAction

    def getNodesExplored(self):
        return self.nodes_explored
