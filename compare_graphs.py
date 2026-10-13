
import matplotlib.pyplot as plt
import numpy as np

# Results copied from your terminal outputs
classical_6city_distance = 92
classical_6city_runtime = 0.00011430

qaoa_reported_distance = 80
qaoa_runtime = 12.0882
qaoa_valid_probability = 4.30

# Graph 1: Best tour distance
plt.figure(figsize=(7, 5))
bars = plt.bar(
    ["Classical (6 cities)", "QAOA (check instance)"],
    [classical_6city_distance, qaoa_reported_distance]
)
plt.ylabel("Tour distance (units)")
plt.title("Classical vs QAOA: Best Reported Tour Distance")
plt.bar_label(bars, fmt="%.1f")
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("graph1_distance.png", dpi=300)
plt.close()

# Graph 2: Runtime, logarithmic scale
plt.figure(figsize=(7, 5))
bars = plt.bar(
    ["Classical (6 cities)", "QAOA (reported)"],
    [classical_6city_runtime, qaoa_runtime]
)
plt.yscale("log")
plt.ylabel("Runtime (seconds, log scale)")
plt.title("Reported Execution Times")
plt.bar_label(bars, labels=[
    f"{classical_6city_runtime:.8f} s",
    f"{qaoa_runtime:.4f} s"
], padding=4)
plt.grid(axis="y", which="both", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("graph2_runtime.png", dpi=300)
plt.close()

# Graph 3: QAOA valid-solution probability
plt.figure(figsize=(6, 5))
plt.bar(["QAOA"], [qaoa_valid_probability])
plt.ylabel("Valid-solution probability (%)")
plt.title("QAOA Valid-Solution Probability")
plt.ylim(0, 100)
plt.text(0, qaoa_valid_probability + 2,
         f"{qaoa_valid_probability:.2f}%", ha="center")
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("graph3_valid_probability.png", dpi=300)
plt.close()

print("Graphs saved:")
print("graph1_distance.png")
print("graph2_runtime.png")
print("graph3_valid_probability.png")
print()
print("WARNING: The 92-unit result is from the six-city run.")
print("The 80-unit QAOA result uses a four-city route.")
print("Do not report the distance chart as a same-instance")
print("comparison until both scripts use the same distance matrix.")
classical_distance = 80
qaoa_distance = 80

classical_runtime = 0.00011430  # Replace with the new 4-city run's time
qaoa_runtime = 12.0882
qaoa_valid_probability = 4.30