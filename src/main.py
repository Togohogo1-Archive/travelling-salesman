from math import dist
from random import sample

import brute_force
import dynamic_programming
import genetic_algorithm
import plotter
import simulated_annealing

city_count = 5
max_dist = 10

# Initializing coordinates
x_coord = sample(range(1, max_dist), city_count)
y_coord = sample(range(1, max_dist), city_count)

dist_from = [[None]*city_count for _ in range(city_count)]

# Initializing distance array
for c1 in range(city_count):
    for c2 in range(city_count):
        c1_point = (x_coord[c1], y_coord[c1])
        c2_point = (x_coord[c2], y_coord[c2])
        dist_from[c1][c2] = dist(c1_point, c2_point)

# Casebreaker
dist_from = [
    [0, 1, 2, 1, 8],
    [1, 0, 1, 2, 3],
    [2, 1, 0, 7, 3],
    [1, 2, 7, 0, 8],
    [8, 3, 3, 8, 0]
]

dynamic_programming.run(x_coord, y_coord, dist_from, city_count)
brute_force.run(x_coord, y_coord, dist_from, city_count)
plotter.show_final()
