# KalmRidge

This repository contains an implementation of the KalmRidge.
Prerequisite packages are listed in a Conda environment file.
Install Conda (if necessary), then execute `conda env create -f environment.yml`.

To initialize the algorithm for CESM2, modify `./cesm2/run_specs/000.csv` to configure the initial ensemble.
Then, edit `./cesm2/common.py` to select your reference case, UCAR account, etc.
Delete any other files in the `run_specs` directory, as this implementation does not yet support multiple cases.
Change your working directory to `./cesm2`.
If you have never used this code before, then execute `./0.extract_restarts.sh` and `./2.compute_laplacians.py` on Casper (not Cheyenne).
Then, execute `./1.submit_runs.py` on Cheyenne to integrate the initial ensemble, followed by `./2.compute_laplacians.py` and `./3.run_enkf.py`.
Repeat the steps in the preceding sentence to iterate.
Finally, execute `./4.plot_history.py` to visualize the results in `history.png`.

To run the algorithm with Lorenz 96, change your working directory to `./lorenz-96`, then execute `./0.run_enkf.py` and `./1.plot_history.py`.
