from dataclasses import dataclass
from collections import defaultdict
from random import random, randint, sample

@dataclass
class DNA:
    fitness: float  # distance
    genes: list[int]  # A valid tour

    def mutate(self, mutation_rate, city_count):
        if random() < mutation_rate:
            a, b = sample(range(1, city_count), 2)
            self.genes[a], self.genes[b] = self.genes[b], self.genes[a]

    def cross(self, other, city_count):
        return self.partially_mapped_crossover(other, city_count)

    def partially_mapped_crossover(self, other, city_count):
        p1_segment = self.genes[1:-1]
        p2_segment = other.genes[1:-1]
        p1_idx = [0]*city_count  # Easy way to init array
        p2_idx = [0]*city_count
        child = p1_segment[:]  # First copying p1_segment into child

        lo, hi = sorted([randint(0, city_count-2), randint(0 , city_count-2)])

        # Faster than .index
        for i in range(city_count-1):
            p1_idx[p1_segment[i]] = i
            p2_idx[p2_segment[i]] = i

        for i in range(city_count-1):
            if not (lo <= i <= hi):  # p1_idx[child[i]]
                tmp = p2_segment[i]

                # Mapping
                while lo <= p1_idx[tmp] <= hi:
                    tmp = p2_segment[p1_idx[tmp]]

                child[i] = tmp

        return [0] + child + [0]

    def order_crossover(self, other, city_count):
        p1_segment = self.genes[1:-1]
        p2_segment = other.genes[1:-1]
        p1_idx = [0]*city_count  # Easy way to init array
        p2_idx = [0]*city_count
        child = p1_segment[:]  # First copying p1_segment into child

        lo, hi = sorted([randint(0, city_count-2), randint(0 , city_count-2)])
        mod = city_count - 1

        # Faster than .index
        for i in range(mod):
            p1_idx[p1_segment[i]] = i
            p2_idx[p2_segment[i]] = i

        start = p2_idx[p1_segment[(hi+1)%mod]]  # Next element in first array, then take index of that element in second array
        ii = 0  # Auxiliary index required for order crossover

        for i in range(start, start+mod):
            i %= mod

            # Not already in child
            if not (lo <= p1_idx[p2_segment[i]] <= hi):
                while lo <= ii <= hi:
                    ii += 1

                child[ii] = p2_segment[i]
                ii += 1  # Move to the next position

        return [0] + child + [0]

    def cycle_crossover(self, other, city_count):
        p1_segment = self.genes[1:-1]
        p2_segment = other.genes[1:-1]
        p1_idx = [0]*city_count  # Easy way to init array
        p2_idx = [0]*city_count
        child = [-1]*(city_count-1)

        # Faster than .index
        for i in range(city_count - 1):
            p1_idx[p1_segment[i]] = i
            p2_idx[p2_segment[i]] = i

        tmp = 0

        while child[tmp] < 0:
            child[tmp] = p1_segment[tmp]
            tmp = p1_idx[p2_segment[tmp]]

        for i in range(city_count-1):
            if child[i] < 0:
                child[i] = p2_segment[i]

        return [0] + child + [0]

    def __lt__(self, other):
        return self.fitness < other.fitness
