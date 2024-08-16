"""
Name: heuristics.py

Purpose: Handles the probability/suitability of certain routes
"""

import numpy

def generateHeuristicMatrix(num_cities, D):
  """ 
  Generates Heuristic Matrix

  :param num_cities: number of cities in current TSP
  :param D: distance matrix
  :return: heuristics matrix generated based on distance matrix and chosen heuristic function
  """

  # Initialise heuristic matrix
  H = numpy.full((num_cities,num_cities), 0).tolist()

  # Overwriting heuristic matrix using 1/d for each edge
  for i in range(num_cities):
    for j in range(num_cities):
      if i != j:
        H[i][j] = round(1/D[i][j], 4)

  # Printing heuristic matrix
  #print('\n'.join([''.join(['{:10}'.format(item) for item in row]) for row in H]))

  return H

def removeCurNode(num_cities, H, curNode):
  """
  Sets all heuristic values that go to the current node to 0 to signify it has been visited

  :param num_cities: number of cities in current TSP
  :param H: heuristics matrix
  :param curNode: current node that has been visited
  :return: heuristics matrix with the all of the current nodes values set to 0
  """

  for i in range(num_cities):

    H[i][curNode] = 0

  return H

