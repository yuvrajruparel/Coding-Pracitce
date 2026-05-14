import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def get_data(filename: str) -> tuple[np.ndarray,np.ndarray]:
    """Read file with data in two columns into two np arrays"""
    data = np.loadtxt(filename) 
    t = data[:, 0]
    vc = data[:, 1]
    return t, vc


def voltage_lc_circuit(t: np.ndarray, v0: np.float64, LC: np.float64) -> np.ndarray:
    """Model voltage as a function of time with cosine"""
    return v0 * np.cos(np.sqrt(1 / LC) * t)


def get_lc_model(tdata: np.ndarray, vcdata: np.ndarray) -> np.ndarray:
    """Provided: Find the best fit model parameters for time and voltage data"""
    # curve_fit first argument: function to fit data to
    # curve_fit second and third arguments: x and y data to fit
    # curve_fit p0 argument: initial guesses for the model parameter values (v0 and LC here)
    # curve_fit returns tuple with first element the estimated model parameter values 
    #   (we will not use the second element)
    popt, _ = curve_fit(voltage_lc_circuit, tdata, vcdata, p0=[5, 0.08])
    return popt


def main():
    t, vc = get_data("lc_circuit_data.txt")

    plt.scatter(t, vc, label="Data", color="blue")

    v0_fit, LC_fit = get_lc_model(t, vc)
    vc_fit = voltage_lc_circuit(t, v0_fit, LC_fit)

    plt.plot(t, vc_fit, 'r-', label=f"Fit: v0={v0_fit:.2f}, LC={LC_fit:.3f}")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.legend()

    plt.savefig("lc_circuit_plot.png")
    plt.show()


if __name__ == '__main__':
    main()