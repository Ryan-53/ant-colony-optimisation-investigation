"""
Name: transition.py

Purpose: Handles deciding what route to traverse for an ant
"""

import random

def computeTranProb(num_cities, H, curNode, T, alpha, beta):
  """
  Computes the transition probabilites from a specified node

  :param num_cities: number of cities in current TSP
  :param H: heuristics matrix
  :param curNode: current node that has been visited
  :param T: pheromone matrix
  :param alpha: selected alpha value
  :param beta: selected beta value
  :return: List of transition probabilities for every node from that node
  """

  # Initialises list of unscaled transition values
  N = [None] * num_cities

  # Initialises list of transition probabilities
  P = [None] * num_cities

  # Total probability
  tot = 0

  # Calculating unscaled transition values
  for j in range(num_cities):
    N[j] = T[curNode][j] ** alpha * H[curNode][j] ** beta
    tot += N[j]

  # Calculating scaled transition probabilities
  for j in range(num_cities):
    if N[j] == 0:
      P[j] = 0
    else:
      P[j] = N[j]/tot

  return P

def selectNode(num_cities, P):
  """
  Selects next node to traverse to

  :param num_cities: number of cities in current TSP
  :param P: transition probabilities
  :return: node selected to traverse to
  """

  # Calculates a random number from 0-1
  rand = random.random()

  # Initialises cumulative probability
  CP = 0

  # Initialises to prevent error
  cityChosen = 0
  
  # Adds probability of each node until the total is more than the random number
  for j in range(num_cities):

    CP += P[j]

    # When the total probability is more than the random number, assign the node 
    # which was the most recently added probability as the node to be chosen.
    if CP >= rand:
      cityChosen = j
      break

  return cityChosen