from math import log2
'''
(1 << index) | num   to turn on bit at index N
(1 << index) & num   to check of bit at index N is 1

dp[i][j] = min dist of city sequence that ends on i with length j


'''


def comb(ans, idx, maxn, bits):
    if idx == maxn:
        if bits == 0:
            yield ans

        return

    yield from comb(ans ^ (1 << idx), idx+1, maxn, bits-1)
    yield from comb(ans, idx+1, maxn, bits)


def run(x_coord, y_coord, dist_from, city_count):
    dp = [[float("inf")]*(2**city_count) for _ in range(city_count)]

    # Initialization
    for last in range(1, city_count):
        dp[last][0] = dist_from[0][last]

    # Do dp
    for cities in range(1, city_count):
        for perm in comb(0, 0, city_count-1, cities):  # 2^n part
            for last in range(1, city_count):  # Last city
                if not (1 << last-1) & perm:  # Last city not in `perm``
                    best = float("inf")

                    for slast in range(1, city_count):  # Second last city

                        if (1 << slast-1) & perm:  # Second last city must be in `perm`
                            if dp[slast][(1 << slast-1) ^ perm] + dist_from[slast][last] < best:
                                best = dp[slast][(1 << slast-1) ^ perm] + dist_from[slast][last]

                    dp[last][perm] = best

    ans = float("inf")

    for last in range(1, city_count):
        for perm in comb(0, 0, city_count-1, city_count-2):
            if dp[last][perm] + dist_from[last][0] < ans:
                ans = dp[last][perm] + dist_from[last][0]

    print(ans, "_")
    return ans