# Modeling Data

In this activity, you will practice plotting and learn how to model data by finding the best polynomial fit.

## Provided data

The file `fit_data.py` is provided and contains an ndarray of data in the variable `data`. The arrays were generated according to a physical formula, with a little bit of noise added, to create synthetic data.

This could represent experimental data for time (column at index 0), and $x$ and $y$ displacements for a physical object (columns at indices 1 and 2 respectively).

## Assignment

Your task is to create a mathematical model that describes how $x$ and $y$ displacements vary with time.

### Make a plan

If you were the experimentalist who gathered the data, you might already have physical principles in mind and an idea of what models might fit the data.

Sometimes, however, data scientists do something called *exploratory data analysis*, identifying general patterns in the data to guide what analysis to do next. This often involves plotting the data different ways to look for patterns. 

Even though you may not know precisely where the analysis will take you, you know your data has three columns, and you want to plot the dependent variables vs. the independent variable. You can break down this work into two high-level steps:

1. Store each column of the data in three arrays: `t`, `x`, and `y`
2. Plot the data
    * Create two plots: $x$ vs $t$ and $y$ vs $t$
    * Plot the data with markers, since it is "experimental"
    * Label the x-axis $t$ and the y-axes $x$ and $y$

Complex steps are good choices for functions, so you have two ideas for functions you can write and what names make sense.

You also know there are one or two things you might want to look up in the documentation:
* How do you get each column of a multidimensional array and assign it to a variable?
    * [Indexing and Slicing](https://numpy.org/doc/stable/user/absolute_beginners.html#indexing-and-slicing)
    * [The N-dimensional array (ndarray)](https://numpy.org/doc/stable/reference/arrays.ndarray.html#arrays-ndarray)
* How do you plot arrays with markers and label the axes?
    * See the content in Readings to review.

## Plot the data

Now that you have a plan and have looked up new information you need to execute it, you can write code to plot the data.

Create one figure with two subplots: 1) $x$ vs. $t$, and 2) $y$ vs. $t$.

Some tips:
1. We suggest using markers, since the data is "experimental." 
2. Plots always need labels on both axes.
3. Plots do *not* need titles if you are going to use them in a document where they will be captioned. Plots *do* need titles if they will not be captioned.

## Model the data

Now you are interested in finding a mathematical model that describes the data.

Statisticians have a saying "All models are wrong, but some are useful," attributed to George E. P. Box. Math can never exactly describe reality, but a good model is one that provides insight and allows you to make predictions.

Sometimes you have a physical law or theory that you can use as a starting point for modeling the data. Other times, you are looking for patterns and may need to try different mathematical relationships.

At this point, you might be able to state with some certainty what pattern the data follows, whether it is a straight line or a quadratic function.

### Polynomials in NumPy

The equation for a straight line is a specific case of a *polynomial*.  
Often, engineers will want to see if a data set fits a particular order of polynomial, and if so, what the best coefficients of that polynomial might be to have the data points collectively as close as possible to the model.  The general form for a polynomial can be written as:
$$
\begin{aligned}
y&=a_{0}x^0+a_{1}x^{1}+...+a_{N-1}x^{N-1}+ a_{N}x^N\\
&=\sum_{n=0}^{N}a_nx^n
\end{aligned}
$$

NumPy has a function called `np.polyfit()` to determine polynomial fits to data.  It takes three arguments:
1. An independent data set
2. A dependent data set
3. An integer N (the order fit desired)

This command, however, returns the values of
the polynomial coefficients in a slightly different order from that
shown above.  Specifically, if the variable `p` is where you have told Python to store the polynomial coefficients, the equation that
Python will fit for an Nth order polynomial is:
$$
\begin{aligned}
y&=p[0]~x^N+p[1]~x^{N-1}+...+p[N-1]~x^1+ p[N]~x^0
\\
&=\sum_{k=0}^{N}p[k]~x^{(N-k)}
\end{aligned}
$$
This is because of the way Python interprets arguments to functions
that are supposed to represent polynomials.  To clarify this further, 
some common polynomials are:

|Order | N | Example Equation | Polynomial Representation |
|---------|------------|--------|--------------|
|First Order | 1 | $y=3x+4$ | `p=[3, 4]` |
| Second Order | 2 | $y=3x^2+4x+5$ | `p=[3, 4, 5]`|
| Third Order | 3 | $y=3x^3+4x^2+5x+6$ | `p=[3, 4, 5, 6]` |
| Third Order | 3 | $y=3x^3+5x$ | `p=[3, 0, 5, 0]` |

Note in the last case that the far right entry in the array always represents the coefficient of the zeroth power—if that coefficient happens to be 0, you cannot simply omit it. Similarly, any
other "missing" coefficients must be represented by 0's in the
representational array for Python to be able to understand the
coefficients properly. 

### Create a model

For each of the two sets of data, determine "by eye" what order polynomial you want to try to fit.

Then use the array of polynomial coefficients returned by `np.polyfit()` to create a model. 

One of the models you are seeking is for time and displacement $x$. Now that you have the polynomial coefficient of the model, you need to generate an array to use for time (the independent variable).

Try this using the NumPy array creation techniques you have learned to generate the time model. A good choice for the time array is to have the same minimum and maximum as the experimental data, but with at least 100 points, so the model will look smooth when plotted.

Then, you need to evaluate the proposed polynomial function at each of these time points. NumPy provides a function `np.polyval()`. Consult its [documentation](https://numpy.org/doc/stable/reference/generated/numpy.polyval.html) to learn how to generate dependent data, given a polynomial and array of independent data.

### Plot the model 

Now, you can overlay the model arrays you have generated on the plot with data.

We recommend doing this with a line because the model is continuous.

For each of the two data sets, plot your chosen polynomial model and determine "by eye" whether the fit looks good. If it does not, try a different order polynomial.

## Example algorithm

Eventually, you want to be able to take a task such as
> "Given experimental data in a file, determine a model (or justify a physical model) for it, and evaluate the fit of the model."

and generate a reasonably detailed algorithm for how you will address this problem. There are several complex steps involved in something like this! Here is an example algorithm for the task of this activity.

1. Extract the data by columns from an n by 3 array into 3 arrays for time, $x$, and $y$ displacement.
2. Plot the data on one figure with two subplots: $x$ vs. $t$, and $y$ vs. $t$.
    1. Use a marker
    2. Label axes and title plot
3. For each plot,
    1. Estimate an order polynomial that will give a good fit.
    2. Generate a model for the chosen order of polynomial.
        * Use `polyfit()` to get the polynomial coefficients.
        * Create an array for the independent model.
        * Use `polyval()` to get a model of the dependent data.
    3. Plot the model overlaid on the data, and save the figure as `displacement_plot.png`.
    4. Evaluate the goodness of fit by eye.
4. Submit the following to Gradescope:
    1. Your code file `fit_data.py`. We will check that running your program creates a file named `displacement_plot.png`, but we will grade the plot manually.
	2. A markdown file `results.md` that states the polynomial found to fit each data set and contains your speculation of what what physical relationship is present in each one.

Once you are happy with your plan, go forth and code!

## Acknowledgements

The polynomial section is adapted from EGR 103L Fall 2023 Lab 2: Introduction to Python by Michael Gustafson. 

