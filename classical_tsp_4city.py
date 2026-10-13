
import itertools
import time
import numpy as np

# Same four-city problem as qaoa_optimized.py
cities = ["A", "B", "C", "D"]

distance = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
], dtype=float)

start = time.perf_counter()

best_route = None
best_distance = float("inf")
checked = 0

# Keep A fixed; examine all orders of B, C, D
for order in itertools.permutations(cities[1:]):
    route = ("A",) + order + ("A",)
    total = sum(
        distance[cities.index(route[i]),
                 cities.index(route[i + 1])]
        for i in range(len(route) - 1)
    )
    checked += 1

    if total < best_distance:
        best_distance = total
        best_route = route

runtime = time.perf_counter() - start

print("CLASSICAL EXHAUSTIVE SEARCH — FOUR-CITY TSP")
print("Cities:", " -> ".join(cities))
print("Tours checked:", checked)
print("Optimal route:", " -> ".join(best_route))
print("Minimum distance:", best_distance)
print(f"Runtime: {runtime:.8f} seconds")
print("Optimality guaranteed: Yes")
