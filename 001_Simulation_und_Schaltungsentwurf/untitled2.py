#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 13:45:29 2025
Repaired by assistant: double-exponential (2nd-order) lowpass operates at measurement rate.
"""

import numpy as np
import matplotlib.pyplot as plt

# Farben
my_blue  = (10/255, 85/255, 140/255)
my_red   = (195/255, 5/255, 35/255)
my_green = (0/255, 145/255, 90/255)

# Parameter
f_ref     = 1000.0
f_current = 1015.0
df_max    = 4.0         # maximale Schrittweite [Hz]
fs        = 200_000.0
T         = 0.5
t         = np.arange(0, T, 1/fs)

# Start-Phasenoffset zwischen ref und sig
phi_offset = np.deg2rad(60.0)

ref = np.sin(2*np.pi*f_ref*t)
sig = np.zeros_like(t)
phi_sig = 0.0

time_log  = []
freq_log  = []
phase_log = []

prev_ref = ref[0]

Kp = df_max / 90.0 * 0.2   # [Hz/°] - beibehalten, kann feinjustiert werden

# --- 2nd-order lowpass als Kaskade zweier 1.Ordnung-Exponentialfilter ---
f_cut = 20.0    # Grenzfrequenz des Filters in Hz (try: 10..50)
# Filterzustände (je Filterstufe)
y1 = 0.0
y2 = 0.0
last_update_time = 0.0
# --------------------------------------------------------------------

# ----- initialer Phasenwert -----
phi_ref_0 = 0.0
phi_sig_0 = phi_sig + phi_offset
phi_diff_0 = ((phi_sig_0 - phi_ref_0 + np.pi) % (2*np.pi)) - np.pi
phi_deg_0 = np.degrees(phi_diff_0)

time_log.append(0.0)
freq_log.append(f_current)
phase_log.append(phi_deg_0)
# -------------------------------------------------------

for i in range(1, len(t)):
    sig[i] = np.sin(phi_sig + phi_offset)
    phi_sig += 2*np.pi*f_current/fs

    # steigender Nulldurchgang
    if prev_ref < 0 and ref[i] >= 0:
        # exakte Interpolation des Null-Durchgangs
        dt = -prev_ref / (ref[i] - prev_ref) / fs
        t_exact = t[i-1] + dt

        # Referenzphase zum exakten Zeitpunkt
        phi_ref_exact = (2*np.pi*f_ref*t_exact) % (2*np.pi)

        # zurückrechnen der sig-Phase zum exakten Zeitpunkt
        # (phi_sig ist bereits für aktuellen Sample-Index i aufgefüllt)
        phi_sig_exact = phi_sig - 2*np.pi*f_current/fs*(1 - dt)
        phi_sig_exact = (phi_sig_exact + phi_offset) % (2*np.pi)

        # Phasendifferenz [-pi, pi]
        phi_diff = phi_sig_exact - phi_ref_exact
        phi = ((phi_diff + np.pi) % (2*np.pi)) - np.pi
        phi_deg = np.degrees(phi)
        phase_log.append(phi_deg)

        # ---------- symmetrische Regelung um 90° ----------
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
        else:
            direction = +1
            dist = phi_rel - 270

        error = direction * dist        # [-90, 90]

        # Proportionale Stellgröße (roh)
        delta_f_raw = Kp * error
        delta_f_raw = np.clip(delta_f_raw, -df_max, df_max)

        # ---------- Diskreter 2. Ordnung (approx) auf Messrate ----------
        # dt_measure = Zeit seit letzter Messung (wichtig!)
        dt_measure = t_exact - last_update_time if last_update_time != 0.0 else 1.0 / f_ref
        # Guard: minimale dt (vermeidet div/0)
        if dt_measure <= 0:
            dt_measure = 1.0 / f_ref

        # Berechne alpha für Exponentialfilter bei dieser Messrate
        # alpha = 1 - exp(-2*pi*f_cut*dt)
        alpha = 1.0 - np.exp(-2.0 * np.pi * f_cut * dt_measure)

        # Kaskadiere zwei identische 1.Ordnung-Filterstufen (annähernd 2.Ordnung)
        y1 = (1.0 - alpha) * y1 + alpha * delta_f_raw
        y2 = (1.0 - alpha) * y2 + alpha * y1

        delta_f_filt = y2

        last_update_time = t_exact
        # ---------------------------------------------------------------

        # Frequenz anpassen (optional: begrenzen)
        f_current += delta_f_filt
        # optional: beschränke f_current sinnvoll, z.B. +/- 100 Hz um f_ref
        f_current = np.clip(f_current, f_ref - 200.0, f_ref + 200.0)

        time_log.append(t_exact)
        freq_log.append(f_current)

    prev_ref = ref[i]

# Plots
plt.figure(1, figsize=(12, 8))
plt.subplot(211)
plt.plot(time_log, freq_log, color=my_blue, label='f_current')
plt.axhline(y=f_ref, color=(0,0,0), linestyle='--', alpha=0.5, label='f_ref')
plt.title("Frequenzverlauf")
plt.xlabel("Zeit [s]")
plt.ylabel("Frequenz [Hz]")
plt.grid(True)
plt.legend(loc='lower left')

plt.subplot(212)
plt.plot(time_log, phase_log, '.', color=my_green)
plt.axhline(y=90,  color='r', linestyle=':', alpha=0.5, label='90° Grenze')
plt.axhline(y=-90, color='r', linestyle=':', alpha=0.5)
plt.title("Phasendifferenz")
plt.xlabel("Zeit [s]")
plt.ylabel("Phase [°]")
plt.grid(True)
plt.legend(loc='lower left')

plt.tight_layout()
plt.show()
