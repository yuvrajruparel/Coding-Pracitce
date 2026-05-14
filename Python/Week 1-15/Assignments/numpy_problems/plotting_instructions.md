# Plotting for NumPy Problems

Complete the NumPy problems, then add the following plots for each.

## Plots

### Problem 1: Standard Normal Probability Density Function

Plot f(z) vs. z from this problem. Label the axes z and f(z), and title the plot "Standard normal probability density function."

---

### Problem 2: Spring Force and Energy

Create a plot with two subplots:

1. Plot the experimental force data vs. displacement as blue circles. Overlay the line described by Hook's law, using your average k.
2. Plot the experimental energy vs. displacement as green exes.

Label the x-axis "Displacement (m)", and the y-axes "Force (N)" and "Energy (J)", respectively.

---

### Problem 3: Water Density and Temperature

Using the array of celsius temperatures and density, include the following on one plot.

- Plot of density vs. temperature in celsius
- A red 'x' where the maximum density occurs 
- A text label just above the maximum density "max density." (You may need to change the axes limits to see the text well. Consult the documentation for `Axes.set_ylim`.)

---

### Problem 4: Air Drag and Terminal Velocity

You have arrays of experimental data for mass, terminal velocity, and area, as well as functions to calculate the drag coefficient and the nondimensional drag coefficient.

On one figure with two subplots, plot the drag coefficients vs. mass as follows:

- Plot the drag coefficient $c_d$ vs. mass as `'*'`s connected by lines. Plot a horizontal line at the average value.
- Plot the dimensionless drag coefficient $C_D$ vs. mass as points. Plot a horizontal line at the average value.

Note: if you plot these data in unsorted order, connecting the lines by points will look confusing. Since you are plotting with mass on the x-axis, for the line through experimental data to be somewhat meaningful, sort the mass data, and order the terminal velocity and area data in the same order of the mass. See the documentation for NumPy `argsort` to do this.

## Submission

For each problem, write the code to save the figure generated as "problemX.png". Add/commit/push all four of these files to git to submit.