from itertools import permutations as p
import plotter


def calc_dist(dist_from, cities):
    return sum(dist_from[c1][c2] for c1, c2 in zip(cities[1:], cities[:-1]))


def evaluate(new_dist, x_coord, y_coord, tour):
    title = f"Distance: {new_dist:.2f}"
    plotter.plot_path(x_coord, y_coord, tour, title)
    plotter.draw_path()


def run(x_coord, y_coord, dist_from, city_count):
    min_dist = float("inf")

    # Trying all permutations
    for ptour in p(range(1, city_count), city_count-1):
        tour = [0] + list(ptour) + [0]
        new_dist = calc_dist(dist_from, tour)

        # Found a better permutation
        if new_dist < min_dist:
            min_dist = new_dist
            evaluate(new_dist, x_coord, y_coord, tour)
