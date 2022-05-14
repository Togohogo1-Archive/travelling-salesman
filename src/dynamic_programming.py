import plotter


def evaluate(new_dist, x_coord, y_coord, tour):
    title = f"Distance: {new_dist:.2f}"
    plotter.plot_path(x_coord, y_coord, tour, title)
    plotter.draw_path()


def find_path(trace, slast, mask):
    path = [0, slast]
    cur = slast

    while cur != 0:
        mask ^= 1 << cur-1
        cur = trace[cur][mask]
        path.append(cur)

    return path


def comb(ans, idx, maxn, bits):
    if idx == maxn:
        if bits == 0:
            yield ans

        return

    yield from comb(ans ^ (1 << idx), idx+1, maxn, bits-1)
    yield from comb(ans, idx+1, maxn, bits)


def run(x_coord, y_coord, dist_from, city_count):
    dp = [[float("inf")]*(2**city_count) for _ in range(city_count)]
    trace = [[0]*(2**city_count) for _ in range(city_count)]

    # Initialization
    for last in range(1, city_count):
        dp[last][0] = dist_from[0][last]

    # Do dp
    for cities in range(1, city_count):
        for perm in comb(0, 0, city_count-1, cities):  # 2^n part
            for last in range(1, city_count):  # Last city
                if not (1 << last-1) & perm:  # Last city not in `perm`
                    best = float("inf")

                    for slast in range(1, city_count):  # Second last city

                        if (1 << slast-1) & perm:  # Second last city must be in `perm`
                            if dp[slast][(1 << slast-1) ^ perm] + dist_from[slast][last] < best:
                                best = dp[slast][(1 << slast-1) ^ perm] + dist_from[slast][last]
                                trace[last][perm] = slast

                    dp[last][perm] = best

    ans = float("inf")
    slast = -1

    for last in range(1, city_count):
        for perm in comb(0, 0, city_count-1, city_count-2):
            if dp[last][perm] + dist_from[last][0] < ans:
                ans = dp[last][perm] + dist_from[last][0]
                slast = last

    lesus = find_path(trace, slast, 2**(city_count-1)-1)  # Joshgone requires lesus name
    evaluate(ans, x_coord, y_coord, lesus)
