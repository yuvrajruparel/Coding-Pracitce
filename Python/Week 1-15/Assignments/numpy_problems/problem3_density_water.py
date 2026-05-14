import numpy as np
import matplotlib.pyplot as plt

def calc_density_water(temperatures):
    density = (-1.2329 * (10 ** (-7)) * (temperatures ** 4)) + (4.11472 * (10 ** (-5)) * (temperatures ** 3)) - (0.00748423 * (temperatures ** 2)) + (0.0508007 * temperatures) + 999.904
    return density

tf = np.linspace(32,212, num = 51, endpoint=True)
tc = (tf - 32) * 5/9
density = calc_density_water(tc)
idx = np.argmax(density)
maxtc = tc[idx]
maxtf = tf[idx]
maxd = density[idx]

print(f"{maxtf:.1f}")

plt.plot(tc, density)
plt.plot(maxtc,maxd, "rx")
plt.text(maxtc, maxd, f"max density: {maxd:.1f}, max temperature: {maxtc:.1f}")
plt.show()