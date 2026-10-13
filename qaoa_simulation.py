import numpy as np

from qiskit import transpile
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator


# ============================================================
# SMALL-SCALE QAOA TSP DEMONSTRATION
# 4 CITIES
#
# A is fixed as the starting city.
# 3 cities x 3 positions = 9 qubits
# ============================================================

print("=" * 60)
print("QAOA TSP - SMALL SCALE DEMONSTRATION")
print("=" * 60)


# ------------------------------------------------------------
# 1. Cities
# ------------------------------------------------------------

cities = ["A", "B", "C", "D"]

distance = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
], dtype=float)


# A is fixed at position 0.
#
# Remaining:
# B, C, D
#
# Positions:
# 1, 2, 3
#
# 3 x 3 = 9 qubits

num_cities = 3
num_positions = 3
num_qubits = 9

print("\nStarting city: A")
print("Remaining cities: B, C, D")
print("Number of qubits:", num_qubits)


# ------------------------------------------------------------
# 2. Variable mapping
# ------------------------------------------------------------

def variable(city, position):
    return city * num_positions + position


# ------------------------------------------------------------
# 3. Build QUBO
# ------------------------------------------------------------

P = 100.0

Q = np.zeros(
    (num_qubits, num_qubits),
    dtype=float
)


def add_linear(i, value):
    Q[i, i] += value


def add_quadratic(i, j, value):

    if i > j:
        i, j = j, i

    Q[i, j] += value


# ------------------------------------------------------------
# 4. Position constraints
# ------------------------------------------------------------

for position in range(num_positions):

    variables = [
        variable(city, position)
        for city in range(num_cities)
    ]

    for i in variables:
        add_linear(i, -P)

    for a in range(len(variables)):

        for b in range(a + 1, len(variables)):

            add_quadratic(
                variables[a],
                variables[b],
                2 * P
            )


# ------------------------------------------------------------
# 5. City constraints
# ------------------------------------------------------------

for city in range(num_cities):

    variables = [
        variable(city, position)
        for position in range(num_positions)
    ]

    for i in variables:
        add_linear(i, -P)

    for a in range(len(variables)):

        for b in range(a + 1, len(variables)):

            add_quadratic(
                variables[a],
                variables[b],
                2 * P
            )


# ------------------------------------------------------------
# 6. Distance objective
# ------------------------------------------------------------

# Mapping:
#
# reduced city 0 = B
# reduced city 1 = C
# reduced city 2 = D
#
# actual city index = reduced + 1


# A -> first city

for city in range(num_cities):

    q = variable(city, 0)

    actual_city = city + 1

    add_linear(
        q,
        distance[0, actual_city]
    )


# City -> next city

for position in range(num_positions - 1):

    for city1 in range(num_cities):

        for city2 in range(num_cities):

            q1 = variable(city1, position)
            q2 = variable(city2, position + 1)

            actual_city1 = city1 + 1
            actual_city2 = city2 + 1

            add_quadratic(
                q1,
                q2,
                distance[
                    actual_city1,
                    actual_city2
                ]
            )


# Last city -> A

for city in range(num_cities):

    q = variable(city, num_positions - 1)

    actual_city = city + 1

    add_linear(
        q,
        distance[actual_city, 0]
    )


print("\nQUBO created.")
print("QUBO shape:", Q.shape)


# ------------------------------------------------------------
# 7. QUBO -> Ising Hamiltonian
# ------------------------------------------------------------

pauli_terms = []


# Linear terms

for i in range(num_qubits):

    qii = Q[i, i]

    if abs(qii) > 1e-12:

        pauli = ["I"] * num_qubits

        pauli[num_qubits - 1 - i] = "Z"

        pauli_terms.append(
            (
                "".join(pauli),
                -qii / 2
            )
        )


# Quadratic terms

for i in range(num_qubits):

    for j in range(i + 1, num_qubits):

        qij = Q[i, j]

        if abs(qij) > 1e-12:

            # Zi
            pauli_i = ["I"] * num_qubits
            pauli_i[num_qubits - 1 - i] = "Z"

            pauli_terms.append(
                (
                    "".join(pauli_i),
                    -qij / 4
                )
            )

            # Zj
            pauli_j = ["I"] * num_qubits
            pauli_j[num_qubits - 1 - j] = "Z"

            pauli_terms.append(
                (
                    "".join(pauli_j),
                    -qij / 4
                )
            )

            # ZiZj
            pauli_ij = ["I"] * num_qubits
            pauli_ij[num_qubits - 1 - i] = "Z"
            pauli_ij[num_qubits - 1 - j] = "Z"

            pauli_terms.append(
                (
                    "".join(pauli_ij),
                    qij / 4
                )
            )


# ------------------------------------------------------------
# 8. Combine Pauli terms
# ------------------------------------------------------------

combined = {}

for pauli, coefficient in pauli_terms:

    combined[pauli] = (
        combined.get(pauli, 0.0)
        + coefficient
    )


combined = {
    pauli: coefficient
    for pauli, coefficient in combined.items()
    if abs(coefficient) > 1e-12
}


hamiltonian = SparsePauliOp.from_list(
    [
        (
            pauli,
            complex(coefficient)
        )
        for pauli, coefficient in combined.items()
    ]
)


print("Hamiltonian terms:", len(hamiltonian))


# ------------------------------------------------------------
# 9. Create QAOA
# ------------------------------------------------------------

qaoa = QAOAAnsatz(
    cost_operator=hamiltonian,
    reps=1
)


print("\nQAOA created.")
print("QAOA layers:", 1)
print("QAOA parameters:", qaoa.num_parameters)


# ------------------------------------------------------------
# 10. Test parameters
# ------------------------------------------------------------

gamma = 0.5
beta = 0.5

qaoa.assign_parameters(
    [gamma, beta],
    inplace=True
)

qaoa.measure_all()


# ------------------------------------------------------------
# 11. Aer simulator
# ------------------------------------------------------------

simulator = AerSimulator()


# ------------------------------------------------------------
# 12. Transpile
# ------------------------------------------------------------

compiled = transpile(
    qaoa,
    simulator,
    optimization_level=1
)


print("\nCircuit transpiled.")
print("Circuit depth:", compiled.depth())


# ------------------------------------------------------------
# 13. Run
# ------------------------------------------------------------

shots = 256

print("\nRunning QAOA...")
print("Shots:", shots)

job = simulator.run(
    compiled,
    shots=shots
)

result = job.result()

counts = result.get_counts()


# ------------------------------------------------------------
# 14. Results
# ------------------------------------------------------------

print("\nQAOA simulation completed.")

print(
    "Unique states:",
    len(counts)
)


sorted_counts = sorted(
    counts.items(),
    key=lambda x: x[1],
    reverse=True
)


print("\nTop measured states:")

for bitstring, count in sorted_counts[:10]:

    probability = count / shots

    print(
        f"{bitstring}  "
        f"counts={count:3d}  "
        f"probability={probability:.4f}"
    )


print("\n" + "=" * 60)
print("SMALL-SCALE QAOA TEST COMPLETED")
print("=" * 60)