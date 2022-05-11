'''
(1 << index) | num   to turn on bit at index N
(1 << index) & num   to check of bit at index N is 1

dp[i][j] = min dist of city sequence that ends on i with length j


'''

def run(x_coord, y_coord, dist_from, city_count):
    dp = [[float("inf")]*city_count for _ in range(city_count)]
    vis = [[1]*city_count for _ in range(city_count)]
    ans = float("inf")

    # Initialization
    for city in range(1, city_count):
        dp[city][1] = dist_from[0][city]
        vis[city][1] = (1 << city) | vis[city][0]  # Setting index `city` as visited

    for seg_len in range(2, city_count):
        for end_city in range(1, city_count):
            best = float("inf")
            best_vis = 1

            for pre_end_city in range(1, city_count):
                if end_city != pre_end_city and not (1 << end_city) & vis[pre_end_city][seg_len-1]:
                    if dp[pre_end_city][seg_len-1] + dist_from[pre_end_city][end_city] < best:
                        best = dp[pre_end_city][seg_len-1] + dist_from[pre_end_city][end_city]
                        best_vis = (1 << end_city) | vis[pre_end_city][seg_len-1]

            dp[end_city][seg_len] = best
            vis[end_city][seg_len] = best_vis

    for pre_end_city in range(1, city_count):
        if dp[pre_end_city][city_count-1] + dist_from[pre_end_city][0] < ans:
            ans = dp[pre_end_city][city_count-1] + dist_from[pre_end_city][0]

    print(ans)