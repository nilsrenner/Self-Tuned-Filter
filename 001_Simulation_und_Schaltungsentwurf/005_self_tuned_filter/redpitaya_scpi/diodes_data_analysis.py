# -*- coding: utf-8 -*-
"""
Messdatenauswertung

@author: T. Ziemann, M. Meiners
"""

# %% Init
# import os
import numpy as np
# import scipy.io as io
import pandas as pd
import matplotlib.pyplot as plt

# %% Einlesen der Daten
DEVICE = {
    "d1": "1N4001",
    "d2": "1N4148",
    "npn": "2N3904",
    "pnp": "2N3906",
    "nmos": "BS170",
    "pmos": "BS250"
}

Data_IN1 = 'data/IN1_' + DEVICE["d1"] + \
    "_ELIE4" + str(TSTAMP.strftime('_%Y-%m-%d_%H-%M'))
Data_IN2 = 'data/IN2_' + DEVICE["d1"] + \
    "_ELIE4" + str(TSTAMP.strftime('_%Y-%m-%d_%H-%M'))

# %% CSV/TSV Daten einlesen
DF_IN1 = pd.read_csv(Data_IN1 + '.csv')
DF_IN2 = pd.read_csv(Data_IN2 + '.csv')

# %% Parquet Daten einlesen
# DF_IN1 = pd.read_parquet(Data_IN1 + '.parquet')
# DF_IN2 = pd.read_parquet(Data_IN2 + '.parquet')

# %% MATLAB mat Daten einlesen
# DF_IN1 = io.loadmat(Data_IN1 + '.mat')
# DF_IN2 = io.loadmat(Data_IN2 + '.mat')

# %% Darstellung
t = np.linspace(0, 2.097e-3, 16384)  # Skalierung der Zeitachse
DF_MATH = (DF_IN1.mean(axis=1) - DF_IN2.mean(axis=1)) / 10e3

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Zeit t in ms')
ax1.set_ylabel('Spannung in V', color=color)
ax1.plot(t * 1e3, DF_IN1.mean(axis=1), color=color, label='IN1')
ax1.plot(t * 1e3,
         DF_IN2.mean(axis=1),
         color=color,
         linestyle='dashed',
         label='IN2')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid()

# Zweite y-Achse
ax2 = ax1.twinx()

# Achsenbeschriftung ax2
color = 'tab:red'
ax2.set_ylabel(r'Strom in $\mu$A', color=color)
ax2.plot(t * 1e3, DF_MATH * 1e6, color=color, label='MATH')
ax2.tick_params(axis='y', labelcolor=color)

# Gemeinsame Legende für beide Achsen
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc=0)

# Passt die zweite y-Achse an
fig.tight_layout()
plt.show()
