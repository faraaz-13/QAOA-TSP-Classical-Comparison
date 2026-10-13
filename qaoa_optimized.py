import numpy as np
import time
from itertools import permutations

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


# ============================================================
# 1. 4-CITY TSP DATASET
# ============================================================

cities = ["A", "B", "C", "D"]

distance = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
], dtype=float)

N = 4

# A is fixed as the starting city.
remaining_cities = ["B", "C", "D"]

# 3 remaining cities × 3 positions
num_qubits = 9


# ============================================================
# 2. CREATE REDUCED QUBO
# ============================================================

P = 100

Q = np.zeros((num_qubits, num_qubits))


def index(city, position):
    """
    Map city index and position to a qubit.
    city = 0 -> B
    city = 1 -> C
    city = 2 -> D
    position = 0,1,2
    """
    return city * 3 + position


# ------------------------------------------------------------
# Constraint 1:
# Exactly one city at every position
# ------------------------------------------------------------

for position in range(3):

    variables = [
        index(city, position)
        for city in range(3)
    ]

    for i in variables:
        Q[i, i] += -P

    for a in range(len(variables)):
        for b in range(a + 1, len(variables)):
            i = variables[a]
            j = variables[b]
            Q[i, j] += 2 * P


# ------------------------------------------------------------
# Constraint 2:
# Every city appears exactly once
# ------------------------------------------------------------

for city in range(3):

    variables = [
        index(city, position)
        for position in range(3)
    ]

    for i in variables:
        Q[i, i] += -P

    for a in range(len(variables)):
        for b in range(a + 1, len(variables)):
            i = variables[a]
            j = variables[b]
            Q[i, j] += 2 * P


# ------------------------------------------------------------
# Objective:
# A -> first city
# city -> city
# last city -> A
# ------------------------------------------------------------

# A -> first city
for city in range(3):

    i = index(city, 0)

    Q[i, i] += distance[0, city + 1]


# City -> city between positions
for position in range(2):

    for city1 in range(3):

        for city2 in range(3):

            i = index(city1, position)
            j = index(city2, position + 1)

            Q[i, j] += distance[city1 + 1, city2 + 1]


# Last city -> A
for city in range(3):

    i = index(city, 2)

    Q[i, i] += distance[city + 1, 0]


# ============================================================
# 3. QUBO ENERGY
# ============================================================

def qubo_energy(bitstring):
    """
    Calculate x^T Q x.
    """

    bits = np.array(
        [int(bit) for bit in bitstring[::-1]]
    )

    return float(bits @ Q @ bits)


# ============================================================
# 4. DECODE BITSTRING
# ============================================================

def decode_bitstring(bitstring):

    # Qiskit displays highest qubit on the left.
    bits = bitstring[::-1]

    matrix = np.array(
        [int(bit) for bit in bits]
    ).reshape(3, 3)

    return matrix


# ============================================================
# 5. CHECK TSP CONSTRAINTS
# ============================================================

def check_valid(matrix):

    position_sums = matrix.sum(axis=0)
    city_sums = matrix.sum(axis=1)

    return (
        np.all(position_sums == 1)
        and np.all(city_sums == 1)
    )


# ============================================================
# 6. CONVERT MATRIX TO ROUTE
# ============================================================

def get_route(matrix):

    route = ["A"]

    for position in range(3):

        selected = np.where(
            matrix[:, position] == 1
        )[0]

        if len(selected) != 1:
            return None

        city_index = selected[0]

        route.append(
            remaining_cities[city_index]
        )

    route.append("A")

    return route


# ============================================================
# 7. CALCULATE ROUTE DISTANCE
# ============================================================

def route_distance(route):

    total = 0

    for i in range(len(route) - 1):

        a = cities.index(route[i])
        b = cities.index(route[i + 1])

        total += distance[a, b]

    return total


# ============================================================
# 8. BUILD QAOA CIRCUIT
# ============================================================

