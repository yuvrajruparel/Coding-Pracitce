import numpy as np
from functools import partial


def f(t, X, m, c, k, F_fn):
    """dX/dt = [v, (F − c·v − k·x) / m]"""
    x, v = X
    return np.array([v, (F_fn(t) - c*v - k*x) / m])


def rk4_step(f, t, X, dt):
    k1 = f(t,        X)
    k2 = f(t + dt/2, X + (dt/2)*k1)
    k3 = f(t + dt/2, X + (dt/2)*k2)
    k4 = f(t + dt,   X + dt*k3)
    return X + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)


def simulate(m, c, k, x0, v0, F_fn, t_end=20.0, dt=0.01):
    f_bound = partial(f, m=m, c=c, k=k, F_fn=F_fn)
    n = int(t_end / dt) + 1
    t_arr = np.linspace(0, t_end, n)
    X = np.zeros((n, 2))
    X[0] = [x0, v0]
    for i in range(n - 1):
        X[i+1] = rk4_step(f_bound, t_arr[i], X[i], dt)
    return t_arr, X


def regime(m, c, k):
    zeta = c / (2 * (m*k)**0.5)
    if abs(zeta - 1) < 1e-3: return "critical"
    return "underdamped" if zeta < 1 else "overdamped"