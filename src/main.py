from math import dist
from random import sample

import brute_force
import dynamic_programming
import genetic_algorithm
import plotter
import simulated_annealing

city_count = 15
max_dist = 100

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

solution = dynamic_programming.run(x_coord, y_coord, dist_from, city_count)
simulated_annealing.run(x_coord, y_coord, dist_from, city_count, solution)
plotter.show_final()
