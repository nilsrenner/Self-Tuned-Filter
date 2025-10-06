# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 13:30:36 2025

@author: nilsr
"""

# 
# filepath = r'C:\Users\nilsr\OneDrive\Desktop\Nils\001_Studium\006_Semester6\001_Analoge_Schaltungen\schaltungsentwurf_no1\schaltungsentwurf_no1.raw'
# l = ltspice.Ltspice(filepath)
# l.parse() # Data loading sequence. It may take few minutes for huge file.

# time = l.get_time()
# V1 = l.get_data('V(N1)')

# %% Init
from ltspice import Ltspice  # <-- das ist die richtige Klasse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Import auf KiCad
filepath = 'schaltungsentwurf_no1.raw'
l = Ltspice(filepath)  # jetzt funktioniert der Konstruktor
l.parse()
print(l.variables)  # statt get_trace_names()

freq = l.get_frequency()
LPF = l.get_data('v(/lpf)')
HPF = l.get_data('v(/hpf)')
BPF = l.get_data('v(/bpf)')
BSF = l.get_data('v(/bsf)')




# plt.plot(phase_lp)
# #Import der realen Daten
# #Bandpass
# bp10 = pd.read_csv(r'C:\Users\nilsr\OneDrive\Desktop\Nils\001_Studium\006_Semester6\001_Analoge_Schaltungen\Chap4\freq_sweep_bp_Q10.csv')
# bp10.columns = bp10.columns.str.strip()

# bp10_f = bp10['Frequency [Hz]']
# bp10_a = bp10['Amplitude [dB]']
# bp10_p = bp10['Phase [deg]']
# #r_bp10a_dB = 20 * np.log10(abs(bp10_a) + 1e-12)

# bp1 = pd.read_csv(r'C:\Users\nilsr\OneDrive\Desktop\Nils\001_Studium\006_Semester6\001_Analoge_Schaltungen\Chap4\freq_sweep_bp_Q1.csv')
# bp1.columns = bp1.columns.str.strip()

# bp1_f = bp1['Frequency [Hz]']
# bp1_a = bp1['Amplitude [dB]']
# bp1_p = bp1['Phase [deg]']

# #Bandsperre
# bs10 = pd.read_csv(r'C:\Users\nilsr\OneDrive\Desktop\Nils\001_Studium\006_Semester6\001_Analoge_Schaltungen\Chap4\freq_sweep_bs_Q10.csv')
# bs10.columns = bs10.columns.str.strip()

# bs10_f = bs10['Frequency [Hz]']
# bs10_a = bs10['Amplitude [dB]']
# bs10_p = bs10['Phase [deg]']


### Realteile der filter in dB
## Amplitudengang
real_LPF_dB = 20 * np.log10(abs(LPF) + 1e-12)
real_HPF_dB = 20 * np.log10(abs(HPF) + 1e-12)
real_BPF_dB = 20 * np.log10(abs(BPF) + 1e-12)
real_BSF_dB = 20 * np.log10(abs(BSF) + 1e-12)


## Phasengang
phase_lp = np.angle(LPF)
phase_hp = np.angle(HPF)
phase_bp = np.angle(BPF)
phase_bs = np.angle(BSF)




### Plot
# plt.figure(1,figsize = (8,6))
# plt.semilogx(freq, real_LPF_dB,label = 'Lowpass')
# plt.semilogx(freq, real_HPF_dB,label = 'Highpass')
# plt.semilogx(freq, real_BPF_dB,label = 'Bandpass')
# plt.semilogx(freq, real_BSF_dB,label = 'Bandstop')
# plt.xlabel("Frequenz [Hz]")
# plt.ylabel("Amplitude")
# plt.title('Frequenzsweep verschiedener Filtertypen')
# plt.legend()
# plt.grid()
# plt.show()

plt.figure(3,figsize=(8,6))
plt.semilogx(freq, phase_lp ,label = 'Lowpass')
plt.semilogx(freq, phase_hp ,label = 'Highpass')
plt.semilogx(freq, phase_bp ,label = 'Bandpass')
plt.semilogx(freq, phase_bs ,label = 'Bandstop')

plt.title('Phasengang aller Ausgänge des Biquads')
# plt.xlabel(r"$\phi \;[\mathrm{rad}]$")
# plt.ylabel(r"$V_{\mathrm{av}}\;[\mathrm{V}]$")

plt.xlabel("Frequenz [Hz]")
plt.ylabel("Phase [rad]")
plt.yticks(
    [-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
    [r"$-\pi$", r"$-\pi/2$", r"$0$", r"$+\pi/2$", r"$+\pi$"]
)

plt.legend()
plt.grid(True, which='both', ls='--', lw=0.5)
plt.show()

# plt.figure(3)
# #plt.semilogx(bs10_f,bs10_a, label = 'Praxis')
# plt.semilogx(freq, real_BSF_dB,label = 'Theorie')
# plt.xlabel("Frequenz [Hz]")
# plt.ylabel("Amplitude")
# plt.title('Frequenzsweep Bandsperre')
# plt.legend()
# plt.grid()
# plt.show()
