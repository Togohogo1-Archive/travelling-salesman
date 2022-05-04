from itertools import permutations as p
import plotter


def calc_dist(dist_from, cities):
    dist = 0

    for c1, c2 in zip(cities[1:], cities[:-1]):
        dist += dist_from[c1][c2]

    return dist


def run(x_coord, y_coord, dist_from, city_count):
    min_dist = float("inf")

    for ptour in p(range(1, city_count), city_count-1):
        tour = [0] + list(ptour) + [0]
        new_dist = calc_dist(dist_from, tour)

        if new_dist < min_dist:
            min_dist = new_dist

            # Debug
            # print(min_dist, tour)

            # Plotting
            plotter.plot_path(x_coord, y_coord, tour)
            plotter.draw_path()

    return "final", min_dist, tour
