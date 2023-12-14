class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        "*** YOUR CODE HERE ***"
        def max_value(gameState, alpha, beta, depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
                return self.evaluationFunction(gameState)

            v = float("-inf")
            legalActions = gameState.getLegalActions(0)

            for action in legalActions:
                v = max(v, value(gameState.generateSuccessor(0, action), alpha, beta, depth + 1))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(gameState, alpha, beta, depth, agentIndex):
            if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
                return self.evaluationFunction(gameState)

            v = float("inf")
            legalActions = gameState.getLegalActions(agentIndex)

            for action in legalActions:
                v = min(v, value(gameState.generateSuccessor(agentIndex, action), alpha, beta, depth + 1))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        def value(gameState, alpha, beta, depth):
            agentIndex = depth % gameState.getNumAgents()
            if agentIndex == 0:  
                return max_value(gameState, alpha, beta, depth)
            else:
                return min_value(gameState, alpha, beta, depth, agentIndex)

        alpha = float("-inf")
        beta = float("inf")
        bestAction = None
        bestScore = float("-inf")

        for action in gameState.getLegalActions(0):  
            successorState = gameState.generateSuccessor(0, action)
            score = value(successorState, alpha, beta, 1)
            if score > bestScore:
                bestScore = score
                bestAction = action
            alpha = max(alpha, score)
        return bestAction
