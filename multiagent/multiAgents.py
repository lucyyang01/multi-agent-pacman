# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***" 

        #coefficients
        score = 0
        foodCoefficient = 1
        scaredGhostCoefficient = 3
        normalGhostCoefficient = -3.2

        #get distance from each ghost
        for newGhost in newGhostStates:
            ghostPosition = newGhost.getPosition()
            distanceToGhost = util.manhattanDistance(ghostPosition, newPos)
            isScared = newGhost.scaredTimer != 0
            #check if we have time to eat the ghost
            if(isScared and util.manhattanDistance(ghostPosition, newPos) < newGhost.scaredTimer):
                if distanceToGhost == 1 :
                    score += scaredGhostCoefficient
                else:
                    score += scaredGhostCoefficient/distanceToGhost
            else:
                if distanceToGhost == 1 or distanceToGhost == 0:
                    score -= 1000
                else:
                    score += normalGhostCoefficient/distanceToGhost
        for foodCordinates in newFood.asList():
            distanceToFood = util.manhattanDistance(newPos, foodCordinates)
            
            if distanceToFood == 1:
                score += 0.7
            else:
                score += foodCoefficient/distanceToFood
        #give a big boost if the num food is decreased after a move
        currentFood = currentGameState.getFood()
        if(len(currentFood.asList()) > len(newFood.asList())):
            score += 2 
        if((len(newGhostStates) > 0)): 
            if(len(newFood.asList()) > 1):
                chaseFoodCoefficient = 4/(len(newFood.asList()) ** 2)
            else:
                #we are at the last food
                if len(newFood.asList()) == 0:
                    return 100000
                lastFoodItem = newFood.asList()[0]
                ghostPosition = [ghosts.getPosition() for ghosts in newGhostStates]
                currMin = 1000
                minPosition = (1000, 1000)
                for position in ghostPosition:
                    if currMin > util.manhattanDistance(position, lastFoodItem):
                        minPosition = position
                    currMin = min(currMin, util.manhattanDistance(position, lastFoodItem))
                if(util.manhattanDistance(lastFoodItem, currentGameState.getPacmanPosition()) < util.manhattanDistance(minPosition, lastFoodItem)):
                    chaseFoodCoefficient = 0
                else:
                    chaseFoodCoefficient = float('inf')
        else:
            chaseFoodCoefficient = 0
        return score + chaseFoodCoefficient
        

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #for i in range(1, self.depth):
        
        
        
        return minimax(self, gameState, 0, 0, None)[1]
        

def minimax(self, gamestate, depth, indexOfPlayer, bestAction):
    if (depth == self.depth and indexOfPlayer == 0) or gamestate.isWin() or gamestate.isLose():
        # print("self.depth", self.depth)
        # print("target:" ,self.depth + 1)
        # print("actual:" ,depth)
        # print(gamestate.isWin(), gamestate.isLose())
        return (self.evaluationFunction(gamestate), bestAction)
    if indexOfPlayer == 0:
        maximumEval = -1000
        for action in gamestate.getLegalActions(indexOfPlayer):
            successorState = gamestate.generateSuccessor(indexOfPlayer, action)
            evaluation = minimax(self, successorState, depth + 1, (indexOfPlayer +1) % gamestate.getNumAgents(), action)[0]
            if maximumEval < evaluation:
                bestAction = action
            maximumEval = max(maximumEval, evaluation)
            
        return (maximumEval, bestAction)
    else:
        minimumEval = 1000
        for action in gamestate.getLegalActions(indexOfPlayer):
            successorState = gamestate.generateSuccessor(indexOfPlayer, action)
            evaluation = minimax(self, successorState, depth, (indexOfPlayer +1) % gamestate.getNumAgents(), action)[0]
            if minimumEval < evaluation:
                bestAction = action
            minimumEval = min(minimumEval, evaluation)
        return (minimumEval, bestAction)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return alphaBeta(self, gameState, 0, -10000, 10000, 0, None)[1]

