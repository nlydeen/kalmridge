#!/usr/bin/env python

import numpy as np

from matplotlib import pyplot as plt
from sys import argv


if __name__ == "__main__":
    if len(argv) == 2 and argv[1].endswith(".npy"):
        in_file = argv[1]
    else:
        print("Usage: ./1.plot_history.py <file.npy>")
        exit(1)

    history = np.load(in_file)

    labels = ["F", "h", "c", "b"]
    colors = ["blue", "green", "orange", "red"]

    plt.figure(dpi=300)

    for i in range(4):
        mean = history[:, 0, i]
        upper = mean + 0.5 * history[:, 1, i]
        lower = mean - 0.5 * history[:, 1, i]

        # log(c) -> c
        if i == 2:
            mean = np.exp(mean)
            upper = np.exp(upper)
            lower = np.exp(lower)

        plt.plot(mean, color=colors[i])
        plt.fill_between(np.arange(len(history)), lower, upper, alpha=0.25,
                         color=colors[i], label=labels[i])

    plt.axhline( 1, color="black", linestyle="--", linewidth=1)
    plt.axhline(10, color="black", linestyle="--", linewidth=1)

    plt.xlabel("Iteration")

    plt.xlim( 0, len(history) - 1)
    plt.ylim(-1, 15)

    plt.legend()

    out_file = ".".join(in_file.split(".")[:-1]) + ".png"
    plt.savefig(out_file, transparent=True)
