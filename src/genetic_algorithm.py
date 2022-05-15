from population import Population

def run(x_coord, y_coord, dist_from, city_count, solution=None):
    population_size = 1000
    mutation_rate = 0.01
    max_generations = 2000

    population = Population(population_size, mutation_rate)
    population.initialize(dist_from, city_count)

    while population.generation < max_generations:
        population.select()
        population.evaluate(dist_from, x_coord, y_coord, solution)
        population.crossover(dist_from, city_count)  # And mutate

    return population.best