# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


#%% Init.

from ltspice import Ltspice  # <-- das ist die richtige Klasse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#%% HSB Farben

my_blue = (10/255,85/255,140/255)      #x/255 da HTMP bis 255 sene Farbscala hat und Matplotlib bis 1
my_red = (195/255, 5/255, 35/255)
my_green = (0/255, 145/255, 90/255)
my_yellow = (250/255, 190/255, 0/255)


#%% Phase Charakteristik des Multiplizierers

plt.close('all')

x = np.linspace(0,np.pi,num=4)


y = -6.366197723675814*x + 10

plt.figure(1,figsize=(8,6))
plt.plot(x,y, color=my_blue, linewidth=2)
plt.grid(True, which='both', ls='--', lw=0.5)

plt.title('Phasencharakteristik des Multiplizierers')
plt.xlabel(r"$\phi \;[\mathrm{rad}]$")
plt.ylabel(r"$V_{\mathrm{av}}\;[\mathrm{V}]$")

plt.xticks(
    [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi],
    [r"$0$", r"$\dfrac{\pi}{4}$", r"$\dfrac{\pi}{2}$", r"$\dfrac{3\pi}{4}$", r"$\pi$"]
)



#%% Simulationsdaten Semester 6

#=> aus "sim_data.py"

# Import auf KiCad
filepath = 'schaltungsentwurf_no1/schaltungsentwurf_no1.raw'
l = Ltspice(filepath)  # jetzt funktioniert der Konstruktor
l.parse()
print(l.variables)  # statt get_trace_names()

freq = l.get_frequency()
LPF = l.get_data('v(/lpf)')
HPF = l.get_data('v(/hpf)')
BPF = l.get_data('v(/bpf)')
BSF = l.get_data('v(/bsf)')

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


plt.figure(3,figsize=(8,6), dpi=150)
plt.semilogx(freq, phase_lp, color=my_blue, label = 'Lowpass',ls='-')
plt.semilogx(freq, phase_hp, color=my_red, label = 'Highpass',ls='-')
plt.semilogx(freq, phase_bp, color=my_green, label = 'Bandpass',ls='-')
plt.semilogx(freq, phase_bs, color=my_yellow, label = 'Bandstop', ls='--')

plt.title('Phasengang aller Ausgänge des Biquads')
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Phase [rad]")
plt.yticks(
    [-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
    [r"$-\pi$", r"$-\pi/2$", r"$0$", r"$+\pi/2$", r"$+\pi$"]
)

plt.legend()
plt.grid(True, which='both', ls='--', lw=0.5)
plt.show()








