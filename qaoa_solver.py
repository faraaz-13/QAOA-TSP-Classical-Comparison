import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp


# ============================================================
# QAOA FOR 6-CITY TSP
# ============================================================

print("=" * 60)
print("QAOA FOR 6-CITY TRAVELING SALESMAN PROBLEM")
print("=" * 60)


# ------------------------------------------------------------
# 1. Load the QUBO matrix
# ------------------------------------------------------------

Q = np.load("qubo_matrix.npy")

num_qubits = Q.shape[0]

print("\nQUBO matrix shape :", Q.shape)
print("Number of qubits  :", num_qubits)


# ------------------------------------------------------------
# 2. Convert QUBO to Ising Hamiltonian
#
# QUBO:
#       E(x) = x^T Q x
#
# Using:
#       x_i = (1 - Z_i) / 2
#
# We obtain:
#
#       H = constant
#           + sum(h_i Z_i)
#           + sum(J_ij Z_i Z_j)
#
# The constant does not affect optimization.
# ------------------------------------------------------------

pauli_terms = []
constant = 0.0

# Linear terms
for i in range(num_qubits):

    qii = Q[i, i]

    if abs(qii) > 1e-12:
        constant += qii / 2

        linear_coeff = -qii / 2

        pauli = ["I"] * num_qubits
        pauli[num_qubits - 1 - i] = "Z"

        pauli_terms.append(
            ("".join(pauli), linear_coeff)
        )


# Quadratic terms
for i in range(num_qubits):

    for j in range(i + 1, num_qubits):

        qij = Q[i, j]

        if abs(qij) > 1e-12:

            # Constant contribution
            constant += qij / 4

            # Linear contribution for Zi
            coeff_i = -qij / 4

            pauli_i = ["I"] * num_qubits
            pauli_i[num_qubits - 1 - i] = "Z"

            pauli_terms.append(
                ("".join(pauli_i), coeff_i)
            )

            # Linear contribution for Zj
            coeff_j = -qij / 4

            pauli_j = ["I"] * num_qubits
            pauli_j[num_qubits - 1 - j] = "Z"

            pauli_terms.append(
                ("".join(pauli_j), coeff_j)
            )

            # ZZ contribution
            zz_coeff = qij / 4

            pauli_ij = ["I"] * num_qubits
            pauli_ij[num_qubits - 1 - i] = "Z"
            pauli_ij[num_qubits - 1 - j] = "Z"

            pauli_terms.append(
                ("".join(pauli_ij), zz_coeff)
            )


# ------------------------------------------------------------
# 3. Combine identical Pauli terms
# ------------------------------------------------------------

combined_terms = {}

for pauli, coefficient in pauli_terms:

    if pauli not in combined_terms:
        combined_terms[pauli] = 0.0

    combined_terms[pauli] += coefficient


# Remove extremely small coefficients
combined_terms = {
    pauli: coeff
    for pauli, coeff in combined_terms.items()
    if abs(coeff) > 1e-12
}


# ------------------------------------------------------------
# 4. Create SparsePauliOp
# ------------------------------------------------------------

hamiltonian = SparsePauliOp.from_list(
    [
        (pauli, complex(coeff))
        for pauli, coeff in combined_terms.items()
    ]
)


print("\nIsing Hamiltonian created successfully.")

print("Number of Pauli terms :", len(hamiltonian))

print("Constant offset       :", constant)


# ------------------------------------------------------------
# 5. Create QAOA circuit
# ------------------------------------------------------------

reps = 1

qaoa_circuit = QAOAAnsatz(
    cost_operator=hamiltonian,
    reps=reps
)

print("\nQAOA configuration")
print("------------------")
print("Qubits       :", qaoa_circuit.num_qubits)
print("QAOA layers  :", reps)
print("Parameters   :", qaoa_circuit.num_parameters)


# ------------------------------------------------------------
# 6. Add measurements
# ------------------------------------------------------------

qaoa_circuit.measure_all()


# ------------------------------------------------------------
# 7. Circuit information
# ------------------------------------------------------------

print("\nCircuit information")
print("-------------------")
print("Depth        :", qaoa_circuit.depth())
print("Gate count   :", len(qaoa_circuit.data))


print("\nQAOA CIRCUIT CREATED SUCCESSFULLY")

print("=" * 60)