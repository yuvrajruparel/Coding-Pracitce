import matplotlib.pyplot as plt

import numpy as np

def snp(z):
    root = 1 / np.sqrt(2 * np.pi)
    exponent = np.exp(- (z ** 2) / 2)
    ans = root * exponent
    return ans

z = np.linspace(-4,4, num = 101, endpoint=True)
f = snp(z)

print(f"{np.max(f):.4f}")

plt.plot(z, f)
plt.xlabel("z")
plt.ylabel("f(z)")
plt.title("Standard normal probability density function.")
plt.show()