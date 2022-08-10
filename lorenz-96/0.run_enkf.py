#!/usr/bin/env python

import numpy as np
import xarray as xr

from datetime import datetime
from multiprocessing import Pool
from os import getpid
from rpy2.robjects import globalenv, numpy2ri, r
from time import time
from tqdm import trange
from warnings import filterwarnings

from l96 import integrate


# ---- BEGIN CONFIGURATION ---- #

ref_file = "reference.nc"  # Reference integration file.

N = 25    # Number of iterations.
E = 100   # Ensemble size.
T = 100.  # Integration time.

n_workers = 12  # Number of parallel integrations.

# ----- END CONFIGURATION ----- #


data = xr.open_dataset(ref_file)

X = data.X.data
Y = data.Y.data
x = np.concatenate([X, Y.reshape(len(X), -1)], axis=1)

dt = float(data.t[1] - data.t[0])


def compute_moments(x):
    K, J = data.Y.shape[1:]

    X, Y = np.split(x, [K], axis=1)
    Y.shape = (-1, K, J)
    Y_bar = Y.mean(axis=2)

    return np.array([X, Y_bar, X**2, X * Y_bar, (Y**2).mean(axis=2)]
                   ).swapaxes(0, 1).reshape(len(X), -1)



def integrate_member(theta):
    np.random.seed((getpid() * int(time())) % 123456789)

    x_0 = x[np.random.randint(len(x))]
    x_hat = integrate(x_0, theta, T, dt, *data.Y.shape[1:])

    return compute_moments(x_hat.T)


def integrate_ensemble(thetas):
    with Pool(n_workers) as pool:
        return np.moveaxis(np.array(pool.map(integrate_member, thetas)), 0, 2)


def update_ensemble(fs_ref, fs_ens, thetas):
    r["source"]("../parameter.est.enkf.R")
    numpy2ri.activate()
    thetas = np.array(
        globalenv["parameter.est.enkf"](fs_ref, fs_ens, thetas)[2]).T
    numpy2ri.deactivate()

    return thetas, integrate_ensemble(thetas)


def compute_means_iqrs(thetas):
    theta_mean = thetas.mean(axis=0)
    theta_iqr = np.diff(np.percentile(thetas, [25, 75], axis=0),
                        axis=0).squeeze()

    return theta_mean, theta_iqr


if __name__ == "__main__":
    filterwarnings("ignore")

    history = []

    thetas  = np.random.normal(0, 1, (E, 4))
    thetas *= np.sqrt(np.array([10., 1., 0.1, 10.])).reshape(1, -1)
    thetas += np.reshape(np.array([10., 0., 2., 5.]), (1, -1))

    history.append(compute_means_iqrs(thetas))

    fs_ref = compute_moments(x)
    fs_ens = integrate_ensemble(thetas)

    for _ in trange(N):
        thetas, fs_ens = update_ensemble(fs_ref, fs_ens, thetas)

        history.append(compute_means_iqrs(thetas))

    out_file = datetime.utcnow().astimezone().strftime("%Y%m%d.%H%M%SZ.npy")
    np.save(out_file, np.array(history))
