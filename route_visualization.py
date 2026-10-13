import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


# ============================================================
# 4-CITY TSP DATA
# ============================================================

cities = ["A", "B", "C", "D"]

distance = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
], dtype=float)


# ============================================================
# BEST QAOA ROUTE
# ============================================================

route = ["A", "B", "D", "C", "A"]

best_distance = 80


# ============================================================
# CREATE GRAPH
# ============================================================

G = nx.Graph()

for city in cities:
    G.add_node(city)


# Add all connections
for i in range(len(cities)):
    for j in range(i + 1, len(cities)):

        G.add_edge(
            cities[i],
            cities[j],
            weight=distance[i, j]
        )


# ============================================================
# DRAW GRAPH
# ============================================================

plt.figure(figsize=(9, 7))

pos = {
    "A": (0, 1),
    "B": (1, 2),
    "D": (2, 1),
    "C": (1, 0)
}


# Draw all possible connections
nx.draw_networkx_edges(
    G,
    pos,
    width=1
)


# Draw city nodes
nx.draw_networkx_nodes(
    G,
    pos,
    node_size=1800
)


# Draw city labels
nx.draw_networkx_labels(
    G,
    pos,
    font_size=16,
    font_weight="bold"
)


# ============================================================
# HIGHLIGHT QAOA ROUTE
# ============================================================

route_edges = []

for i in range(len(route) - 1):

    route_edges.append(
        (route[i], route[i + 1])
    )


nx.draw_networkx_edges(
    G,
    pos,
    edgelist=route_edges,
    width=4
)


# ============================================================
# DISTANCE LABELS ON ROUTE
# ============================================================

edge_labels = {}

for i in range(len(route) - 1):

    a = route[i]
    b = route[i + 1]

    edge_labels[(a, b)] = int(
        distance[
            cities.index(a),
            cities.index(b)
        ]
    )


nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    font_size=12
)


# ============================================================
# TITLE
# ============================================================

plt.title(
    "QAOA Solution for 4-City TSP\n"
    "Route: A → B → D → C → A | Distance = 80",
    fontsize=15,
    fontweight="bold"
)


plt.axis("off")

plt.tight_layout()


# ============================================================
# SAVE FIGURE
# ============================================================

plt.savefig(
    "qaoa_best_route.png",
    dpi=300,
    bbox_inches="tight"
)


plt.show()


print("=" * 60)
print("QAOA ROUTE VISUALIZATION")
print("=" * 60)

print(
    "Best QAOA route:",
    " -> ".join(route)
)

print(
    "Total distance:",
    best_distance
)

print(
    "Saved as:",
    "qaoa_best_route.png"
)

print("=" * 60)