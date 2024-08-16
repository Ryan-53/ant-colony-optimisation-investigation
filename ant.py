"""
Name: ant.py

Purpose: Contains function for the run of an ant around the map of cities
"""

from heuristics import *
from transition import *

def antRun(num_cities, D, curNode, T, alpha, beta):
  """
  A single run of a single ant

  :param num_cities: number of cities in current TSP
  :param D: distance matrix
  :param curNode: current node that has been visited
  :param T: pheromone matrix
  :param originalH: heurstics matrix
  :param alpha: selected alpha value
  :param beta: selected beta value
  :return: list of route taken with length of route at the last index (14)
  """

  cost = 0
  route = [0] * (num_cities + 1)

  # Generate Heuristic Matrix
  H = generateHeuristicMatrix(num_cities, D)

  for i in range(num_cities):

    # Remove current node from allowed nodes within heuristics matrix to show it has been visited
    H = removeCurNode(num_cities, H, curNode)

    # Generate Transition Probabilities for all cities from current node
    P = computeTranProb(num_cities, H, curNode, T, alpha, beta)

    # Select next city to move to based on transition probabilities
    city_chosen = selectNode(num_cities, P)

    # Adds distance value to next node chosen to total cost of route so far
    cost += D[curNode][city_chosen]

    # Adds node visited to list of route taken
    route[i] = curNode
    curNode = city_chosen

  route[num_cities] = cost

  return route