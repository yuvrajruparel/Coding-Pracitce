import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

m = 1.0
k = 5.0
x0 = 0.5
v0 = 0.0

t = np.linspace(0, 10, 200)
omega = np.sqrt(k / m)
x = x0 * np.cos(omega * t) + (v0 / omega) * np.sin(omega * t)

fig1, ax1 = plt.subplots()
ax1.set_xlim(-1, 1)
ax1.set_ylim(-1, 1)
ax1.set_xlabel("Position (m)")
ax1.set_ylabel("Vertical displacement (m)")
mass_point, = ax1.plot([], [], 'ro', markersize=15)

def init_motion():
    mass_point.set_data([], [])
    return mass_point,

def update_motion(frame):
    y = -x[frame]
    mass_point.set_data([0], [y])
    return mass_point,

ani1 = FuncAnimation(fig1, update_motion, frames=len(t)//2, init_func=init_motion, blit=True)
ani1.save('mass_spring_motion.gif', writer=PillowWriter(fps=20))
plt.show()
plt.close(fig1)

fig2, ax2 = plt.subplots()
ax2.set_xlim(0, max(t))
ax2.set_ylim(min(x) * 1.1, max(x) * 1.1)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Displacement (m)')
line, = ax2.plot([], [], 'b-', linewidth=2)
point, = ax2.plot([], [], 'ro')

def init_displacement():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def update_displacement(frame):
    line.set_data(t[:frame], x[:frame])
    point.set_data([t[frame]], [x[frame]])
    return line, point

ani2 = FuncAnimation(fig2, update_displacement, frames=len(t)//2, init_func=init_displacement, blit=True)
ani2.save('mass_spring_displacement.gif', writer=PillowWriter(fps=20))
plt.show()
plt.close(fig2)