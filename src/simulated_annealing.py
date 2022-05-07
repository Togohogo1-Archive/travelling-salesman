from math import exp
from random import sample, random
import plotter

t0 = 1000
best_tour = []


def calc_dist(dist_from, cities):
    dist = 0

    for c1, c2 in zip(cities[1:], cities[:-1]):
        dist += dist_from[c1][c2]

    return dist


def evaluate(dist_from, x_coord, y_coord, temp):
    title = f"Temperature: {temp}, Distance: {calc_dist(dist_from, best_tour):.2f}"
    plotter.plot_path(x_coord, y_coord, best_tour, title)
    plotter.draw_path()


# Swap 2 cities
def neighbour(best_tour, city_count):
    next_tour = best_tour[:]
    a, b = sample(range(1, city_count), 2)
    next_tour[a], next_tour[b] = next_tour[b], next_tour[a]
    return next_tour


# Acceptance probability function
def metropolis(dist_from, old, new, temp):
    dist_old = calc_dist(dist_from, old)
    dist_new = calc_dist(dist_from, new)

    if dist_new <= dist_old:
        best_tour[:] = new
    elif random() < exp((dist_old-dist_new)/temp):
        print(exp((dist_old-dist_new)/temp))
        best_tour[:] = new


def temperature(x):
    return t0*exp(-0.005*x)


def run(x_coord, y_coord, dist_from, city_count):
    best_tour[:] = [0] + sample(range(1, city_count), city_count-1) + [0]
    temp = t0
    x = 0

    while temp > 0:
        temp = temperature(x)
        next_tour = neighbour(best_tour, city_count)
        metropolis(dist_from, best_tour, next_tour, temp)
        evaluate(dist_from, x_coord, y_coord, temp)
        x += 1
