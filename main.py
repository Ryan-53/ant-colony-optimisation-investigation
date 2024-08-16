"""
Name: main.py

Purpose: Runs different Ant Colony experiment runs
"""

from xml_parser import *
from heuristics import *
from transition import *
from pheromone import *
from ant import *
import numpy
import random

### Setting up variables ###

# Initial values
# _ used instead of camelCase to signify this is a value modifiable by the
# user for experimentation
num_cities = 14 ##### EDIT THIS NUMBER WHEN CHANGING XML FILE ####
num_ants = 75
starting_node = 0 # Replaced with random
intial_pheromone = 1
num_iterations = int(10000/num_ants)

# Constants - These can also be modified for experimentation
alpha = 0.5 # Rate used in transition probability
beta = 3 # Another rate used in transition probability
rho = 0.5 # Evaporation rate
Q = 3

# Current node - Initialises starting node as random
curNode =  random.randint(0, num_cities - 1)


# Loads in distance matrix 
#### COMMENT ONE AND UNCOMMENT THE OTHER TO SWITCH BETWEEN XML FILES ####
D = loadDistanceMatrix("distance_matrices/burma14.xml", 14)
#D = loadDistanceMatrix('distance_matrices/brazil58.xml', 58)

# Initialise pheromone matrices
T = numpy.full((num_cities, num_cities), intial_pheromone).tolist()
Tn = numpy.full((num_cities, num_cities), intial_pheromone).tolist()

# Initialise best route list
bestRoute = [9999999999] * (num_cities + 1)

# Initialise global best (for MMAS)
globalbest = [9999999999] * (num_cities + 1)

### ###


### Standard Ant colony run ###
"""
# Loops for a certain number of iterations
for i in range(num_iterations):

  if not i % 20:
    print((i/num_iterations) * 100, "%")

  # Evaporates pheromones by rho for next iteration
  Tn = evaporatePheromones(num_cities, T, rho, 0, 1)

  # Randomise starting node per iteration
  #curNode =  random.randint(0, num_cities - 1)

  # Loops for a certain number of ants per iteration
  for j in range(num_ants):

    # Randomise starting node per ant
    curNode =  random.randint(0, num_cities - 1)

    # Sends a single ant on 1 run of the TSP
    route = antRun(num_cities, D, curNode, T, alpha, beta)

    # Deposits pheromones on phermone matrix of next iteration
    Tn = depositPheromones(num_cities, Tn, route, Q)

    # Compares route to best route in this current run and if it is the best, it is recorded
    if route[num_cities] < bestRoute[num_cities]:
      bestRoute = route

  T = Tn
"""
### ###



### MMAS Ant colony run (only iteration best tour lays pheromones) ###
"""
pheromone_min = 0.4
pheromone_max = 0.9

T = numpy.full((num_cities, num_cities), pheromone_max).tolist()
Tn = numpy.full((num_cities, num_cities), pheromone_max).tolist()

# Loops for a certain number of iterations
for i in range(num_iterations):

  if not i % 20:
    print((i/num_iterations) * 100, "%")

  # Evaporates pheromones by rho for next iteration
  Tn = evaporatePheromones(num_cities, T, rho, pheromone_min, pheromone_max)

  # Resets best route so it can be calculated again
  bestRoute = [9999999999] * (num_cities + 1)

  # Loops for a certain number of ants per iteration
  for j in range(num_ants):
  
    # Randomise starting node per ant
    curNode =  random.randint(0, num_cities - 1)

    # Sends a single ant on 1 run of the TSP
    route = antRun(num_cities, D, curNode, T, alpha, beta)

    # Compares route to best route in this current run and if it is the best, it is recorded
    if route[num_cities] < bestRoute[num_cities]:
      bestRoute = route

  if bestRoute[num_cities] < globalbest[num_cities]:
    globalbest = bestRoute

  # Deposits pheromones on phermone matrix of only best run for this iteration
  Tn = depositPheromones(num_cities, Tn, bestRoute, Q)

  T = Tn

bestRoute = globalbest
"""
### ###



### Elitist Ant colony run ###
"""
# Loops for a certain number of iterations
for i in range(num_iterations):

  if not i % 20:
    print((i/num_iterations) * 100, "%")

  # Evaporates pheromones by rho for next iteration
  Tn = evaporatePheromones(num_cities, T, rho, 0, 1)


  # Loops for a certain number of ants per iteration
  for j in range(num_ants):
  
    # Randomise starting node per ant
    curNode =  random.randint(0, num_cities - 1)

    # Sends a single ant on 1 run of the TSP
    route = antRun(num_cities, D, curNode, T, alpha, beta)

    # Compares route to best route in this current run and if it is the best, it is recorded
    if route[num_cities] < bestRoute[num_cities]:
      bestRoute = route

  # Deposits pheromones on phermone matrix of only global best run so far
  Tn = depositPheromones(num_cities, Tn, bestRoute, Q)

  T = Tn
"""
### ###



### Rank-Based - ASrank ### ----------------- BEST ALGORITHM -----------------

# Number of best ants that can lay pheromones
num_rank = 5

# Loops for a certain number of iterations
for i in range(num_iterations):

  if not i % 20:
    print(int((i/num_iterations) * 100), "%")

  # Evaporates pheromones by rho for next iteration
  Tn = evaporatePheromones(num_cities, T, rho, 0, 1)

  # Resets best route so it can be calculated again
  bestRoute = [9999999999] * (num_cities + 1)

  # Resets best route array so it can be calculated again
  bestIterRoute = numpy.full((num_cities + 1, num_rank), 99999999).tolist()


  # Loops for a certain number of ants per iteration
  for j in range(num_ants):

    # Randomise starting node per ant
    curNode =  random.randint(0, num_cities - 1)

    # Sends a single ant on 1 run of the TSP
    route = antRun(num_cities, D, curNode, T, alpha, beta)

    # Compares route to best route in this current run and if it is the best, it is recorded
    for p in range(num_rank):
      if route[num_cities] < bestIterRoute[num_cities][p]:

        # Copying route, index by index, into the ranked list
        for q in range(num_cities + 1):
          bestIterRoute[q][p] = route[q]
        break
  
  # Compares iteration best to global best, overwriting if better
  if bestIterRoute[num_cities][0] < globalbest[num_cities]:
    
    # Copying route, index by index, into the global best
    for q in range(num_cities + 1):
      globalbest[q] = bestIterRoute[q][0]

  # Deposits pheromones on phermone matrix of only best (num_rank) runs for this iteration
  for p in range(num_rank):

    # Copying each row of the best ranked ants, so they can each deposit pheromones
    for q in range(num_cities + 1):
      bestRoute[q] = bestIterRoute[q][p]

    # Deposits pheromones of that particular route within the ranked list of top (num_rank) ants
    Tn = depositPheromones(num_cities, Tn, bestRoute, Q)

  # Sets Pheromone matrix as updated version with newly layed pheromone values
  T = Tn

# Sets global best of all iterations to bestRoute so it can be output
bestRoute = globalbest

### ###



### Printing best route and cost ###

bestRoutePath = [0] * (num_cities)

for i in range(num_cities):
  bestRoutePath[i] = bestRoute[i]

bestRouteCost = bestRoute[num_cities]

print("The best route is: ", bestRoutePath)

print("Cost = ", bestRouteCost)

