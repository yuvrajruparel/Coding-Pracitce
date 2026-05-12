# NumPy Problems

This assignment contains four physics and engineering problems solved using NumPy. Each problem is implemented in a separate Python file.

Make sure you have installed the `numpy` library before you begin.

## Problems

### Problem 1: Standard Normal Probability Density Function
(Adapted from Chapra 2.12)

The standard normal probability density function is a bell-shaped curve described by

$$ f(z) = \frac{1}{\sqrt{2 \pi}} e^{-\frac{z^2}{2}} $$

Implement code for the standard normal probability density function  with the following requirements.

**File:** `problem1_normal_distribution.py`

**Function:** `snp` 
- Takes an array `z` as a parameter 
- Returns an array that are the values of $f(z)$ as defined above

**Program:** 
- Generate 101 linearly spaced points for `z` between -4 and 4
- Call `snp` to find the values of the standard normal probability for those values of `z`
- Print out the maximum value of those values. Print only the number, to the precision of four digits after the decimal point.

Hint: if you want to learn how to use a new function, such as NumPy's `max`, search for its documentation by doing an internet search for "numpy.org max." The examples are usually near the bottom of the page.

---

### Problem 2: Spring Force and Energy
(Adapted from Chapra 2.13)

You may be familiar with Hook's law from physics; the force of a spring $F$ is proportional to its displacement $x$ by a spring constant $k$.

$$F = kx$$

The energy stored in that spring $U$ is given by:

$$U = \frac{1}{2} k x^2$$

Assume you have experimental data for the force and displacement of a spring:

| Force (N) | Displacement (m) |
|-----------|------------------|
| 14        | 0.013            |
| 18        | 0.020            |
| 8         | 0.009            |
| 9         | 0.010            |
| 13        | 0.012            |

Implement code to find the average spring constant and spring energy with the following requirements.

**File:** `problem2_spring_force.py`

**Functions:** 
1. `spring_const`, which takes an array of forces and an array of displacements as parameters and returns the average spring constant $k$ for the data.
2. `spring_energy`, which takes an array of forces and an array of displacements as parameters and returns an array of potential energies $U$ based on those arrays and the formulas given in the problem. Note: this function should use the $k$ calculated for each pair of data, not the average $k$.

**Program:**  
- Write code to define variables `force_data` and `disp_data`, and initialize them as arrays with the values shown in the table.
- Call `spring_const` to calculate the average $k$ of the data.
- Call `spring_energy` to find the array of $U$ for the provided data.
- Print the average $k$ and maximum $U$: only the numbers, one per line, to the precision of four digits after the decimal point.

---

### Problem 3: Water Density and Temperature
(Adapted from Chapra 2.14)

The density of pure water (kg/$\mathrm{m}^3$) at atmospheric pressure varies with temperature between the freezing point (0 C) and the boiling point (100 C). This relationship can be empirically described by the fourth order polynomial

$$ \rho = - 1.2329\times 10^{-7} T^4 + 4.11472\times10^{-5} T^3 - 0.00748423 T^2 + 0.0508007 T + 999.904 $$

where $\rho$ is the density in kg/$\mathrm{m}^3$ and $T$ is the temperature in C.

Implement code to create an array of density values with the following requirements.

**File:** `problem3_density_water.py`

**Function:** `calc_density_water` 
- Takes an array of temperatures as parameter
- Returns an array of corresponding densities

**Program:**
1. Generate an array of temperatures in Fahrenheit from 32 to 212 F in 3.6 F increments.
2. Convert this array to Celcius temperatures.
3. Call `calc_density_water` to find an array of densities.
4. Determine at what temperature Fahrenheit the maximum density occurs.
5. Print the temperature of the maximum density, only the number, to a precision of one digit after the decimal point.

---

### Problem 4: Air Drag and Terminal Velocity
(Adapted from Chapra 2.21)

The terminal velocity of a free-falling object, like a bungee jumper is

$$v_t = \sqrt{\frac{mg}{c_d}} $$

where $v_t$ is the terminal velocity (m/s), $m$ is the mass (kg), $g$ is the gravitational constant (9.81 m/$\mathrm{s}^2$), and $c_d$ is the drag coefficient (kg/m).

The drag coefficient $c_d$ actually depends on the density of the fluid and frontal area as well!

$$ c_d = \frac{C_D \rho A}{2} $$

where $C_D$ is a dimensionless drag coefficient, $\rho$ is the air density (kg/$\mathrm{m}^3$), and $A$ is the frontal area ($\mathrm{m}^2$).

Data for several bungee jumpers has been measured experimentally.

| Mass (kg) | Terminal velocity (m/s) | Area (m^2) |
|-----------|-------------------------|------------|
| 83.6      | 53.4                    | 0.455      |
| 60.2      | 48.5                    | 0.402      |
| 72.1      | 50.9                    | 0.452      |
| 91.1      | 55.7                    | 0.486      |
| 92.9      | 54.0                    | 0.531      |
| 65.3      | 47.7                    | 0.475      |
| 80.9      | 51.1                    | 0.487      |

Implement code to analyze the bungee jumper data with the following requirements.

**File:** `problem4_air_drag.py`

**Functions:** Write functions of your choosing to find:
1. The drag coefficient $c_d$ for each jumper
2. The dimensionless drag coefficient $C_D$ for each jumper (use 1.293 kg/m3 as the value for air density in this problem)
    
**Program:**
Write a program that calls your functions and prints out the following values. Print only the numbers, one per line, to the precision of four digits after the decimal point:

 * Minimum $c_d$
 * Maximum $c_d$
 * Average $c_d$
 * Minimum $C_d$
 * Maximum $C_d$
 * Average $C_d$
    
---

## Learning Objectives

These problems demonstrate:
- NumPy array operations and mathematical functions
- Scientific computing with Python
- Practical applications in physics and engineering
- Function implementation and testing
- Data analysis with arrays

## References

Problems adapted from Chapra's *Applied Numerical Methods with MATLAB for Engineers and Scientists*.
