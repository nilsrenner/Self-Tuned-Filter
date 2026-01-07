#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 12:53:08 2025

@author: nils
"""

import numpy as np
import matplotlib.pyplot as plt

# Farben
my_blue  = (10/255, 85/255, 140/255)
my_red   = (195/255, 5/255, 35/255)
my_green = (0/255, 145/255, 90/255)

# Parameter
f_ref     = 1000.0       
f_current = 1000.0       
df_max    = 4.0         # maximale Schrittweite [Hz]
fs        = 200_000.0    
T         = 0.5      
t         = np.arange(0, T, 1/fs)

ref = np.sin(2*np.pi*f_ref*t)
sig = np.zeros_like(t)
phi_sig = 0.0            

time_log = []
freq_log = []
phase_log = []  # Phase in [-180,180]

prev_ref = ref[0]

# Proportionalfaktor
Kp = df_max / 90.0 * 0.3   # [Hz/°]

# --- Tiefpass-Parameter für delta_f ---
alpha = 0.25            # 0<alpha<=1, kleiner = stärker geglättet
delta_f_filt = 0.0       # Initialwert des gefilterten Stellsignals
# --------------------------------------

phi_offset = np.deg2rad(0.0)   # 45° Start-Phasendifferenz

for i in range(1, len(t)):
    sig[i] = np.sin(phi_sig + phi_offset)   # hier Offset addieren
    phi_sig += 2*np.pi*f_current/fs

    if prev_ref < 0 and ref[i] >= 0:
        # Exakte Interpolation
        dt = -prev_ref / (ref[i] - prev_ref) / fs
        t_exact = t[i-1] + dt
        
        phi_ref_exact = 2*np.pi*f_ref*t_exact % (2*np.pi)
        phi_sig_exact = phi_sig - 2*np.pi*f_current/fs*(1-dt)
        phi_sig_exact = phi_sig_exact % (2*np.pi)
        
        # Phasendifferenz [-pi, pi]
        phi_diff = phi_sig_exact - phi_ref_exact
        phi = ((phi_diff + np.pi) % (2*np.pi)) - np.pi
        
        phi_deg = np.degrees(phi)
        phase_log.append(phi_deg)

        # ---------- ROBUSTE SYMMETRISCHE REGELUNG UM 90° ----------
        phi_rel = phi_deg % 360.0

        if 0 <= phi_rel < 90:
            direction = +1
            dist = 90 - phi_rel
        elif 90 <= phi_rel < 180:
            direction = -1
            dist = phi_rel - 90
        elif 180 <= phi_rel < 270:
            direction = -1
            dist = 270 - phi_rel
        else:  # 270..360
            direction = +1
            dist = phi_rel - 270

        error = direction * dist   # [-90,90]

        # ungefiltertes Stellsignal
        delta_f_raw = Kp * error
        delta_f_raw = np.clip(delta_f_raw, -df_max, df_max)

        # -------- Tiefpassfilter auf delta_f --------
        # einfacher IIR: y[n] = (1-alpha)*y[n-1] + alpha*x[n]
        delta_f_filt = (1.0 - alpha) * delta_f_filt + alpha * delta_f_raw

        # gefiltertes Stellsignal anwenden
        f_current += delta_f_filt
        # --------------------------------------------

        time_log.append(t_exact)
        freq_log.append(f_current)

    prev_ref = ref[i]

# Plots
plt.figure(1, figsize=(12, 8))
plt.subplot(211)
plt.plot(time_log, freq_log, color=my_blue, label='f_current')
plt.axhline(y=f_ref, color=(0,0,0), linestyle='--', alpha=0.5, label='f_ref')
plt.title("Frequenzverlauf")
plt.xlabel("Zeit [s]"); plt.ylabel("Frequenz [Hz]")
plt.grid(True)
plt.legend(loc='lower left')

plt.subplot(212)
plt.plot(time_log, phase_log, '.', color=my_green)
plt.axhline(y=90,  color='r', linestyle=':', alpha=0.5, label='90° Grenze')
plt.axhline(y=-90, color='r', linestyle=':', alpha=0.5)
plt.title("Phasendifferenz")
plt.xlabel("Zeit [s]"); plt.ylabel("Phase [°]")
plt.grid(True)
plt.legend(loc='lower left')

plt.tight_layout()
plt.show()
