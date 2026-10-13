import numpy as np


# ============================================================
# DECODE QAOA RESULTS
# ============================================================

cities = ["A", "B", "C", "D"]

distance = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
], dtype=float)


# Results obtained from the QAOA simulation
counts = {
    "000101000": 9,
    "010100000": 5,
    "110111000": 5,
    "011111000": 4,
    "010001000": 4,
    "010110000": 4,
    "111101000": 4,
    "010111111": 4,
    "010100100": 4,
    "010111000": 4,
}


def decode_bitstring(bitstring):

    # Qiskit displays classical bits in reverse order.
    bits = bitstring[::-1]

    matrix = np.array(
        [int(bit) for bit in bits]
    ).reshape(3, 3)

    return matrix


def check_valid(matrix):

    # Every position must contain exactly one city.
    position_sums = matrix.sum(axis=0)

    # Every city must appear exactly once.
    city_sums = matrix.sum(axis=1)

    return (
        np.all(position_sums == 1)
        and np.all(city_sums == 1)
    )


def get_route(matrix):

    route = ["A"]

    # Rows represent B, C, D.
    # Columns represent positions 1, 2, 3.

    for position in range(3):

        city_index = np.where(
            matrix[:, position] == 1
        )[0][0]

        route.append(
            cities[city_index + 1]
        )

    route.append("A")

    return route


def route_distance(route):

    total = 0

    for i in range(len(route) - 1):

        a = cities.index(route[i])
        b = cities.index(route[i + 1])

        total += distance[a, b]

    return total


print("=" * 60)
print("QAOA RESULT DECODER")
print("=" * 60)


valid_results = []


for bitstring, count in counts.items():

    matrix = decode_bitstring(bitstring)

    if check_valid(matrix):

        route = get_route(matrix)

        cost = route_distance(route)

        probability = count / 256

        valid_results.append(
            (
                cost,
                count,
                probability,
                bitstring,
                route
            )
        )


# ------------------------------------------------------------
# Display valid solutions
# ------------------------------------------------------------

print("\nValid QAOA solutions:", len(valid_results))

valid_results.sort(
    key=lambda x: x[0]
)


for cost, count, probability, bitstring, route in valid_results:

    print("\nBitstring:", bitstring)

    print(
        "Route:",
        " -> ".join(route)
    )

    print("Distance:", cost)

    print("Counts:", count)

    print(
        "Probability:",
        f"{probability:.4f}"
    )


# ------------------------------------------------------------
# Best valid solution
# ------------------------------------------------------------

if valid_results:

    best = valid_results[0]

    print("\n" + "=" * 60)
    print("BEST VALID QAOA SOLUTION")
    print("=" * 60)

    print(
        "Route:",
        " -> ".join(best[4])
    )

    print("Distance:", best[0])

    print("Counts:", best[1])

    print(
        "Probability:",
        f"{best[2]:.4f}"
    )

else:

    print("\nNo valid TSP solutions were measured.")

print("\n" + "=" * 60)