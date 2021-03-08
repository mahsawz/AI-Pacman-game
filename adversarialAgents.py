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
import random
import util

from game import Agent
from ghostAgents import GHOST_AGENT_MAX_DEPTH, GhostAgent


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class AdversarialSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxAgent, SmartPacmanAgent, SmartGhostAgent

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # index should be 0 by default
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def getOpponentIndex(self):
        return 1 - self.index


class MinimaxAgent(AdversarialSearchAgent):

    def getAction(self, gameState):
        """
        The Agent will receive a GameState and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        minimaxScores = []
        legalActions = gameState.getLegalActions(self.index)
        for action in legalActions:
            score = self.minimax(gameState.generateSuccessor(self.index, action), self.getOpponentIndex(), 0)
            minimaxScores.append((score, action))

        bestAction = max(minimaxScores)[1]

        return bestAction

    def minimax(self, gameState, maximizingAgent, currentDepth):

        if gameState.isLose() or gameState.isWin() or currentDepth == self.depth:
            return self.evaluationFunction(gameState)

        if maximizingAgent == self.index:  # maximize for pacman
            v = -100000
            for newState in gameState.getLegalActions(maximizingAgent):
                actions = gameState.generateSuccessor(maximizingAgent, newState)
                v = max(v, self.minimax(actions, self.getOpponentIndex(), currentDepth + 1))
            return v

        elif maximizingAgent == self.getOpponentIndex():  # minimize for agent
            v = 100000
            for newState in gameState.getLegalActions(maximizingAgent):
                actions = gameState.generateSuccessor(maximizingAgent, newState)
                v = min(v, self.minimax(actions, self.index, currentDepth + 1))
            return v


class SmartPacmanAgent(MinimaxAgent):
    def __init__(self, depth='2'):
        self.index = 0
        self.depth = int(depth)

    @staticmethod
    def evaluationFunction(gameState):

        # Calculating distance to the closest food pellet.
        Pos = gameState.getPacmanPosition()
        Food = gameState.getFood()
        FoodList = Food.asList()
        min_food_distance = -1
        for food in FoodList:
            distance = util.manhattanDistance(Pos, food)
            if min_food_distance >= distance or min_food_distance == -1:
                min_food_distance = distance

        # Calculating the distances from pacman to the ghosts.
        distances_to_ghosts = 1
        proximity_to_ghosts = 0
        for ghost_state in gameState.getGhostPositions():
            distance = util.manhattanDistance(Pos, ghost_state)
            distances_to_ghosts += distance
            if distance <= 1:
                proximity_to_ghosts += 1

        # Obtaining the number of capsules available.
        Capsule = gameState.getCapsules()
        numberOfCapsules = len(Capsule)
        foodNum = gameState.getNumFood()

        score = gameState.getScore() - 2 * float(min_food_distance) - 2 * (
                1 / float(distances_to_ghosts)) - 50 * numberOfCapsules - 10 * foodNum

        return score

class SmartGhostAgent(MinimaxAgent):
    def __init__(self, index):
        self.index = 1
        self.depth = GHOST_AGENT_MAX_DEPTH

    @staticmethod
    def evaluationFunction(gameState):
        """
        Similar to SmartPacmanAgent
        """
        Pos = gameState.getPacmanPosition()
        Food = gameState.getFood().asList()
        GhostStates = gameState.getGhostStates()
        ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

        if gameState.isLose():
            return -float("inf")
        elif gameState.isWin():
            return float("inf")

        # food distance
        foodDist = min(map(lambda x: util.manhattanDistance(Pos, x), Food))

        # number of cap
        numcap = len(gameState.getCapsules())

        # number of food left
        numfoodleft = len(Food)

        # ghost
        ghostScore = 0
        if ScaredTimes[0] > 0:
            ghostScore += 100.0  # the ghost pacman can eat
        for state in GhostStates:
            dist = manhattanDistance(Pos, state.getPosition())
            if state.scaredTimer == 0 and dist < 3:
                ghostScore -= 1.0 / (3.0 - dist);
            elif state.scaredTimer < dist:
                ghostScore += 1.0 / (dist)

        score = 1 * gameState.getScore() - (2 * foodDist) + ghostScore - (5 * numcap) - (4 * numfoodleft)

        return score


class SuperGhostAgent(GhostAgent):
    def __init__(self, index):
        self.index = index
        self.depth = GHOST_AGENT_MAX_DEPTH

    def getAction(self, gameState):
        """
        The Agent will receive a GameState and
        must return an action from Directions.{North, South, East, West}
        """
        util.raiseNotDefined()
