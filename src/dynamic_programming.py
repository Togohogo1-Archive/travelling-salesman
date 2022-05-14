import plotter


def evaluate(new_dist, x_coord, y_coord, tour):
    title = f"Distance: {new_dist:.2f}"
    plotter.plot_path(x_coord, y_coord, tour, title)
    plotter.draw_path()


def find_path(trace, slast, mask):
    path = [0, slast]

    while slast != 0:
        mask ^= 1 << slast-1  # Removing `slast` from the set
        slast = trace[slast][mask]  # Retreive second last of new set with previous value of `slast` as last
        path.append(slast)

    return path


# Generates all integers with `bits` bits as 1 and having len `maxn`
def comb(ans, idx, maxn, bits):
    if idx == maxn:
        if bits == 0:
            yield ans

        return

    yield from comb(ans ^ (1 << idx), idx+1, maxn, bits-1)
    yield from comb(ans, idx+1, maxn, bits)


# https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm
def run(x_coord, y_coord, dist_from, city_count):
    # dp[i][j] = min distance staring from city 0 -> subset j -> last city i
    dp = [[float("inf")]*(2**city_count) for _ in range(city_count)]

    # trace[i][j] = 2nd last city visited in best subset j where the last city visited is i
    trace = [[0]*(2**city_count) for _ in range(city_count)]

    # Initialization
    for last in range(1, city_count):
        dp[last][0] = dist_from[0][last]

    # Do dp
    for cities in range(1, city_count):
        for perm in comb(0, 0, city_count-1, cities):  # 2^n part combined with previous for loop
            for last in range(1, city_count):  # Last city
                if not (1 << last-1) & perm:  # Last city not in `perm`
                    best = float("inf")

                    for slast in range(1, city_count):  # Second last city
                        if (1 << slast-1) & perm:  # Second last city must be in `perm`

                            # Previous dp state: set with second last as the last
                            # All previous states will end with `last`, hence find the minimum distance across all states
                            if dp[slast][(1 << slast-1) ^ perm] + dist_from[slast][last] < best:
                                best = dp[slast][(1 << slast-1) ^ perm] + dist_from[slast][last]
                                trace[last][perm] = slast

                    dp[last][perm] = best

    ans = float("inf")
    slast = -1

    # Finding shortest tour by connecting all last cities back to 0
    for last in range(1, city_count):
        for perm in comb(0, 0, city_count-1, city_count-2):
            if dp[last][perm] + dist_from[last][0] < ans:
                ans = dp[last][perm] + dist_from[last][0]
                slast = last

    lesus = find_path(trace, slast, 2**(city_count-1)-1)  # Joshgone requires lesus name
    evaluate(ans, x_coord, y_coord, lesus)
