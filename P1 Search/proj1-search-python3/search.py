#!/usr/bin/env python3

# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    #print("Start:", problem.getStartState())
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    closed = util.Stack()
    fringe = util.Stack()
    fringe.push((problem.getStartState(), 'Start', 0))
    node = util.Stack()
    node.push((problem.getStartState(), 'Start', 0))
    
    while True:
        
        " Check if fringe is empty "
        if fringe.isEmpty():
            print("Empty set - FAILURE")
            util.raiseNotDefined()
        
        " Add to NODE  "
        if not fringe.list[-1][1] == 'Start':
            node.push(fringe.list[-1])
        #print('NODE: ', node.list)
         
        " Check if we have reached the goal " 
        if problem.isGoalState(node.list[-1][0]):
            #print('WIN!!!!!!!!!!')
            answerTMP = util.Stack()
            answer = util.Stack()
            
            "Clean results to get direct path"
            if len(problem.getStartState())>1:  # ORGANIZE COORDINATES
                print("modo numeros")
                for result in reversed(node.list):
                    if len(answerTMP.list) == 0:
                        answerTMP.push(result)
                    else:
                        if util.manhattanDistance(result[0], answerTMP.list[-1][0]) == 1:
                            answerTMP.push(result)
                answerTMP.pop()
                
            else:                               # ORGANIZE LETTERS
                print("modo letras")
                
                for result in reversed(node.list):
                    if len(answerTMP.list) == 0:
                        answerTMP.push(result)
                    else:
                        if answerTMP.list[-1][1].find(result[0]) >0:
                            answerTMP.push(result)
                answerTMP.pop()
                
            while len(answerTMP.list)>0:        # REVERSE BACK
                answer.push(answerTMP.list[-1][1])
                answerTMP.pop()
            print("ANSWER", answer.list) 
            return  answer.list
        
        " Check if node element is in closed and expand"
        if not node.list[-1][0] in closed.list:
            closed.push(node.list[-1][0])
            fringe.pop()
            
            for child in problem.getSuccessors(node.list[-1][0]):
                #print('CHILD: ', child)
                if not child[0] in closed.list:
                    fringe.push(tuple(child))
            #print('FRINGE: ', fringe.list)
        else:
            print('ALREADY EXPANDED')
            closed.push(node.list[-1][0])
            fringe.pop()
            node.pop()
            
    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    closed = util.Stack()
    fringe = util.Queue()
    fringe.push((problem.getStartState(), [], 0))
    node = []
    path = list([])
    
    while True:
        
        #print("Closed: ", closed.list)
        #print("Fringe: ", fringe.list)
        
        " ***********************************Check if fringe is empty************************************* "
        if fringe.isEmpty():
            print("Empty set - FAILURE")
            util.raiseNotDefined()
        
        " ****************************************Add to NODE********************************************* "
        node, path, weight = list(fringe.pop())
        #print('NODE: ', node)
         
        " *******************************Check if we have reached the goal ******************************* " 
        if problem.isGoalState(node):
            print('WIN!!!!!!!!!!')
            print("ANSWER", (path))          
            return  path
        
        " *******************************************Add to expanded list********************************* "
        
        if not node in closed.list:
            closed.push(node)
        
            " *****************************Check if node element is in closed and expand********************** "
            for child in problem.getSuccessors(node):
                
                if not child[0] in closed.list:
                    #print(type(path), path)
                    new = list((child[0], path + [child[1]], child[2] ))
                    #print("NEW", new)
                    fringe.push(new)
    
    
    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    
    #print("Start:", problem.getStartState())
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    closed = util.Stack()
    fringe = util.PriorityQueue()
    fringe.push((problem.getStartState(), [], 0), 0)
    node = []
    path = []
    weight = []
    
    priority = list(((0,0), 0, 0))
    
    #print("FRINGE", fringe.heap)
    
    
    while True:
        
        " ***********************************Check if fringe is empty************************************* "
        if fringe.isEmpty():
            print("Empty set - FAILURE")
            util.raiseNotDefined()
        
        " ****************************************Add to NODE********************************************* "
        
        #print("NODE", node.list[-1][1])
        node, path, weight = fringe.pop()
        #print("LIST", node)
        
        " *******************************Check if we have reached the goal ******************************* " 
  
        if problem.isGoalState(node):
            print('WIN!!!!!!!!!!')
            #print("ANSWER", (answer.list))          
            return  path
        
        " *******************************************Add to expanded list********************************* "
        if not node in closed.list:
            closed.push(node)
        
            " *****************************Check if node element is in closed and expand********************** "
        
            for child in problem.getSuccessors(node):
                if not child[0] in closed.list:
                    #print("CHLD:", (child))
                    #print("LIST:", closed.list)
                    priority =   weight + child[2]
                    fringe.update((child[0], path + [child[1]], priority ), priority)
                #else:
                    #print("hola")
        
        
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    closed = util.Stack()
    fringe = util.PriorityQueue()
    fringe.push((problem.getStartState(), [], heuristic(problem.getStartState(), problem)), 0)
    node = []
    path = []
    weight = []
    
    priority = list(((0,0), 0, 0))
    
    while True:
        
        " ***********************************Check if fringe is empty************************************* "
        if fringe.isEmpty():
            print("Empty set - FAILURE")
            util.raiseNotDefined()
        
        " ****************************************Add to NODE********************************************* "

        node, path, weight = fringe.pop()
        
        
        " *******************************Check if we have reached the goal ******************************* " 
        
        if problem.isGoalState(node):
            print('WIN!!!!!!!!!!')
            #print("ANSWER", (answer.list))          
            return  path
        
        " *******************************************Add to expanded list********************************* "

        if not node in closed.list:
            closed.push(node)
        
            " *****************************Check if node element is in closed and expand********************** "
            
            for child in problem.getSuccessors(node):
                
                if not child[0] in closed.list:
                    
                    h  = heuristic(child[0], problem)
                    priority =   weight + child[2] + h
                    fringe.update((child[0], path + [child[1]], weight + child[2] ), priority)
    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
