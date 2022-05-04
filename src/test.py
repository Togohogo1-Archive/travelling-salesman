
from random import randint, sample

def cycle(self, other, city_count):
    p1_segment = self[1:-1]
    p2_segment = other[1:-1]
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

a = [0, 1, 2, 3, 4, 5, 6, 7, 0]
b = [0, 5, 3, 7, 1, 4, 6, 2, 0]

a = [0] + sample(range(1, 1000001), 1000000) + [0]
b = [0] + sample(range(1, 1000001), 1000000) + [0]


c = cycle(a, b, 1000001)
# print(c)
print("done")
# print(partially_mapped(a, b, 8))