import numpy as np


# ============================================================
# 1. CITY NAMES
# ============================================================

cities = ["A", "B", "C", "D", "E", "F"]

num_cities = len(cities)


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
# 3. QUBO SETTINGS
# ============================================================

# Penalty coefficient.
# It makes invalid routes more expensive.
P = 100


# ============================================================
# 4. CREATE VARIABLE MAPPING
# ============================================================

variables = {}

variable_number = 0

for city in range(num_cities):

    for position in range(num_cities):

        variables[(city, position)] = variable_number

        variable_number += 1


num_variables = variable_number


# ============================================================
# 5. CREATE QUBO MATRIX
# ============================================================

Q = np.zeros(
    (num_variables, num_variables),
    dtype=float
)


# ============================================================
# 6. HELPER FUNCTION
# ============================================================

def add_qubo_term(i, j, value):

    Q[i, j] += value


# ============================================================
# 7. CONSTRAINT 1
#
# Every position must contain exactly one city.
#
# (x1 + x2 + ... + x6 - 1)^2
# ============================================================

for position in range(num_cities):

    # Linear terms
    for city in range(num_cities):

        q = variables[(city, position)]

        add_qubo_term(q, q, -P)

    # Quadratic terms
    for city1 in range(num_cities):

        for city2 in range(city1 + 1, num_cities):

            q1 = variables[(city1, position)]
            q2 = variables[(city2, position)]

            add_qubo_term(q1, q2, 2 * P)


# ============================================================
# 8. CONSTRAINT 2
#
# Every city must appear exactly once.
#
# (x1 + x2 + ... + x6 - 1)^2
# ============================================================

for city in range(num_cities):

    # Linear terms
    for position in range(num_cities):

        q = variables[(city, position)]

        add_qubo_term(q, q, -P)

    # Quadratic terms
    for position1 in range(num_cities):

        for position2 in range(position1 + 1, num_cities):

            q1 = variables[(city, position1)]
            q2 = variables[(city, position2)]

            add_qubo_term(q1, q2, 2 * P)


# ============================================================
# 9. DISTANCE OBJECTIVE
#
# Minimize the distance between consecutive cities.
# ============================================================

for position in range(num_cities):

    next_position = (position + 1) % num_cities

    for city1 in range(num_cities):

        for city2 in range(num_cities):

            if city1 != city2:

                q1 = variables[(city1, position)]
                q2 = variables[(city2, next_position)]

                distance = distance_matrix[city1, city2]

                add_qubo_term(
                    q1,
                    q2,
                    distance
                )


# ============================================================
# 10. DISPLAY QUBO INFORMATION
# ============================================================

print()
print("=" * 60)
print("                 QUBO MODEL")
print("=" * 60)

print()
print("Number of cities      :", num_cities)
print("Number of variables   :", num_variables)
print("Penalty coefficient P :", P)


# ============================================================
# 11. DISPLAY MATRIX
# ============================================================

print()
print("QUBO Matrix Shape:")
print(Q.shape)

print()
print("Number of non-zero terms:")
print(np.count_nonzero(Q))


# ============================================================
# 12. DISPLAY VARIABLE MAPPING
# ============================================================

print()
print("-" * 60)
print("VARIABLE MAPPING")
print("-" * 60)

for (city, position), variable in variables.items():

    print(
        f"x[{cities[city]},{position}] -> q{variable}"
    )


# ============================================================
# 13. DISPLAY QUBO MATRIX
# ============================================================

print()
print("-" * 60)
print("QUBO MATRIX")
print("-" * 60)

np.set_printoptions(
    linewidth=200,
    suppress=True
)

print(Q)


# ============================================================
# 14. SAVE QUBO MATRIX
# ============================================================

np.save(
    "qubo_matrix.npy",
    Q
)

print()
print("QUBO matrix saved as:")
print("qubo_matrix.npy")

print()
print("=" * 60)
print("QUBO MODEL CREATED SUCCESSFULLY")
print("=" * 60)