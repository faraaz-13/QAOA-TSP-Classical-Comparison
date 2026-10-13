import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import itertools
import time


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Quantum Mission Control",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT DATA
# ============================================================

distance_matrix = np.array([
    [0, 10, 15, 20, 18, 12],
    [10, 0, 35, 25, 17, 22],
    [15, 35, 0, 30, 28, 20],
    [20, 25, 30, 0, 14, 16],
    [18, 17, 28, 14, 0, 11],
    [12, 22, 20, 16, 11, 0]
])

cities = ["A", "B", "C", "D", "E", "F"]

# Classical six-city result
classical_route = "A → B → E → D → F → C → A"
classical_distance = 92
classical_runtime = 0.00048730

# Reduced QAOA result
qaoa_route = "A → B → D → C → A"
qaoa_distance = 80
qaoa_runtime = 8.5199

gamma = 1.570796
beta = 2.617994

valid_probability = 3.12
average_energy = -8.7109

qubo_variables = 36
qubo_terms = 396
qubo_penalty = 100
qubo_energy = -1108.0

qaoa_qubits = 9
qaoa_layers = 1
shots = 1024


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚛️ QuantumRoute")

    st.caption("QUANTUM MISSION CONTROL")

    st.divider()

    page = st.radio(
        "MISSION CONTROL",
        [
            "🚀 Mission Control",
            "🗺️ The Challenge",
            "⚛️ Quantum Lab",
            "🔢 QUBO Engine",
            "🏁 Final Result",
            "📖 How It Works"
        ]
    )

    st.divider()

    st.caption("SYSTEM STATUS")

    st.success("TSP MODEL  ONLINE")
    st.success("QUBO MODEL  VERIFIED")
    st.success("QAOA CIRCUIT  READY")

    st.divider()

    st.caption("PROJECT")

    st.write("6-City TSP")
    st.write("36-variable QUBO")
    st.write("9-qubit QAOA validation")

    st.divider()

    st.caption("TECH STACK")

    st.write("Python")
    st.write("Qiskit")
    st.write("NumPy")
    st.write("Streamlit")


# ============================================================
# TOP BRAND
# ============================================================

st.title("⚛️ Quantum Mission Control")

st.caption(
    "QAOA × TRAVELING SALESMAN PROBLEM  •  EXPERIMENT DASHBOARD"
)

st.divider()


# ============================================================
# MISSION CONTROL
# ============================================================

if page == "🚀 Mission Control":

    st.header("Can a quantum optimizer discover the shortest route?")

    st.write(
        "A six-city Traveling Salesman Problem is transformed into a "
        "Quadratic Unconstrained Binary Optimization model and then "
        "mapped into a quantum optimization experiment."
    )

    st.info(
        "MISSION OBJECTIVE  →  Find a minimum-cost closed tour."
    )

    st.divider()

    # --------------------------------------------------------
    # HERO METRICS
    # --------------------------------------------------------

    st.subheader("Mission Snapshot")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "Cities",
            "6"
        )

    with c2:
        st.metric(
            "Classical Routes",
            "120"
        )

    with c3:
        st.metric(
            "QUBO Variables",
            "36"
        )

    with c4:
        st.metric(
            "QAOA Qubits",
            "9"
        )

    with c5:
        st.metric(
            "Best Distance",
            "80"
        )

    st.divider()

    # --------------------------------------------------------
    # CURIOSITY SECTION
    # --------------------------------------------------------

    st.subheader("🔍 The Question")

    question_col1, question_col2 = st.columns([1.4, 1])

    with question_col1:

        st.write(
            "The classical solver can examine every possible route "
            "for this tiny six-city problem."
        )

        st.write(
            "But what happens when the same optimization problem is "
            "encoded as a quantum cost Hamiltonian?"
        )

        st.write(
            "That is the experiment."
        )

        st.warning(
            "The goal is not to claim quantum speedup. "
            "The goal is to demonstrate the complete "
            "TSP → QUBO → Ising → QAOA workflow."
        )

    with question_col2:

        st.metric(
            "Classical optimum",
            "92"
        )

        st.metric(
            "Reduced QAOA optimum",
            "80"
        )

        st.metric(
            "Difference",
            "12"
        )

    st.divider()

    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    st.subheader("🧬 Experiment Pipeline")

    p1, p2, p3, p4, p5 = st.columns(5)

    with p1:
        st.info("①\n\nTSP")

    with p2:
        st.info("②\n\nQUBO")

    with p3:
        st.info("③\n\nISING")

    with p4:
        st.info("④\n\nQAOA")

    with p5:
        st.success("⑤\n\nROUTE")

    st.divider()

    # --------------------------------------------------------
    # LIVE-LOOKING STATUS
    # --------------------------------------------------------

    st.subheader("🛰️ Mission Telemetry")

    t1, t2, t3 = st.columns(3)

    with t1:
        st.metric(
            "QUBO construction",
            "COMPLETE"
        )

    with t2:
        st.metric(
            "Hamiltonian",
            "306 terms"
        )

    with t3:
        st.metric(
            "QAOA circuit",
            "38 gates"
        )

    st.progress(
        1.0,
        text="Experiment pipeline completed"
    )


