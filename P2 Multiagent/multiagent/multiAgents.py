#!/usr/bin/env python3

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

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        lastMove = ""
        
        
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        
        #print("Scores:", scores, legalMoves, legalMoves[chosenIndex])
        #print(lastMove.direction(), legalMoves)
        
        if lastMove in legalMoves:
            #print ("1:", lastMove)
            return lastMove
        else:
            lastMove = legalMoves[chosenIndex]
            #print ("2:", lastMove)
            return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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
        
        #for space in successorGameState:
        #    if space == "G":
        #        print(space)
        #print(newGhostStates[0], newGhostStates[1])
        
        nearest = 10
        scary = 0
        
        if not action == "Stop":
            for food in newFood.asList():
                nearest = min(nearest , util.manhattanDistance(food, newPos))
                #print(nearest)
                
        for ghost in newGhostStates:
                if util.manhattanDistance(ghost.getPosition(), newPos) <= 3 and ghost.scaredTimer == 0:
                    scary = 1000000
        
        #print(successorGameState.getScore())

        "*** YOUR CODE HERE ***"
        return 0 - nearest + successorGameState.getScore() - scary

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        
        
        def maximizer(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            
            score = -100000000
            
            #print ("Agent:", agentIndex, gameState.getNumAgents())
            for action in gameState.getLegalActions(agentIndex):
                #print("Action:", action)
                score = max(score, minimizer(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1  ))
            
            return score
            
        def minimizer(gameState, depth, agentIndex):
            
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            
            score = 100000000
            
            #print ("Agent:", agentIndex, gameState.getNumAgents())
            if agentIndex == gameState.getNumAgents() - 1:
                for action in gameState.getLegalActions(agentIndex):
                    score = min(score, maximizer(gameState.generateSuccessor(agentIndex, action), depth + 1, 0  ))
            else:
                for action in gameState.getLegalActions(agentIndex):
                    score = min(score, minimizer(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1  ))
            return score
    
        direction = ""
        first = 0
        maxScore = -1000000000
        
        for action in gameState.getLegalActions(0):
            
            score = minimizer(gameState.generateSuccessor(0, action), 0, 1)
            #print("Score:", score)
            
            if score > maxScore:
                maxScore = score
                direction = action
        
        #print("Player:", player )
        return direction
        util.raiseNotDefined()
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maximizer(gameState, depth, agentIndex, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            
            score = -100000000
            
            #print ("Agent:", agentIndex, gameState.getNumAgents())
            for action in gameState.getLegalActions(agentIndex):
                #print("Action:", action)
                score = max(score, minimizer(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta))
                if score > beta:
                    return score
                alpha = max(alpha, score)
                
            return score
            
        def minimizer(gameState, depth, agentIndex, alpha, beta):
            
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            
            score = 100000000
            
            #print ("Agent:", agentIndex, gameState.getNumAgents())
            if agentIndex == gameState.getNumAgents() - 1:
                for action in gameState.getLegalActions(agentIndex):
                    score = min(score, maximizer(gameState.generateSuccessor(agentIndex, action), depth + 1, 0, alpha, beta))
                    if score < alpha:
                        return score
                    beta = min(beta, score)
            else:
                for action in gameState.getLegalActions(agentIndex):
                    score = min(score, minimizer(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta))
                    if score < alpha:
                        return score
                    beta = min(beta, score)
            return score
    
        direction = ""
        first = 0
        maxScore = -1000000000
        alpha = -100000000
        beta = 100000000
        
        for action in gameState.getLegalActions(0):
            
            score = minimizer(gameState.generateSuccessor(0, action), 0, 1, alpha, beta)
            #print("Score:", score)
            
            if score > maxScore:
                maxScore = score
                direction = action
            alpha = max(alpha, score)
        #print("Player:", player )
        return direction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        def maximizer(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            
            score = -100000000
            
            #print ("Agent:", agentIndex, gameState.getNumAgents())
            for action in gameState.getLegalActions(agentIndex):
                #print("Action:", action)
                score = max(score, minimizer(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1  ))
            
            return score
            
        def minimizer(gameState, depth, agentIndex):
            
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            
            score = 0
            count = 0
            
            #print ("Agent:", agentIndex, gameState.getNumAgents())
            if agentIndex == gameState.getNumAgents() - 1:
                for action in gameState.getLegalActions(agentIndex):
                    score = score + maximizer(gameState.generateSuccessor(agentIndex, action), depth + 1, 0  )
                    count += 1
            else:
                for action in gameState.getLegalActions(agentIndex):
                    score = score + minimizer(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1  )
                    count += 1
            
            
            
            return score / count
    
        direction = ""
        first = 0
        maxScore = -1000000000
        
        for action in gameState.getLegalActions(0):
            
            score = minimizer(gameState.generateSuccessor(0, action), 0, 1)
            #print("Score:", score)
            
            if score > maxScore:
                maxScore = score
                direction = action
        
        #print("Player:", player )
        return direction
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    
    I started just like in 1 assigning a value based on distance to nearest food and using my "scary" variable for running away from ghosts was working very well
    But I wanted to incentivise the Capsules, and eating the ghosts, I realized that my algorythm wasnt working because when Pacman = Capsule or Ghost, the item dissapears from the list
    I tied a few things, but I pacman wouldnt eat them, so I just focused on the scared times instead and cleared with 1000pts, but I'm still not sure how I could improve the eating Ghosts incentive
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
        #successorGameState = currentGameState.generatePacmanSuccessor(action
    
    
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    Capsules = currentGameState.getCapsules()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    
    
    finalScore = 0
    nearestFood = 20
    nearestCapsule = 20
    scary = 0.0
    win = 0
    
    #print("Pacman: ", Pos)
    
    for food in Food.asList():
        nearestFood = min(nearestFood, util.manhattanDistance(food, Pos) )
        #print("Food", food)
    
    """
    for capsule in Capsules:
        nearestCapsule = min(nearestCapsule, util.manhattanDistance(capsule, Pos) ) +1
        
        if util.manhattanDistance(capsule, Pos) <= 5:
            scary = 500 / (util.manhattanDistance(capsule, Pos) +1)
    """  
      
    for ghost in GhostStates:
        if util.manhattanDistance(ghost.getPosition(), Pos) <= 2 and ghost.scaredTimer == 0:
            scary = -1000000 / (util.manhattanDistance(ghost.getPosition(), Pos) + 1)
        #elif util.manhattanDistance(ghost.getPosition(), Pos) <= 3 and ghost.scaredTimer > 0:
        #    scary = 10000000 / (util.manhattanDistance(ghost.getPosition(), Pos) + 1)
            #print(scary)
         
    """   
    if currentGameState.isWin():
        win = 10000000
    elif currentGameState.isLose():
        win = -10000000
    """
    
    #print("Nearest Food:, ", nearestFood)
    #print("Nearest Capsule:, ", nearestCapsule)
    
    finalScore = currentGameState.getScore() + (1.0/float(nearestFood + 1))  * (sum(ScaredTimes) + 1) + scary 
    
    #print("score 2:", finalScore)
    return finalScore

# Abbreviation
better = betterEvaluationFunction