def create_qaoa_circuit(gamma, beta):

    qc = QuantumCircuit(num_qubits)

    # --------------------------------------------------------
    # Initial |+> state
    # --------------------------------------------------------

    for q in range(num_qubits):
        qc.h(q)

    # --------------------------------------------------------
    # Cost unitary
    #
    # For QUBO:
    #
    # x_i = (1 - Z_i) / 2
    #
    # Instead of constructing a full Hamiltonian,
    # we directly implement the QUBO phase.
    # --------------------------------------------------------

    for i in range(num_qubits):

        if Q[i, i] != 0:

            qc.rz(
                -gamma * Q[i, i],
                i
            )

    for i in range(num_qubits):

        for j in range(i + 1, num_qubits):

            if Q[i, j] != 0:

                qc.cx(i, j)

                qc.rz(
                    gamma * Q[i, j],
                    j
                )

                qc.cx(i, j)

    # --------------------------------------------------------
    # Mixer unitary
    # --------------------------------------------------------

    for q in range(num_qubits):

        qc.rx(
            2 * beta,
            q
        )

    # --------------------------------------------------------
    # Measurement
    # --------------------------------------------------------

    qc.measure_all()

    return qc


# ============================================================
# 9. CLASSICAL TSP BASELINE
# ============================================================

print("=" * 70)
print("CLASSICAL TSP BASELINE")
print("=" * 70)

classical_start = time.perf_counter()

best_classical_route = None
best_classical_distance = float("inf")

for permutation in permutations(remaining_cities):

    route = ["A"] + list(permutation) + ["A"]

    cost = route_distance(route)

    if cost < best_classical_distance:

        best_classical_distance = cost
        best_classical_route = route

classical_runtime = (
    time.perf_counter() - classical_start
)

print(
    "Best classical route:",
    " -> ".join(best_classical_route)
)

print(
    "Classical distance:",
    best_classical_distance
)

print(
    "Classical runtime:",
    f"{classical_runtime:.8f} seconds"
)


# ============================================================
# 10. QAOA EXPERIMENT SETTINGS
# ============================================================

shots = 1024

# Moderate grid so the experiment remains practical.
gamma_values = np.linspace(
    0.0,
    2 * np.pi,
    9
)

beta_values = np.linspace(
    0.0,
    np.pi,
    7
)

print("\n" + "=" * 70)
print("QAOA OPTIMIZATION")
print("=" * 70)

print("Qubits:", num_qubits)
print("QAOA layers: 1")
print("Shots per parameter pair:", shots)

print(
    "Gamma values:",
    len(gamma_values)
)

print(
    "Beta values:",
    len(beta_values)
)

print(
    "Total parameter combinations:",
    len(gamma_values) * len(beta_values)
)


# ============================================================
# 11. SIMULATOR
# ============================================================

simulator = AerSimulator()


# ============================================================
# 12. RUN QAOA GRID SEARCH
# ============================================================

results = []

experiment_start = time.perf_counter()

total_experiments = (
    len(gamma_values) *
    len(beta_values)
)

experiment_number = 0


for gamma in gamma_values:

    for beta in beta_values:

        experiment_number += 1

        print(
            f"\nExperiment "
            f"{experiment_number}/{total_experiments}"
        )

        print(
            f"gamma = {gamma:.4f}, "
            f"beta = {beta:.4f}"
        )

        # Create circuit
        qc = create_qaoa_circuit(
            gamma,
            beta
        )

        # Transpile
        transpiled = transpile(
            qc,
            simulator
        )

        # Measure runtime
        start_time = time.perf_counter()

        job = simulator.run(
            transpiled,
            shots=shots
        )

        result = job.result()

        runtime = (
            time.perf_counter()
            - start_time
        )

        counts = result.get_counts()

        # ----------------------------------------------------
        # Analyze all measured states
        # ----------------------------------------------------

        valid_shots = 0

        best_route = None
        best_route_cost = float("inf")

        total_energy = 0

        valid_states = []

        for bitstring, count in counts.items():

            energy = qubo_energy(bitstring)

            total_energy += (
                energy * count
            )

            matrix = decode_bitstring(
                bitstring
            )

            if check_valid(matrix):

                valid_shots += count

                route = get_route(matrix)

                if route is not None:

                    cost = route_distance(
                        route
                    )

                    valid_states.append(
                        (
                            cost,
                            count,
                            bitstring,
                            route
                        )
                    )

                    if cost < best_route_cost:

                        best_route_cost = cost
                        best_route = route

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        valid_probability = (
            valid_shots / shots
        )

        average_energy = (
            total_energy / shots
        )

        if best_route is None:

            best_route_cost = None

        # ----------------------------------------------------
        # Save result
        # ----------------------------------------------------

        results.append({
            "gamma": gamma,
            "beta": beta,
            "average_energy": average_energy,
            "valid_probability": valid_probability,
            "best_route_cost": best_route_cost,
            "runtime": runtime,
            "counts": counts,
            "valid_states": valid_states
        })

        print(
            "Valid probability:",
            f"{valid_probability:.4f}"
        )

        print(
            "Average QUBO energy:",
            f"{average_energy:.4f}"
        )

        if best_route is not None:

            print(
                "Best route:",
                " -> ".join(best_route)
            )

            print(
                "Best route distance:",
                best_route_cost
            )

        else:

            print(
                "Best route: None"
            )


