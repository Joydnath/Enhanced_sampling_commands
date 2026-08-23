import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# Global styling (important)
# -----------------------
plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 14,
    "axes.linewidth": 1.2,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 4,
    "ytick.major.size": 4
})

# -----------------------
# Load data
# -----------------------
data = np.loadtxt("fes.dat", comments="#")
s1 = data[:, 0]   # AlphaRMSD
s2 = data[:, 1]   # Rg
V  = data[:, 2]   # Free energy

# Shift minimum to zero (VERY important for papers)
F = V - np.min(V)

# -----------------------
# Plot
# -----------------------
fig, ax = plt.subplots(figsize=(6.5, 5.5))

cf = ax.tricontourf(
    s1, s2, F,
    levels=100,
    cmap="viridis"
)

# Optional: contour lines for clarity
ax.tricontour(
    s1, s2, F,
    levels=10,
    colors="k",
    linewidths=0.3,
    alpha=0.7
)

# Labels
ax.set_xlabel("s", fontsize=14, labelpad=12)
ax.set_ylabel("z", fontsize=14, labelpad=12)

# Colorbar
cbar = plt.colorbar(cf, ax=ax, pad=0.02)
cbar.set_label("Free Energy (kJ/mol)", fontsize=14, labelpad=12)
cbar.ax.tick_params(labelsize=10)

# Tight layout
plt.tight_layout()

# Save high resolution (VERY important for papers)
plt.savefig("fes_publication.png", dpi=600, bbox_inches="tight")

plt.show()
