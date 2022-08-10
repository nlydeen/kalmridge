import numpy as np

from numba import njit
from scipy.integrate import solve_ivp


def integrate(x_0, theta, T=100., dt=0.1, K=36, J=10):
    F, h, log_c, b = theta
    c = np.exp(log_c)

    @njit
    def dx_dt(t, x):
        X, Y = np.split(x, [K])

        Y_ = Y.reshape(K, J)
        Y_bar = []

        for i in range(K):
            Y_bar.append(Y_[i].mean())

        Y_bar = np.array(Y_bar)

        dx_dt = np.zeros(K * (J + 1))
        dX_dt, dY_dt = np.split(dx_dt, [K])

        for k in range(-1, K - 1):
            dX_dt[k] = \
                -X[k - 1] * (X[k - 2] - X[k + 1]) - X[k] + F - h * c * Y_bar[k]

            for j in range(J):
                dY_dt[j + k * J] = \
                    - c * b * Y[(j + 1) + k * J] \
                      * (Y[(j + 2) + k * J] - Y[(j - 1) + k * J]) \
                    - c * Y[j + k * J] + (h * c / J) * X[k]

        return dx_dt

    return solve_ivp(dx_dt, (0, T + dt), x_0,
                     t_eval=(np.arange(0, T, dt) + dt),
                     atol=0.01, rtol=0.01, method="DOP853").y
