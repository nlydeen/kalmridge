#!/usr/bin/env python

import pandas as pd

from matplotlib import pyplot as plt
from scipy.interpolate import interp1d


kalmridge = pd.read_csv("kalmridge.csv")
iglesias = pd.read_csv("iglesias.csv")

f_kalmridge = interp1d(kalmridge["x"], kalmridge["y"], kind="linear", fill_value="extrapolate")
f_iglesias = interp1d(iglesias["x"], iglesias["y"], kind="linear", fill_value="extrapolate")

x_kalmridge = list(range(0, 24+1))
y_kalmridge = [f_kalmridge(i) for i in x_kalmridge]
x_iglesias = list(range(1, 14+1))
y_iglesias = [f_iglesias(i) for i in x_iglesias]

#plt.plot(y_kalmridge)
#plt.plot(y_iglesias)
#plt.show()

fig, ax1 = plt.subplots()

line1, = ax1.plot(x_kalmridge, y_kalmridge, color="#a3be8c", label="KalmRidge")
ax2 = ax1.twinx()
line2, = ax2.plot(x_iglesias, y_iglesias, color="#81a1c1", label="Iglesias & Yang (2021)")
lines = [line1, line2]
labels = ["KalmRidge", "Iglesias & Yang (2021)"]
plt.title(r"$-\log_{10}(\lambda)$")
ax1.set_xlabel("Iteration")
ax1.legend(lines, labels)
plt.savefig("lambdas.png")
