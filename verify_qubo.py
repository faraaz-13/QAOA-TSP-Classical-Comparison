import numpy as np


# ============================================================
# 1. LOAD QUBO MATRIX
# ============================================================

Q = np.load("qubo_matrix.npy")


# ============================================================
# 2. CITY INFORMATION
# ============================================================

cities = ["A", "B", "C", "D", "E", "F"]

distance_matrix = np.array([
    [0, 10, 15, 20, 18, 12],
    [10, 0, 35, 25, 17, 22],
    [15, 35, 0, 30, 28, 20],
    [20, 25, 30, 0, 14, 16],
    [18, 17, 28, 14, 0, 11],
    [12, 22, 20, 16, 11, 0]
])


# ============================================================
# 3. CLASSICAL BEST ROUTE
# ============================================================

route = [0, 1, 4, 3, 5, 2]

# A -> B -> E -> D -> F -> C -> A


# ============================================================
# 4. CREATE 36-BIT SOLUTION
# ============================================================

num_cities = 6

solution = np.zeros(36, dtype=int)

for position, city in enumerate(route):

    variable_index = city * num_cities + position

    solution[variable_index] = 1


# ============================================================
# 5. CALCULATE QUBO ENERGY
#
# E(x) = x^T Q x
# ============================================================

qubo_energy = solution @ Q @ solution


# ============================================================
# 6. CALCULATE ORIGINAL TSP DISTANCE
# ============================================================

tsp_distance = 0

for i in range(len(route)):

    current_city = route[i]

    next_city = route[(i + 1) % len(route)]

    tsp_distance += distance_matrix[
        current_city,
        next_city
    ]


# ============================================================
# 7. CHECK CONSTRAINTS
# ============================================================

# Number of cities selected at each position
position_counts = []

for position in range(num_cities):

    count = 0

    for city in range(num_cities):

        index = city * num_cities + position

        count += solution[index]

    position_counts.append(count)


# Number of positions occupied by each city
city_counts = []

for city in range(num_cities):

    count = 0

    for position in range(num_cities):

        index = city * num_cities + position

        count += solution[index]

    city_counts.append(count)


# ============================================================
# 8. DISPLAY RESULTS
# ============================================================

print()
print("=" * 60)
print("                 QUBO VERIFICATION")
print("=" * 60)

print()

print("Test Route:")
print("A -> B -> E -> D -> F -> C -> A")

print()

print("Binary solution:")
print(solution)

print()

print("Number of 1s in solution:")
print(np.sum(solution))

print()

print("Cities selected at each position:")
print(position_counts)

print()

print("Positions occupied by each city:")
print(city_counts)

print()

print("Original TSP distance:")
print(tsp_distance)

print()

print("QUBO energy:")
print(qubo_energy)

print()

print("=" * 60)

if (
    all(count == 1 for count in position_counts)
    and
    all(count == 1 for count in city_counts)
):

    print("VALID TSP SOLUTION")
    
else:

    print("INVALID TSP SOLUTION")

print("=" * 60)