# TODO check if roulette and sus are legit
# TODO better mutation algorithm

from ctypes import pointer
from itertools import accumulate
from dataclasses import dataclass, field
from random import random, sample, choice, uniform
from threading import main_thread

from dna import DNA
import plotter

@dataclass
class Population:
    pop_size: int
    mutation_rate: float
    generation: int = 0
    population: list[DNA] = field(default_factory=list)
    mating_pool: list[DNA] = field(default_factory=list)
    best: list[int] = field(default_factory=list)

    def calc_fitness(self, dist_from, cities):
        dist = 0

        for c1, c2 in zip(cities[1:], cities[:-1]):
            dist += dist_from[c1][c2]

        return dist

    # Generate random population of individual tours
    def initialize(self, dist_from, city_count):
        for _ in range(self.pop_size):
            tour = [0] + sample(range(1, city_count), city_count-1) + [0]
            tour_dist = self.calc_fitness(dist_from, tour)
            self.population.append(DNA(tour_dist, tour))

    # Determines if the termination condition has been met
    def evaluate(self, x_coord, y_coord):
        print(len(self.mating_pool))
        plotter.plot_path(x_coord, y_coord, self.best)
        plotter.draw_path()
        return False  # Not met

    # Creating children chromosomes from parents
    def crossover(self, dist_from, city_count):
        for i in range(self.pop_size):
            parent1 = choice(self.mating_pool)
            parent2 = choice(self.mating_pool)
            offspring = parent1.cross(parent2, city_count)
            child = DNA(self.calc_fitness(dist_from, offspring), offspring)

            # Mutations refer to accidental errors when copying genetic information from parents
            child.mutate(self.mutation_rate, city_count)
            self.population[i] = child

    # Mating pool of selected individuals creates a new population
    def select(self):
        self.roulette_wheel_selection()

    def roulette_wheel_selection(self):
        self.mating_pool = []

        longest_tour = max(self.population).fitness
        shortest_tour = min(self.population).fitness

        for dna in self.population:
            # Smaller distances are optimal
            norm_fitness = 1 - self.normalize(dna.fitness, shortest_tour, longest_tour)

            # Better than adding multiple of the same elements in the mating pool
            if random() < norm_fitness:
                self.mating_pool.append(dna)

        self.best = min(self.mating_pool).genes

    # Implementation from https://en.wikipedia.org/wiki/Stochastic_universal_sampling
    def stochastic_universal_sampling(self):
        self.mating_pool = []
        fitness_psa = []

        self.population.sort()
        longest_tour = self.population[-1].fitness
        shortest_tour = self.population[0].fitness

        sample_size = 250
        total_fitness = sum(1-self.normalize(dna.fitness, shortest_tour, longest_tour) for dna in self.population)
        fitness_psa = [0] + list(accumulate(1-self.normalize(dna.fitness, shortest_tour, longest_tour) for dna in self.population))
        pointer_dist = total_fitness / sample_size
        start = uniform(0, pointer_dist)

        # Pointers
        for i in range(sample_size-1):
            ii = 0
            pointer_loc = start + i*pointer_dist

            # Range query, use <= when the pointer is at the edge
            while fitness_psa[ii+1] - fitness_psa[0] <= pointer_loc:
                ii += 1

            self.mating_pool.append(self.population[ii])

        self.best = min(self.mating_pool).genes

    def tournament_selection(self):
        self.mating_pool = []

        tournament_size = 20
        tournaments = 1000

        for _ in range(tournaments):
            tourney = sorted(sample(self.population, tournament_size))
            self.mating_pool.append(min(tourney))  # Best of each tournament

        self.best = min(self.mating_pool).genes

    def truncation_selection(self):
        truncation_size = 100  # Top n members
        self.population.sort()
        self.mating_pool = self.population[:truncation_size]
        self.best = self.mating_pool[0].genes

    # Normalizing the values to fit [old_lo, old_hi] to [0, 1]
    def normalize(self, val, old_lo, old_hi):
        if old_hi - old_lo == 0:
            return 0

        return (val-old_lo) / (old_hi-old_lo)