# ============================================================
# 13. FIND BEST QAOA RESULT
# ============================================================

experiment_runtime = (
    time.perf_counter()
    - experiment_start
)


# First preference:
# lowest valid route distance.
valid_results = [
    r for r in results
    if r["best_route_cost"] is not None
]


if valid_results:

    best_result = min(
        valid_results,
        key=lambda r: (
            r["best_route_cost"],
            -r["valid_probability"]
        )
    )

else:

    # If no valid solution was measured,
    # choose the result with highest validity probability.
    best_result = max(
        results,
        key=lambda r: r["valid_probability"]
    )


# ============================================================
# 14. FINAL RESULTS
# ============================================================

print("\n\n")
print("=" * 70)
print("FINAL QAOA RESULTS")
print("=" * 70)

print(
    "\nBest gamma:",
    f"{best_result['gamma']:.6f}"
)

print(
    "Best beta:",
    f"{best_result['beta']:.6f}"
)

print(
    "Valid-solution probability:",
    f"{best_result['valid_probability']:.4f}"
)

print(
    "Average QUBO energy:",
    f"{best_result['average_energy']:.4f}"
)

if best_result["best_route_cost"] is not None:

    print(
        "Best QAOA route:",
        " -> ".join(
            min(
                best_result["valid_states"],
                key=lambda x: x[0]
            )[3]
        )
    )

    print(
        "Best QAOA route distance:",
        best_result["best_route_cost"]
    )

else:

    print(
        "Best QAOA route: No valid route measured"
    )

print(
    "\nQAOA experiment runtime:",
    f"{experiment_runtime:.4f} seconds"
)

print(
    "Classical runtime:",
    f"{classical_runtime:.8f} seconds"
)

print(
    "\nClassical optimum:",
    best_classical_distance
)

if best_result["best_route_cost"] is not None:

    print(
        "QAOA best distance:",
        best_result["best_route_cost"]
    )

    if (
        best_result["best_route_cost"]
        == best_classical_distance
    ):

        print(
            "\nQAOA MATCHED THE CLASSICAL OPTIMUM"
        )

    else:

        print(
            "\nQAOA DID NOT MATCH THE CLASSICAL OPTIMUM"
        )


# ============================================================
# 15. TOP PARAMETER RESULTS
# ============================================================

print("\n" + "=" * 70)
print("TOP QAOA PARAMETER RESULTS")
print("=" * 70)

# Sort:
# 1. valid route distance
# 2. validity probability
sorted_results = sorted(
    results,
    key=lambda r: (
        r["best_route_cost"]
        if r["best_route_cost"] is not None
        else float("inf"),
        -r["valid_probability"]
    )
)

for i, r in enumerate(
    sorted_results[:10],
    start=1
):

    print(
        f"\n{i}. "
        f"gamma={r['gamma']:.4f}, "
        f"beta={r['beta']:.4f}"
    )

    print(
        "   Valid probability:",
        f"{r['valid_probability']:.4f}"
    )

    print(
        "   Average energy:",
        f"{r['average_energy']:.4f}"
    )

    print(
        "   Best route distance:",
        r["best_route_cost"]
    )


# ============================================================
# 16. SAVE RESULTS
# ============================================================

np.save(
    "qaoa_optimization_results.npy",
    np.array(results, dtype=object),
    allow_pickle=True
)

print("\nResults saved to:")
print("qaoa_optimization_results.npy")

print("\n" + "=" * 70)
print("QAOA OPTIMIZATION COMPLETED")
print("=" * 70)