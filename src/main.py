from pprint import pp, pprint
from math import dist
from random import sample
import plotter
import genetic_algorithm
import brute_force
import dp

city_count = 10
max_dist = 1000

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

# pprint(dist_from)
print(x_coord[0], y_coord[0])
brute_force.run(x_coord, y_coord, dist_from, city_count)
plotter.show_final()
