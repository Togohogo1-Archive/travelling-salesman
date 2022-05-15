import plotter


def evaluate(new_dist, x_coord, y_coord, tour, solution):
    title = f"Distance: {new_dist:.2f}"
    plotter.plot_path(x_coord, y_coord, tour, title, solution)
    plotter.draw_path()


def find_path(trace, slast, mask):
    path = [0, slast]

    while slast != 0:
        mask ^= 1 << slast-1  # Removing `slast` from the set
        slast = trace[slast][mask]  # Retreive second last of new set with previous value of `slast` as last
        path.append(slast)

    return path


# https://en.wikipedia.org/wiki/Held–Karp_algorithm
def run(x_coord, y_coord, dist_from, city_count, solution=None):
    # dp[i][j] = min distance staring from city 0 -> subset j -> last city i
    dp = [[float("inf")]*(2**city_count) for _ in range(city_count)]

    # trace[i][j] = 2nd last city visited from best path 0 -> subset j -> last city i
    trace = [[0]*(2**city_count) for _ in range(city_count)]

    # Initialization
    for last in range(1, city_count):
        dp[last][0] = dist_from[0][last]

    # Can loop like this since subsets of every masked subset will have been previously computed
    for perm in range(1, 2**city_count):
        for last in range(1, city_count):  # Last city
            if not (1 << last-1) & perm:  # Last city not in `perm`
                best = float("inf")

                for slast in range(1, city_count):  # Second last city
                    if (1 << slast-1) & perm:  # Second last city must be in `perm`

                        # Previous dp state: 0 -> subset `perm` absent of `slast` -> `slast`
                        # All previous states will end with `slast` -> `last`
                        if dp[slast][(1 << slast-1) ^ perm] + dist_from[slast][last] < best:
                            best = dp[slast][(1 << slast-1) ^ perm] + dist_from[slast][last]
                            trace[last][perm] = slast

                dp[last][perm] = best

    ans = float("inf")
    slast = -1
    full = 2**(city_count-1) - 1  # Mask of full set of cities excluding 0

    # Finding shortest tour by connecting all possible last cities back to 0 for each nearly completed `perm`
    for last in range(1, city_count):
        for cut in range(1, city_count):
            perm = full ^ (1 << cut-1)  # Generates all integers with `city_count` bits as 1 and having len `city_count-1`
            if dp[last][perm] + dist_from[last][0] < ans:
                ans = dp[last][perm] + dist_from[last][0]
                slast = last

    lesus = find_path(trace, slast, full)  # Joshgone requires lesus
    evaluate(ans, x_coord, y_coord, lesus, solution)
    return lesus