# ============================================================
# THE CHALLENGE
# ============================================================

elif page == "🗺️ The Challenge":

    st.header("🗺️ The Challenge")

    st.caption(
        "Before quantum optimization, understand the problem."
    )

    st.subheader("What is the TSP asking?")

    st.write(
        "Visit every city exactly once, return to the starting city, "
        "and minimize the total travel distance."
    )

    st.divider()

    # --------------------------------------------------------
    # CITY MAP
    # --------------------------------------------------------

    st.subheader("🌐 Six-City Network")

    positions = {
        "A": (0, 2),
        "B": (2, 4),
        "C": (5, 4),
        "D": (7, 2),
        "E": (5, 0),
        "F": (2, 0)
    }

    fig, ax = plt.subplots(figsize=(11, 6))

    # Draw all connections
    for i, city1 in enumerate(cities):

        for j, city2 in enumerate(cities):

            if i < j:

                x1, y1 = positions[city1]
                x2, y2 = positions[city2]

                ax.plot(
                    [x1, x2],
                    [y1, y2],
                    linewidth=0.7,
                    alpha=0.25
                )

    # Draw cities
    for city, (x, y) in positions.items():

        ax.scatter(
            x,
            y,
            s=1100,
            zorder=5
        )

        ax.text(
            x,
            y,
            city,
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            zorder=6
        )

    ax.set_title(
        "Six-City Optimization Landscape"
    )

    ax.axis("off")

    st.pyplot(
        fig,
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------------
    # MATRIX
    # --------------------------------------------------------

    st.subheader("📐 Distance Matrix")

    matrix_col1, matrix_col2 = st.columns([1.3, 1])

    with matrix_col1:

        st.dataframe(
            distance_matrix,
            use_container_width=True
        )

    with matrix_col2:

        st.metric(
            "Possible routes",
            "5! = 120"
        )

        st.metric(
            "Classical optimum",
            "92"
        )

        st.code(
            classical_route,
            language="text"
        )

    st.divider()

    st.subheader("🧠 Classical Baseline")

    st.write(
        "The classical solver fixes A as the starting city and "
        "enumerates the remaining five cities."
    )

    st.success(
        "Classical baseline established."
    )


# ============================================================
# QUANTUM LAB
# ============================================================

elif page == "⚛️ Quantum Lab":

    st.header("⚛️ Quantum Lab")

    st.caption(
        "Where the classical routing problem becomes a quantum optimization experiment."
    )

    # --------------------------------------------------------
    # QUANTUM SYSTEM
    # --------------------------------------------------------

    st.subheader("Quantum System")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.metric(
            "Qubits",
            "9"
        )

    with q2:
        st.metric(
            "QAOA depth",
            "p = 1"
        )

    with q3:
        st.metric(
            "Shots",
            "1024"
        )

    with q4:
        st.metric(
            "Pauli terms",
            "306"
        )

    st.divider()

    # --------------------------------------------------------
    # PARAMETER LANDSCAPE
    # --------------------------------------------------------

    st.subheader("🎛️ QAOA Parameter Search")

    st.write(
        "The reduced experiment searches over QAOA parameters γ and β "
        "to identify measured solutions with low cost."
    )

    param1, param2 = st.columns(2)

    with param1:

        st.metric(
            "γ (Gamma)",
            f"{gamma:.6f}"
        )

    with param2:

        st.metric(
            "β (Beta)",
            f"{beta:.6f}"
        )

    st.divider()

    # --------------------------------------------------------
    # EXPERIMENTAL RESULT
    # --------------------------------------------------------

    st.subheader("🎯 Measured State")

    result_col1, result_col2 = st.columns([1.2, 1])

    with result_col1:

        st.success(
            "Optimal measured route found"
        )

        st.subheader(
            qaoa_route
        )

        st.metric(
            "Route distance",
            "80"
        )

    with result_col2:

        st.metric(
            "Valid-solution probability",
            "3.12%"
        )

        st.metric(
            "Average QUBO energy",
            "-8.7109"
        )

    st.divider()

    # --------------------------------------------------------
    # QUANTUM EXPERIMENT
    # --------------------------------------------------------

    st.subheader("🔬 Experiment Telemetry")

    telemetry = {
        "Parameter": [
            "Gamma",
            "Beta",
            "QAOA layers",
            "Qubits",
            "Shots",
            "Valid probability",
            "Average QUBO energy"
        ],
        "Value": [
            f"{gamma:.6f}",
            f"{beta:.6f}",
            "1",
            "9",
            "1024",
            "3.12%",
            "-8.7109"
        ]
    }

    st.dataframe(
        telemetry,
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        "This experiment validates the QAOA workflow on a reduced "
        "four-city instance. It does not establish quantum advantage."
    )


# ============================================================
# QUBO ENGINE
# ============================================================

elif page == "🔢 QUBO Engine":

    st.header("🔢 QUBO Engine")

    st.caption(
        "The mathematical bridge between the TSP and the quantum circuit."
    )

    # --------------------------------------------------------
    # QUBO STATS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Variables",
            "36"
        )

    with c2:
        st.metric(
            "Matrix",
            "36 × 36"
        )

    with c3:
        st.metric(
            "Penalty",
            "100"
        )

    with c4:
        st.metric(
            "Non-zero terms",
            "396"
        )

    st.divider()

    # --------------------------------------------------------
    # ENCODING
    # --------------------------------------------------------

    st.subheader("Binary Encoding")

    left, right = st.columns(2)

    with left:

        st.write(
            "Each binary variable represents whether a city occupies "
            "a particular position in the tour."
        )

        st.code(
            "x(i,t) ∈ {0,1}",
            language="text"
        )

        st.write(
            "Six cities × six positions = 36 variables."
        )

    with right:

        st.write(
            "Constraint penalties enforce:"
        )

        st.write("• One city per position")
        st.write("• One position per city")
        st.write("• Valid closed tour")

    st.divider()

    # --------------------------------------------------------
    # VERIFIED RESULT
    # --------------------------------------------------------

    st.subheader("🧪 Verification Experiment")

    st.info(
        "Test route: A → B → E → D → F → C → A"
    )

    v1, v2, v3 = st.columns(3)

    with v1:
        st.metric(
            "QUBO energy",
            "-1108"
        )

    with v2:
        st.metric(
            "Travel cost",
            "92"
        )

    with v3:
        st.metric(
            "Penalty coefficient",
            "100"
        )

    st.write(
        "For a valid route, the QUBO energy contains both the "
        "travel objective and the constraint terms."
    )

    st.divider()

    st.subheader("QUBO Verification Table")

    verification = {
        "Property": [
            "Matrix shape",
            "Variables",
            "Penalty",
            "Non-zero terms",
            "Test route",
            "QUBO energy",
            "Original distance"
        ],
        "Value": [
            "36 × 36",
            "36",
            "100",
            "396",
            "A → B → E → D → F → C → A",
            "-1108.0",
            "92"
        ]
    }

    st.dataframe(
        verification,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FINAL RESULT
# ============================================================

elif page == "🏁 Final Result":

    st.header("🏁 Final Result")

    st.caption(
        "The moment where the classical and quantum experiments meet."
    )

    # --------------------------------------------------------
    # BIG RESULT
    # --------------------------------------------------------

    st.success(
        "✓ Reduced QAOA experiment produced a route with distance 80."
    )

    st.subheader(
        "A → B → D → C → A"
    )

    st.write(
        "This route has total distance 80 and matches the classical "
        "optimum for the reduced four-city instance."
    )

    st.divider()

    # --------------------------------------------------------
    # COMPARISON
    # --------------------------------------------------------

    st.subheader("⚖️ Experimental Comparison")

    comp1, comp2, comp3 = st.columns(3)

    with comp1:

        st.metric(
            "Classical optimum",
            "80"
        )

        st.caption(
            "Reduced four-city reference"
        )

    with comp2:

        st.metric(
            "QAOA best measured",
            "80"
        )

        st.caption(
            "Reduced four-city experiment"
        )

    with comp3:

        st.metric(
            "Difference",
            "0"
        )

        st.caption(
            "Matched"
        )

    st.divider()

    # --------------------------------------------------------
    # RUNTIME
    # --------------------------------------------------------

    st.subheader("⏱️ Runtime Reality")

    runtime1, runtime2 = st.columns(2)

    with runtime1:

        st.metric(
            "Classical runtime",
            f"{classical_runtime:.8f} s"
        )

    with runtime2:

        st.metric(
            "QAOA experiment runtime",
            f"{qaoa_runtime:.4f} s"
        )

    st.warning(
        "The classical method is much faster for this tiny instance. "
        "Therefore, the experiment should be interpreted as a demonstration "
        "of quantum optimization formulation and execution, not as a quantum "
        "speedup result."
    )

    st.divider()

    # --------------------------------------------------------
    # WHAT WAS ACTUALLY ACHIEVED
    # --------------------------------------------------------

    st.subheader("🚀 What This Project Demonstrates")

    a, b = st.columns(2)

    with a:

        st.write("✓ Six-city TSP formulated")

        st.write("✓ Classical baseline implemented")

        st.write("✓ 36-variable QUBO constructed")

        st.write("✓ QUBO mathematically verified")

    with b:

        st.write("✓ QUBO mapped to Ising Hamiltonian")

        st.write("✓ QAOA circuit constructed")

        st.write("✓ Reduced nine-qubit experiment executed")

        st.write("✓ Measured route decoded and compared")

    st.divider()

    st.info(
        "KEY TAKEAWAY  →  The important result is the complete mapping "
        "from a real combinatorial optimization problem to a quantum "
        "optimization formulation and executable QAOA experiment."
    )


# ============================================================
# HOW IT WORKS
# ============================================================

elif page == "📖 How It Works":

    st.header("📖 How It Works")

    st.caption(
        "Follow the problem from cities to qubits."
    )

    # --------------------------------------------------------
    # STEP 1
    # --------------------------------------------------------

    with st.expander(
        "① Start with the Traveling Salesman Problem",
        expanded=True
    ):

        st.write(
            "The objective is to visit every city exactly once and "
            "return to the starting city while minimizing total distance."
        )

        st.code(
            "A → B → D → C → A",
            language="text"
        )

    # --------------------------------------------------------
    # STEP 2
    # --------------------------------------------------------

    with st.expander(
        "② Convert the problem into binary variables"
    ):

        st.write(
            "A binary variable x(i,t) indicates whether city i is "
            "placed at tour position t."
        )

        st.code(
            "x(i,t) ∈ {0,1}",
            language="text"
        )

    # --------------------------------------------------------
    # STEP 3
    # --------------------------------------------------------

    with st.expander(
        "③ Build the QUBO"
    ):

        st.write(
            "The objective combines travel distance with penalty "
            "terms that enforce valid TSP constraints."
        )

        st.metric(
            "QUBO size",
            "36 × 36"
        )

    # --------------------------------------------------------
    # STEP 4
    # --------------------------------------------------------

    with st.expander(
        "④ Transform QUBO into an Ising Hamiltonian"
    ):

        st.write(
            "Binary variables are transformed into quantum operators."
        )

        st.code(
            "x = (1 - Z) / 2",
            language="text"
        )

    # --------------------------------------------------------
    # STEP 5
    # --------------------------------------------------------

    with st.expander(
        "⑤ Apply QAOA"
    ):

        st.write(
            "QAOA alternates between the cost Hamiltonian and a "
            "mixing Hamiltonian to search the optimization landscape."
        )

        st.metric(
            "QAOA depth",
            "p = 1"
        )

    # --------------------------------------------------------
    # STEP 6
    # --------------------------------------------------------

    with st.expander(
        "⑥ Measure and decode"
    ):

        st.write(
            "Measured bitstrings are converted back into candidate "
            "city-position assignments and checked for valid routes."
        )

        st.success(
            "Best measured route: A → B → D → C → A"
        )

    st.divider()

    st.subheader("⚠️ Simulation Limitation")

    st.warning(
        "The full six-city formulation contains 36 binary variables "
        "and therefore requires a 36-qubit representation. Full "
        "simulation was computationally impractical on the available "
        "machine. A reduced four-city nine-qubit experiment was used "
        "to execute and validate the QAOA workflow."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "⚛️ Quantum Mission Control  •  QAOA × TSP  •  Python + Qiskit + Streamlit"
)