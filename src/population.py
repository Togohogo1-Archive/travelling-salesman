from dataclasses import dataclass, field
from itertools import accumulate
from random import choice, random, sample, uniform

import plotter
from dna import DNA


@dataclass
class Population:
    pop_size: int
    mutation_rate: float
    generation: int = 0
    population: list[DNA] = field(default_factory=list)
    mating_pool: list[DNA] = field(default_factory=list)
    best: list[int] = field(default_factory=list)

    def calc_fitness(self, dist_from, cities):
        return sum(dist_from[c1][c2] for c1, c2 in zip(cities[1:], cities[:-1]))

    # Generates random population of individual tours
    def initialize(self, dist_from, city_count):
        for _ in range(self.pop_size):
            tour = [0] + sample(range(1, city_count), city_count-1) + [0]
            tour_dist = self.calc_fitness(dist_from, tour)
            self.population.append(DNA(tour_dist, tour))

    def evaluate(self, dist_from, x_coord, y_coord, solution):
        self.generation += 1  # Initial state is generation 0
        title = f"Generation: {self.generation}, Distance: {self.calc_fitness(dist_from, self.best):.2f}"
        plotter.plot_path(x_coord, y_coord, self.best, title, solution)
        plotter.draw_path()

    # Creating children chromosomes from parents
    def crossover(self, dist_from, city_count):
        for i in range(self.pop_size):
            parent1 = choice(self.mating_pool)
            parent2 = choice(self.mating_pool)
            offspring = parent1.cross(parent2, city_count)  # Intermediate step, tour
            child = DNA(self.calc_fitness(dist_from, offspring), offspring)

            child.mutate(self.mutation_rate, city_count)
            self.population[i] = child  # Overwriting population with offspring

    # Mating pool of selected individuals creates a new population
    def select(self):
        self.roulette_wheel_selection()

    def roulette_wheel_selection(self):
        self.mating_pool = []

        longest_tour = max(self.population).fitness
        shortest_tour = min(self.population).fitness

        for dna in self.population:
            # Smaller distances have larger fitness
            norm_fitness = 1 - self.normalize(dna.fitness, shortest_tour, longest_tour)

            # Chance of being selected determined by normalized fitness values, doesn't require extra space complexity
            if random() < norm_fitness:
                self.mating_pool.append(dna)

        self.best = min(self.mating_pool).genes

    # Source: https://en.wikipedia.org/wiki/Stochastic_universal_sampling
    def stochastic_universal_sampling(self):
        self.mating_pool = []

        self.population.sort()
        longest_tour = self.population[-1].fitness
        shortest_tour = self.population[0].fitness

        sample_size = 250
        total_fitness = sum(1-self.normalize(dna.fitness, shortest_tour, longest_tour) for dna in self.population)  # Normalizing to work for different city distances
        fitness_psa = [0] + list(accumulate(1-self.normalize(dna.fitness, shortest_tour, longest_tour) for dna in self.population))
        pointer_dist = total_fitness / sample_size  # Pointers distributed evenly across population
        start = uniform(0, pointer_dist)  # Starting at `start` equivalent to starting at `start` + multiple of `pointer_dist`

        # Looping by pointers
        for i in range(sample_size-1):
            ii = 0
            pointer_loc = start + i*pointer_dist

            # First n DNA can be represented by ratio - sum of normalized values up to nth element : `total_fitness`
            # Use <= when the pointer is at the edge
            while fitness_psa[ii+1] - fitness_psa[0] <= pointer_loc:
                ii += 1  # Let the current DNA, `self.population[ii]`, "catch up" to current pointer

            self.mating_pool.append(self.population[ii])

        self.best = min(self.mating_pool).genes

    def tournament_selection(self):
        self.mating_pool = []

        tournament_size = 20
        tournaments = 1000

        for _ in range(tournaments):
            tourney = sample(self.population, tournament_size)
            self.mating_pool.append(min(tourney))  # Best of each tournament

        self.best = min(self.mating_pool).genes

    def truncation_selection(self):
        truncation_size = 100  # Top n DNA
        self.population.sort()
        self.mating_pool = self.population[:truncation_size]  # Keep top n
        self.best = self.mating_pool[0].genes

    # Normalizing the values to fit [old_lo, old_hi] to [0, 1]
    def normalize(self, val, old_lo, old_hi):
        return 0 if old_hi == old_lo else (val-old_lo) / (old_hi-old_lo)
