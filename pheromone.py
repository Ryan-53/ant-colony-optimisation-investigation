"""
Name: pheremone.py

Purpose: Handles pheremones deposited by ants to indicate where they have been
"""

def evaporatePheromones(num_cities, T, rho, min, max):
  """
  Reduces the current pheromones by the value of rho

  :param num_cities: number of cities in current TSP
  :param T: pheromone matrix
  :param rho: evaporation rate
  :param min: minimum pheromone value allowed
  :param max: maximum pheromone value allowed
  :return: updated pheromone matrix with some pheromones evaporated
  """

  for i in range(num_cities):

    for j in range(num_cities):

      T[i][j] = (1 - rho) * T[i][j]

      if T[i][j] < min:
        T[i][j] = min
      elif T[i][j] > max:
        T[i][j] = max


  return T

def depositPheromones(num_cities, T, route, Q):
  """
  Adds pheromones to pheromone matrix where the ant has travelled

  :param num_cities: number of cities in current TSP
  :param T: pheromone matrix
  :param route: list of route the ant has taken with cost at the end of the list
  :param Q: constant used to compute the delta (determines how much pheromone to deposit)
  :return: updated pheromone matrix with the ants pheromones deposited
  """

  # Gets the total cost of that route
  cost = route[num_cities]

  # Value added to pheromones on path
  delta = Q/cost # Perhaps this could be a higher value than 1 to increase pheromones

  for i in range(num_cities - 1):

    T[route[i]][route[i + 1]] += delta

  return T