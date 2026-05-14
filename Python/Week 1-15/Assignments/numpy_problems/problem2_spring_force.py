import numpy as np
import matplotlib.pyplot as plt

def spring_const(forces,displacements):
    k = forces/displacements
    k_avg = np.mean(k)
    return k_avg

def spring_energy(forces, displacements):
    k_values = forces/displacements
    U = 0.5 * k_values * (displacements ** 2)
    return U

force_data = np.array([14, 18, 8, 9, 13])
disp_data = np.array([0.013, 0.020, 0.009, 0.010, 0.012])
average_k = spring_const(force_data, disp_data)
U_values = spring_energy(force_data, disp_data)

print(f"{average_k:.4f}")
print(f"{np.max(U_values):.4f}")

fig, axs = plt.subplots(2, 1)

axs[0].plot(disp_data, force_data, "bo")
axs[0].plot(disp_data, disp_data*average_k)
axs[0].set_xlabel("Displacement (m)")
axs[0].set_ylabel("Force (N)")

axs[1].plot(disp_data, U_values, "gx")
axs[1].set_xlabel("Displacement (m)")
axs[1].set_ylabel("Energy (J)")

plt.show()