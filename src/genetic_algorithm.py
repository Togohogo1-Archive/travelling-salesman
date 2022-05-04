from population import Population

def run(x_coord, y_coord, dist_from, city_count):
    population = Population(1000, 0.01)
    population.initialize(dist_from, city_count)

    while True:
        population.select()
        population.evaluate(x_coord, y_coord)
        population.crossover(dist_from, city_count)



    '''
    Initialize
    While true
        Evaluate
        If (termination condition) break
        Select
        Crossover
        Mutate
    Output best result
    '''
    return
