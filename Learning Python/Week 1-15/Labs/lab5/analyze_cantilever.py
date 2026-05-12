import numpy as np
import matplotlib.pyplot as plt

def analyze_plot_data_file(filename):
    """
    Reads data from a cantilever beam experiment, fits a linear model to
    find the compliance and initial deflection, plots deflection vs. force,
    saves the figure as a PNG file with the same base name as the data file,
    and returns an ndarray of the model parameters.
    """
    data = np.loadtxt(filename)
    mass = data[:, 0]
    deflection = data[:, 1] * 0.0254
    force = 9.81 * mass

    best = np.polyfit(force, deflection, 1)
    compliance = best[0]
    initial_deflection = best[1]
    plot_name = filename.split(".")[0]
    plot_name = plot_name.split("/")[1]+".png"

    dmodel = np.polyval(best, force)
    plt.plot(force, deflection, "bx", label="Data")
    plt.plot(force, dmodel, "b-", label="Model")
    plt.xlabel("Force (N)")
    plt.ylabel("Deflection (m)")
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.savefig(plot_name)
    plt.close()

    return np.array([compliance, initial_deflection])

def main():
    for filename in ['data/beam1.dat', 'data/beam2.dat', 'data/beam3.dat', 'data/cantilever.dat']:
        parameters = analyze_plot_data_file(filename)
        compliance, initial_deflection = parameters
        shortname = filename.split('/')[-1]
        print(f"{shortname}: {compliance:.4e}, {initial_deflection:.4e}")

if __name__ == "__main__":
    main()