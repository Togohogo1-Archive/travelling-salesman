from pprint import pprint
from random import randint
import dynamic_programming
import brute_force


for i in range(10):
    city_count = 4

    dist_from = [[0]*city_count for _ in range(city_count)]

    for c1 in range(city_count):
        for c2 in range(c1, city_count):
            if c1 != c2:
                dist_from[c1][c2] = dist_from[c2][c1] = randint(1, 10)

    a = dynamic_programming.run(None, None, dist_from, city_count)
    b = brute_force.run(None, None, dist_from, city_count)

    if a != b:
        print("dp ->", a, "bf ->", b, "_")
        pprint(dist_from)

'''
dp -> 27 bf -> 20 _
[[0, 10, 2, 4], [10, 0, 4, 10], [2, 4, 0, 9], [4, 10, 9, 0]]
dp -> 18 bf -> 19 _
[[0, 3, 9, 10], [3, 0, 4, 6], [9, 4, 0, 2], [10, 6, 2, 0]]
dp -> 17 bf -> 20 _
[[0, 2, 10, 7], [2, 0, 5, 1], [10, 5, 0, 7], [7, 1, 7, 0]]
dp -> 22 bf -> 15 _
[[0, 9, 2, 5], [9, 0, 2, 6], [2, 2, 0, 10], [5, 6, 10, 0]]
dp -> 18 bf -> 13 _
[[0, 8, 4, 6], [8, 0, 1, 2], [4, 1, 0, 8], [6, 2, 8, 0]]
'''