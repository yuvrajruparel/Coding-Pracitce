import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3,3, 100, True)
p = [5, 1, 0, 3]
y = np.polyval(p,x)

plt.plot(x,y)
plt.xlabel("x")
plt.ylabel("p(x)")
plt.show()

z = np.polyfit(x,y,3)
print(z)