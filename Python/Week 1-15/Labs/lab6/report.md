<div style="text-align: justify;">
# Lab 6 Report

## Part 1: Writing Code with GenAI

### Prompt

My first prompt was:

> You are an expert in visualising dynamical systems with Python code.
>
> Using Python, generate a executable code without any comments, that generates two animated plots of an object as it is dropped while being attached to a spring.
>
> The code should use 2 main imported libraries: Numpy and Matplotlib
>
> The plot should be saved in the gif format   

I did prompt further: After running the output in VS code, I took a screenshot of all the errors that were generated in the Terminal and uploaded them on the same chat. I typed the following prompt:
> These are the errors that VS code shows, fix them

I repeated the above step one more time before almose all the errors were fixed.

### Reflection

#### 1. How many prompts did you have to exchange with the LLM? Did the code it provided work well in the first attempt, or did you need to interface with the LLM to get the desired output?
    
Answer: I had to use 4 prompts in total to get my desired output. The first was the base prompt to start. The next 3 were where I pasted errors from VS Code and asked DukeGPT to fix them.

#### 2. Was there anything that the LLM struggled with in particular? What did it do well?

Answer: Although DukeGPT wrote a code with lots of errors in the begining, it was surprisingly good in fixing its own errors once I pasted the VS Code Terminal output. One thing it failed to correct was the plots not showing in the Python interpreter, giving wrong solutions. I went through the code to find the error and it turns out DukeGPT forgot plt.show hence the plots did not show.

#### 3. Note how the problem is not well defined. Did the LLM make assumptions? What weight did it assign to the object? What was the spring constant? etc.

Answer: Due to the specifics not mentioned in the problem, DukeGPT assumed its own values. It took the mass as 1.0 kg, the spring constant as 5.0 N/m, the initial displacement as 0.5 m, and the initial velocity as 0.0 m/s.

#### 4. How did your results compare to those around you? Did your algorithms run and look the same? What about the visualization aspect?

Answer: While comparing to my friend's code (Felipe), I realised that his code was much longer than mine. He has 81 lines of code while I just had 56 lines. His code was also more complex than mine, using Differential Equations and many more physical parameters to generate plots. Consequently, his plots were more complex. His displacement plot generated a model for the mass that slowly comes to a stop, while mine assumed Simple Harmonic motion. His mass motion gif modelled the mass with a spring, while mine just did so with a mass. He also had to correct his code much more than I had to due to my simplicity. The libraries we both imported were the same.

## Part 2: Understanding AI-Generated Code

### Reflection

#### 1. How complex was the original code? Did you understand most of it or did you have to prompt the LLM to explain/change the code in any way?

The code seemed complex and overwhelming in the start, and I found it difficult to understand it as a whole. However, when I started commenting on it line by line, I was able to understand the code logic slowly and it was starting to piece together. I had a few questions. They were relatively minor questions, which I asked DukeGPT to explain and it explained it well.

#### 2. Often, these models will over complicate a problem, introducing errors. Is this something you noticed in your code?

I did not notice this in my code, since DukeGPT generated a relatively simple code and logic for me. However, when reviewing with my classmates, I noticed that some of their codes were overcomplicated, introducing Differential Equations and other things to model the mass on the spring. This also caused them to having to prompt their LLM many more times to fix all the errors, while I just had to prompt it 4 times.

#### 3. What was one new thing you learned from examining the generated code?

I learnt that the generated code is not necessarily complex, it can be quite simple to understand as well. By following a step by step process and understanding the code line by line instead of as a whole, it is not difficult to examine the generated code.


## Part 3: Working with AI-Generated Code

## Reflection

#### 1. What did you find difficult about working with code that was drafted by GenAI?

I did not find anything difficult while working with the code drafted by DukeGPT. This was because in part 2, commenting throughout the code helped me understand the code really well, hence I was able to make changes without much difficulty.

In general, I learnt that although LLMs are extremely smart, being able to pull data from anywhere on the internet to complete tasks, they may not always give the best result. Even after years, there are always new tasks that they may not be built to complete, causing them to make errors. It is only through continous prompts and human intervention can they give the best result.

#### 2. What prior knowledge did you rely on to make the suggested changes?

I have studied Physics HL in the IBDP, where we had lots of experiments with springs and spring constants. Hence, the suggested changes made lot of sense to me, and I knew exactly what I was supposed to change without even having to look at the code and find the places to make changes.

## Appendix

### Code—Generated Version

```python
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
```

### Code—Commented Version

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter # QUESTION: Is this the Matplotlib class that creates animations? ANSWER: Yes

m = 1.0 # Mass (kg)
k = 5.0 # Spring Constant (N/m)
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
mass_point, = ax1.plot([], [], 'ro', markersize=15) # Creates a red circle marker for the mass

def init_motion(): # Function to create the initial animated frame
    mass_point.set_data([], []) # Creates a blank frame to return
    return mass_point,

def update_motion(frame): # Function to update the blank frame
    y = -x[frame] # QUESTION: Does this find the value on the frame'th index in the x array and put it as y? ANSWER: Yes
    mass_point.set_data([0], [y]) # Moves the point from initial point to set point to return it
    return mass_point,

ani1 = FuncAnimation(fig1, update_motion, frames=len(t)//2, init_func=init_motion, blit=True) # Creates an animation
ani1.save('mass_spring_motion.gif', writer=PillowWriter(fps=20)) # Saves as a gif file
plt.show() # Shows the animation
plt.close(fig1) # Closes the animation

# Repeates the entire process for the second plot (line 14 and onwards)

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
```

### Code—Edited Version

```python
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
```