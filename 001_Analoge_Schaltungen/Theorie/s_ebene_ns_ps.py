# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 10:55:15 2025

@author: nilsr
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib.gridspec as gridspec

# Given values
R = 1e3
C = 1e-6
Q = 1/4
H0 = 1

# Calculate w0
w0 = 1 / (R * C)
#%%


# Define transfer function coefficients for s^2, s, and constant terms
a2 = 1 / w0**2
a1 = 1 / (w0 * Q)
a0 = 1

# Lowpass transfer function
num_LP = [0, 0, H0]
den_LP = [a2, a1, a0]

# Highpass transfer function
num_HP = [H0 / w0**2, 0, 0]
den_HP = [a2, a1, a0]

# Bandpass transfer function
num_BP = [0, -H0 / w0, 0]  # Hier: [0, -H0/w0, 0] für Bandpass, wenn du die Standardform willst
# (Dein MATLAB-Skript hatte num_BP = [-H0/w0, 0], aber das ist nicht korrekt für scipy.signal.tf2zpk,
# weil die Länge von num und den gleich sein muss. Wenn du die Standardform willst, nimm [0, -H0/w0, 0])
den_BP = [a2, a1, a0]

# Bandstop transfer function
num_BS = [-H0 / w0**2, 0, -H0]
den_BS = [a2, a1, a0]

# Funktion zum Plotten der Pol-/Nullstellen
def plot_pzmap(num, den, title, ax):
    # Nullstellen und Polstellen berechnen
    z, p, k = signal.tf2zpk(num, den)
    # Plot
    ax.plot(np.real(z), np.imag(z), 'o', markersize=10, markeredgecolor='b', markerfacecolor='none', label='Nullstellen')
    ax.plot(np.real(p), np.imag(p), 'x', markersize=10, color='r', label='Polstellen')
    ax.axhline(0, color='k', linestyle='--', linewidth=0.5)
    ax.axvline(0, color='k', linestyle='--', linewidth=0.5)
    ax.set_title(title)
    ax.set_xlabel('Re(s)')
    ax.set_ylabel('Im(s)')
    ax.legend(loc='upper right')
    ax.grid()
    ax.set_xlim(-1.25e3, 1.25e3)
    ax.set_ylim(-1.25e3, 1.25e3)

# Figure mit 4 Subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Plots erstellen
plot_pzmap(num_LP, den_LP, 'Lowpass Filter', axs[0, 0])
plot_pzmap(num_HP, den_HP, 'Highpass Filter', axs[0, 1])
plot_pzmap(num_BP, den_BP, 'Bandpass Filter', axs[1, 0])
plot_pzmap(num_BS, den_BS, 'Bandstop Filter', axs[1, 1])

plt.tight_layout()
plt.show()

# Einzelplot für den Bandpass
fig_bp, ax_bp = plt.subplots(figsize=(6, 5))
plot_pzmap(num_BP, den_BP, title= f'Bandpass Filter Q={Q}', ax=ax_bp)
plt.tight_layout()
plt.show()

#%% SOS zu a,b


# Korrekte SOS-Definition
sos_correct = [
    [0, -H0 * w0, 0, 1, w0/Q, w0**2]  # Bandpass-Charakteristik
]

b, a = signal.sos2tf(sos_correct)


print("Zähler (b):", b)  # Ausgabe: [ 0. -10000. 0.]
print("Nenner (a):", a)  # Ausgabe: [1.0e+00 1.0e+04 1.0e+08]

sys = signal.TransferFunction(b, a)
w, mag, phase = signal.bode(sys)

plt.figure(figsize=(10, 4))
plt.semilogx(w, mag)
plt.title('Bandpass-Filter 2. Ordnung')
plt.xlabel('Frequenz [rad/s]')
plt.ylabel('Verstärkung [dB]')
plt.grid()
plt.show()

#%%
# SOS-Definition für Bandpass
sos_correct = [
    [0, -H0 * w0, 0, 1, w0 / Q, w0 ** 2]
]

# In Zähler/Nennerform umwandeln
b, a = signal.sos2tf(sos_correct)

# Transferfunktion und Bodeplot
sys = signal.TransferFunction(b, a)
# w, mag, phase = signal.bode(sys)
w = np.logspace(-2, 5, 1000)    # von 10^-2 bis 10^5 rad/s
w, mag, phase = signal.bode(sys, w)


# Pol-/Nullstellen berechnen
z, p, k = signal.tf2zpk(b, a)

# Figure mit benutzerdefiniertem Grid
fig = plt.figure(figsize=(12, 5))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.75])  # Links quadratisch, rechts breiter

# 1. Plot: Pol-/Nullstellen (quadratisch)
ax1 = fig.add_subplot(gs[0])
ax1.set_aspect('equal')  # sorgt für quadratische Darstellung
ax1.plot(np.real(z), np.imag(z), 'o', markersize=10,
         markeredgecolor='b', markerfacecolor='none', label='Nullstellen')
ax1.plot(np.real(p), np.imag(p), 'x', markersize=10,
         color='r', label='Polstellen')
ax1.axhline(0, color='k', linestyle='--', linewidth=0.5)
ax1.axvline(0, color='k', linestyle='--', linewidth=0.5)
ax1.set_title(f'Pol-/Nullstellen-Diagramm (Q = {Q})')
ax1.set_xlabel('Re(s)')
ax1.set_ylabel('Im(s)')
ax1.legend(loc='upper right')
ax1.grid(True)
ax1.set_xlim(-1.25e3, 1.25e3)
ax1.set_ylim(-1.25e3, 1.25e3)

# 2. Plot: Bode-Magnitudengang (rechteckig)
ax2 = fig.add_subplot(gs[1])
ax2.semilogx(w, mag)
ax2.set_xlim(1e-2, 1e5)      # z. B. von 1 kRad/s bis 100 kRad/s
ax2.set_ylim(-100, 5)       # dB-Bereich, z. B. -40 dB bis +10 dB
ax2.set_title('Bode-Magnitudengang')
ax2.set_xlabel('Frequenz [rad/s]')
ax2.set_ylabel('Verstärkung [dB]')
ax2.grid(True)

plt.tight_layout()
plt.show()
