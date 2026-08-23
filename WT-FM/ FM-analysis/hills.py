import numpy as np
import matplotlib.pyplot as plt

with open("HILLS") as f:
    header = next(line for line in f if "FIELDS" in line)

fields = header.split()[2:]  # skip '#!' and 'FIELDS'

time_idx = fields.index("time")
height_idx = fields.index("height")

data = np.loadtxt("HILLS", comments="#")

time = data[:, time_idx]
height = data[:, height_idx]

plt.plot(time, height)
plt.xlabel("Time", fontsize=14, labelpad=12)
plt.ylabel("Hills", fontsize=14, labelpad=12)
plt.title("Hill Height vs Time")
plt.tight_layout()
plt.savefig("hills.png", dpi=600, bbox_inches="tight")
plt.show()
