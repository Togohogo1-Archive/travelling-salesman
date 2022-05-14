from dataclasses import dataclass
from random import randint, random, sample


@dataclass
class DNA:
    fitness: float  # Distance
    genes: list[int]  # A valid tour

    # Mutation swaps positions of 2 cities
    def mutate(self, mutation_rate, city_count):
        if random() < mutation_rate:
            a, b = sample(range(1, city_count), 2)
            self.genes[a], self.genes[b] = self.genes[b], self.genes[a]

    def cross(self, other, city_count):
        return self.partially_mapped_crossover(other, city_count)

    def partially_mapped_crossover(self, other, city_count):
        p1_segment = self.genes[1:-1]
        p2_segment = other.genes[1:-1]
        p1_idx = [0]*city_count
        p2_idx = [0]*city_count
        child = p1_segment[:]  # Copying `p1_segment` into child which includes random subsequence

        # Selecting the subsequence
        lo, hi = sorted([randint(0, city_count-2), randint(0 , city_count-2)])

        # Faster than .index
        for i in range(city_count-1):
            p1_idx[p1_segment[i]] = i
            p2_idx[p2_segment[i]] = i

        for i in range(city_count-1):
            if not (lo <= i <= hi):  # p1_idx[child[i]]
                tmp = p2_segment[i]

                # Elementwise mappings between `p1_segment` and `p2_segment` for cities in `p1_segment` but not in subsequence
                while lo <= p1_idx[tmp] <= hi:
                    # If corresponding city of `p1_segment` from `p2_segment` in subsequence, continue mapping from location of city in `p1_segment`
                    tmp = p2_segment[p1_idx[tmp]]

                child[i] = tmp

        return [0] + child + [0]

    def order_crossover(self, other, city_count):
        p1_segment = self.genes[1:-1]
        p2_segment = other.genes[1:-1]
        p1_idx = [0]*city_count
        p2_idx = [0]*city_count
        child = p1_segment[:]  # Copying `p1_segment` into child which includes random subsequence

        lo, hi = sorted([randint(0, city_count-2), randint(0 , city_count-2)])  # Selecting the subsequence
        mod = city_count - 1

        # Faster than .index
        for i in range(mod):
            p1_idx[p1_segment[i]] = i
            p2_idx[p2_segment[i]] = i

        start = p2_idx[p1_segment[(hi+1)%mod]]  # Start with index after subsequence and choose city with that index in `p1_segment`
        ii = 0

        # Staring from `start` to copy cities not already in `child` from `p2_segment` in the order the appear
        for i in range(start, start+mod):
            i %= mod

            # Not in child
            if not lo <= p1_idx[p2_segment[i]] <= hi:
                # Keep on moving aux index forward until not in subsequence
                while lo <= ii <= hi:
                    ii += 1

                child[ii] = p2_segment[i]
                ii += 1  # Move aux index forward after assigning to `child`

        return [0] + child + [0]

    def cycle_crossover(self, other, city_count):
        p1_segment = self.genes[1:-1]
        p2_segment = other.genes[1:-1]
        p1_idx = [0]*city_count
        p2_idx = [0]*city_count
        child = [-1]*(city_count-1)

        # Faster than .index
        for i in range(city_count-1):
            p1_idx[p1_segment[i]] = i
            p2_idx[p2_segment[i]] = i

        # Choosing the first city from `p1_segment` to be copied in `child`
        tmp = 0

        # Checking corresponding city of `p1_segment` from `p2_segment` and copying it to `child` in same position it occurs in `p1_segment`
        while child[tmp] < 0:
            child[tmp] = p1_segment[tmp]
            tmp = p1_idx[p2_segment[tmp]]

        # Cycle is complete when encountered a city in `child`, filling remaining cities from `p2_segment`
        for i in range(city_count-1):
            if child[i] < 0:
                child[i] = p2_segment[i]

        return [0] + child + [0]

    def __lt__(self, other):
        return self.fitness < other.fitness