def alphaBeta(self, gamestate, depth, alpha, beta, indexOfPlayer, bestAction):
    if (depth == self.depth and indexOfPlayer == 0) or gamestate.isWin() or gamestate.isLose():
        return (self.evaluationFunction(gamestate), bestAction)
    if indexOfPlayer == 0: #maximizer case
        maximumEval = -10000
        for action in gamestate.getLegalActions(indexOfPlayer):
            successorState = gamestate.generateSuccessor(indexOfPlayer, action)
            evaluation = alphaBeta(self, successorState, depth + 1, alpha, beta, (indexOfPlayer +1) % gamestate.getNumAgents(), action)[0]
            if maximumEval < evaluation:
                bestAction = action
            maximumEval = max(maximumEval, evaluation)
            alpha = max(alpha, maximumEval)
            if beta < alpha:
                break
        return (maximumEval, bestAction)
    else: #minimzer case
        minimumEval = 10000
        for action in gamestate.getLegalActions(indexOfPlayer):
            successorState = gamestate.generateSuccessor(indexOfPlayer, action)
            evaluation = alphaBeta(self, successorState, depth, alpha, beta, (indexOfPlayer +1) % gamestate.getNumAgents(), action)[0]
            if minimumEval < evaluation:
                bestAction = action
            minimumEval = min(minimumEval, evaluation)
            beta = min(minimumEval, beta)
            if beta < alpha:
                break
        return (minimumEval, bestAction)
    

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return expectimax(self, gameState, 0,  0, None)[1]

def expectimax(self, gamestate, depth, indexOfPlayer, bestAction):
    if (depth == self.depth and indexOfPlayer == 0) or gamestate.isWin() or gamestate.isLose():
        return (self.evaluationFunction(gamestate), bestAction)
    if indexOfPlayer == 0:
        maximumEval = -1000
        for action in gamestate.getLegalActions(indexOfPlayer):
            successorState = gamestate.generateSuccessor(indexOfPlayer, action)
            evaluation = expectimax(self, successorState, depth + 1, (indexOfPlayer +1) % gamestate.getNumAgents(), action)[0]
            if maximumEval < evaluation:
                bestAction = action
            maximumEval = max(maximumEval, evaluation)
            
        return (maximumEval, bestAction)
    else:
        expectedEval = 0
        for action in gamestate.getLegalActions(indexOfPlayer):
            successorState = gamestate.generateSuccessor(indexOfPlayer, action)
            # computes the average evaluation out of all outcomes for the successor states.
            expectedEval += 1/(len(gamestate.getLegalActions(indexOfPlayer))) *  expectimax(self, successorState, depth, (indexOfPlayer +1) % gamestate.getNumAgents(), action)[0]
            # in the spec, they say that the ghosts take random actions, this is why I thought we should return a random action instead of 'bestAction'.
        
        return (expectedEval, random.choice(gamestate.getLegalActions(indexOfPlayer)))

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    score = 0
    foodCoefficient = 1
    scaredGhostCoefficient = 2
    normalGhostCoefficient = -3.2
    #eval ghost states
    for newGhost in ghostStates:
        ghostPosition = newGhost.getPosition()
        distanceToGhost = util.manhattanDistance(ghostPosition, position)
        isScared = newGhost.scaredTimer != 0
        #check if we have time to eat the ghost
        if(isScared and util.manhattanDistance(ghostPosition, position) < newGhost.scaredTimer):
            if distanceToGhost == 1 :
                score += scaredGhostCoefficient
            else:
                score += scaredGhostCoefficient/(distanceToGhost)
        else:
            if distanceToGhost == 1 or distanceToGhost == 0:
                score -= 1000
            else:
                score += normalGhostCoefficient/distanceToGhost
    #eval food list
    if len(food.asList()) == 0:
            return 100000
    #reward for shorter food list
    score += 10/(len(food.asList()) ** 2) * 100
    return score


# Abbreviation
better = betterEvaluationFunction
