import numpy as np
import matplotlib.pyplot as plt

def drag_coefficient(mass, terminal_velocity):
    cd = (mass * 9.81) / (terminal_velocity ** 2)
    return cd

def dimensionless_drag_coefficient(cd_values, area):
    Cd = (2 * cd_values) / (1.293 * area)
    return Cd

mass_data = np.array([83.6, 60.2, 72.1, 91.1, 92.9, 65.3, 80.9])
terminal_velocity_data = np.array([53.4, 48.5, 50.9, 55.7, 54.0, 47.7, 51.1])
area_data = np.array([0.455, 0.402, 0.452, 0.486, 0.531, 0.475, 0.487])

cd_array = drag_coefficient(mass_data, terminal_velocity_data)
Cd_array = dimensionless_drag_coefficient(cd_array, area_data)

print(f"{np.min(cd_array):.4f}")
print(f"{np.max(cd_array):.4f}")
print(f"{np.mean(cd_array):.4f}")

print(f"{np.min(Cd_array):.4f}")
print(f"{np.max(Cd_array):.4f}")
print(f"{np.mean(Cd_array):.4f}")

idx = np.argsort(mass_data)
mass_data = mass_data[idx]
cd_array = cd_array[idx]
Cd_array = Cd_array[idx]

avg_cd = np.mean(cd_array)
avg_Cd = np.mean(Cd_array)

fig, axs = plt.subplots(2, 1)

axs[0].plot(mass_data, cd_array, "*-")
axs[0].axhline(avg_cd)

axs[1].plot(mass_data, Cd_array, "*")
axs[1].axhline(avg_Cd)

plt.show()