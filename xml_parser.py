"""
Name: xml_parser.py

Purpose: Handles loading in of the cities involved
"""

import xml.etree.ElementTree as ET
import numpy

def loadDistanceMatrix(path, num_cities):
  """
  Loads the distance matrix of the TSP problem from an .xml file

  :param path: file path of .xml file containing edge values
  :param num_cities: number of cities in current TSP
  :return: parsed distance matrix in a 2D array
  """

  # Loading the element tree into a variable
  tree = ET.parse(path)
  root = tree.getroot()

  #Initialising the costs array
  n = num_cities
  costs = numpy.full((n,n), 0).tolist()

  # Looping through each vertex
  for i in range(num_cities):

    # Looping through each edge
    for j in range(num_cities - 1):

      # Loading the cost of that edge into a variable
      edgeCost = root[5][i][j].attrib["cost"]

      # Loading the vertex that cost is for
      edgeName = int(root[5][i][j].text)

      # Splitting number and power of 10
      cost_arr = edgeCost.split("e+")
      cost_val = round(float(cost_arr[0]) * 10 ** int(cost_arr[1]))

      # Loading the cost value into the costs array 
      costs[i][edgeName] = cost_val

  return costs

#print(costs[0][1])
