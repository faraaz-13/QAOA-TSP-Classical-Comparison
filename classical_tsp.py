
import itertools
import numpy as np
import time

# ============================================================
# 1. CITY NAMES
# ============================================================

cities = ["A", "B", "C", "D", "E", "F"]


# ============================================================
# 2. DISTANCE MATRIX
# ============================================================

distance_matrix = np.array([
    [0, 10, 15, 20, 18, 12],
    [10, 0, 35, 25, 17, 22],
    [15, 35, 0, 30, 28, 20],
    [20, 25, 30, 0, 14, 16],
    [18, 17, 28, 14, 0, 11],
    [12, 22, 20, 16, 11, 0]
])


# ============================================================
# 3. CALCULATE TOTAL DISTANCE OF A ROUTE
# ============================================================

def calculate_route_distance(route):
    total_distance = 0

    for i in range(len(route) - 1):
        total_distance += distance_matrix[
            route[i], route[i + 1]
        ]

    return int(total_distance)


# ============================================================
# 4. CLASSICAL TSP SOLVER
# ============================================================

def solve_tsp():
    best_distance = float("inf")
    best_route = None
    routes_checked = 0

    # Keep city A fixed as the starting city
    remaining_cities = [1, 2, 3, 4, 5]

    start_time = time.perf_counter()

    # Generate all possible orderings of the other cities
    for permutation in itertools.permutations(remaining_cities):

        # Start at A and return to A
        route = (0,) + permutation + (0,)

        # Calculate the complete tour distance
        route_distance = calculate_route_distance(route)

        routes_checked += 1

        # Update the best route
        if route_distance < best_distance:
            best_distance = route_distance
            best_route = route

    end_time = time.perf_counter()
    runtime = end_time - start_time

    return best_route, best_distance, routes_checked, runtime


# ============================================================
# 5. DISPLAY RESULTS
# ============================================================

if __name__ == "__main__":

    best_route, best_distance, routes_checked, runtime = solve_tsp()

    print("\n" + "=" * 60)
    print("             CLASSICAL TSP SOLVER")
    print("=" * 60)

    print("\nCities:")
    print(cities)

    print("\nDistance Matrix:")
    print(distance_matrix)

    print("\nAlgorithm: Exhaustive Search")
    print("Execution platform: Classical CPU")

    print("\nNumber of routes checked:")
    print(routes_checked)

    # Convert city indices to city names
    route_names = [cities[i] for i in best_route]

    print("\nOptimal Route:")
    print(" -> ".join(route_names))

    print("\nMinimum Route Distance:")
    print(f"{best_distance} units")

    print("\nClassical Runtime:")
    print(f"{runtime:.8f} seconds")

    print("\nOptimal solution guaranteed: Yes")

    print("\nTime Complexity: O(n!)")
    print("Space Complexity: O(n) auxiliary route storage")

    print("\n" + "=" * 60)
