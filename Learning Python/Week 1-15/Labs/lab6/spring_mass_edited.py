import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter # QUESTION: Is this the Matplotlib class that creates animations? ANSWER: Yes

m = 5.0 # Mass (kg)
k = 10.0 # Spring Constant (N/m)
x0 = 0.5 # Initial Displacement (m)
v0 = 0.0 # Initial Velocity (m/s)

t = np.linspace(0, 10, 200) # Creates an array of 200 timesteps from 0 seconds to 10 seconds
omega = np.sqrt(k / m) # Calculates the angular frequency of the spring system
x = x0 * np.cos(omega * t) + (v0 / omega) * np.sin(omega * t) 
# QUESTION: What is the exact formular used here to calculate the position? 
# ANSWER: The formula comes from a simple harmonic motion equation x(t) = A cos(wt) + B sin(wt)

fig1, ax1 = plt.subplots() # Creates a new figure and axis for the first animation
ax1.set_xlim(-1, 1) # Sets x-axis limits
ax1.set_ylim(-1, 1) # Sets y-axis limits
ax1.set_xlabel("Position (m)") # Labels x-axis
ax1.set_ylabel("Vertical displacement (m)") # Labels y-axis
mass_point, = ax1.plot([], [], 'go', markersize=15) # Creates a red circle marker for the mass

def init_motion(): # Function to create the initial animated frame
    mass_point.set_data([], []) # Creates a blank frame to return
    return mass_point,

def update_motion(frame): # Function to update the blank frame
    y = -x[frame] # QUESTION: Does this find the value on the frame'th index in the x array and put it as y? ANSWER: Yes
    mass_point.set_data([0], [y]) # Moves the point from initial point to set point to return it
    return mass_point,

ani1 = FuncAnimation(fig1, update_motion, frames=len(t)//2, init_func=init_motion, blit=True) # Creates an animation
ani1.save('spring_mass_motion.gif', writer=PillowWriter(fps=20)) # Saves as a gif file
plt.show() # Shows the animation
plt.close(fig1) # Closes the animation

# Repeates the entire process for the second plot (line 14 and onwards)

fig2, ax2 = plt.subplots()
ax2.set_xlim(0, max(t))
ax2.set_ylim(min(x) * 1.1, max(x) * 1.1)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Displacement (m)')
line, = ax2.plot([], [], 'b-', linewidth=2)
point, = ax2.plot([], [], 'go')

def init_displacement():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def update_displacement(frame):
    line.set_data(t[:frame], x[:frame])
    point.set_data([t[frame]], [x[frame]])
    return line, point

ani2 = FuncAnimation(fig2, update_displacement, frames=len(t)//2, init_func=init_displacement, blit=True)
ani2.save('spring_mass_displacement.gif', writer=PillowWriter(fps=20))
plt.show()
plt.close(fig2)