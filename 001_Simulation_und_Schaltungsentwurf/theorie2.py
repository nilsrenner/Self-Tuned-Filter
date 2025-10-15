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
my_orange = (240/255, 120/255, 35/255)
my_purple = (120/255, 100/255, 165/255)
my_green2 = (110/255, 165/255, 60/255)
my_blue2 = (50/255, 180/255, 200/255)

#%% Phase Charakteristik des Multiplizierers

#plt.close('all')

x = np.linspace(0,np.pi,num=4)


y = -6.366197723675814*x + 10

plt.figure(1,figsize=(8,6))
plt.plot(x,y, color=my_blue, linewidth=2)
plt.grid(True, which='both', ls='--', lw=0.5)

plt.title('Phasencharakteristik des Multiplizierers')
plt.xlabel(r"$\phi \;[\mathrm{rad}]$")
plt.ylabel(r"$V_{\mathrm{av}}\;[\mathrm{V}]$")
#plt.tight_layout()

plt.xticks(
    [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi],
    [r"$0$", r"$\dfrac{\pi}{4}$", r"$\dfrac{\pi}{2}$", r"$\dfrac{3\pi}{4}$", r"$\pi$"]
)



#%% Simulationsdaten Semester 6

#=> aus "sim_data.py"

# Import auf KiCad
filepath = '004_schaltungsentwurf_no1/schaltungsentwurf_no1.raw'
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



#%% Multiplizierer DC

# Import auf KiCad
filepath = '003_analog_multiplier/analog_multiplier.raw'
l = Ltspice(filepath)  # jetzt funktioniert der Konstruktor
l.parse()
#print(l.variables)  # statt get_trace_names()


time = l.get_time() * 1000
in1_dc = l.get_data('v(in1_dc)')
in2_dc = l.get_data('v(in2_dc)')
out_dc = l.get_data('v(out_dc)')


plt.figure(4, figsize=(8,6), dpi=150)
plt.plot(time, in1_dc, color=my_blue, label = r'Input $X_1$',ls='-')
plt.plot(time, in2_dc, color=my_red, label = r'Input $Y_1$',ls='-')
plt.plot(time, out_dc, color=my_yellow, label = 'Output',ls='-')
plt.title('Demonstration mit DC-Spannungen')
plt.xlabel("Zeit [ms]")
plt.ylabel("Spannung [V]")
plt.legend()
plt.grid(True, which='both', ls='--', lw=0.5)
#plt.tight_layout()
plt.show()




#Simtime = 8ms !!!!!




#%% Sim Multiplizier

# Import auf KiCad
filepath = '003_analog_multiplier/analog_multiplier.raw'
l = Ltspice(filepath)  # jetzt funktioniert der Konstruktor
l.parse()
#print(l.variables)  # statt get_trace_names()

time = l.get_time() * 1000
in1 = l.get_data('v(mult1_y)')
in2 = l.get_data('v(in_0)')
in3 = l.get_data('v(in_90)')
in4 = l.get_data('v(in_180)')

out2 = l.get_data('v(mult_out_0)')
out3 = l.get_data('v(mult_out_90)')
out4 = l.get_data('v(mult_out_180)')


plt.figure(5, figsize=(14,6), dpi=150)
plt.subplot(121)
plt.plot(time, in2, color=my_blue, label = r'In: $\phi=0^\circ$',ls='-')
plt.plot(time, in3, color=my_red, label = r'In: $\phi=90^\circ$',ls='-')
plt.plot(time, in4, color=my_yellow, label = r'In: $\phi=180^\circ$',ls='-')
plt.title(r'Eingangssignale in $X_1$ für $\phi = 0^\circ-180^\circ$')
plt.xlabel("Zeit [ms]")
plt.ylabel("Spannung [V]")
plt.legend(loc='lower left')
plt.grid(True, which='both', ls='--', lw=0.5)

plt.subplot(122)
plt.plot(time, out2, color=my_blue, label = r'Out: $\phi=0^\circ$',ls='-')
plt.plot(time, out3, color=my_red, label = r'Out: $\phi=90^\circ$',ls='-')
plt.plot(time, out4, color=my_yellow, label = r'Out: $\phi=180^\circ$',ls='-')
plt.title(r'Multipliziererausgang')
plt.xlabel("Zeit [ms]")
plt.ylabel("Spannung [V]")
plt.legend(loc='lower left')
plt.grid(True, which='both', ls='--', lw=0.5)

plt.tight_layout()
plt.show()

#Simtime= 2ms
#\phi in rad!!!!!



#%% PD anch op

# Import auf KiCad
filepath = '003_analog_multiplier/analog_multiplier.raw'
l = Ltspice(filepath)  # jetzt funktioniert der Konstruktor
l.parse()
#print(l.variables)  # statt get_trace_names()

time = l.get_time() * 1000
op_out1 = l.get_data('v(detec_out0)')
op_out2 = l.get_data('v(detec_out90)')
op_out3 = l.get_data('v(detec_out180)')
op_out0 = l.get_data('v(op_out0)')
op_out90 = l.get_data('v(op_out90)')
op_out180 = l.get_data('v(op_out180)')


plt.figure(6, figsize=(14,6), dpi=150)
plt.subplot(121)
plt.plot(time, op_out1, color=my_blue, label = r'In: $\phi=0^\circ$',ls='-')
plt.plot(time, op_out2, color=my_red, label = r'In: $\phi=90^\circ$',ls='-')
plt.plot(time, op_out3, color=my_yellow, label = r'In: $\phi=180^\circ$',ls='-')
plt.title(r'Ausgang für eine OP verschaltung R= 1k')
plt.xlabel("Zeit [ms]")
plt.ylabel("Spannung [V]")
plt.ylim(0,4.55)
plt.legend(loc='lower left')
plt.grid(True, which='both', ls='--', lw=0.5)

plt.subplot(122)
plt.plot(time, op_out0, color=my_blue, label = r'Out: $\phi=0^\circ$',ls='-')
plt.plot(time, op_out90, color=my_red, label = r'Out: $\phi=90^\circ$',ls='-')
plt.plot(time, op_out180, color=my_yellow, label = r'Out: $\phi=180^\circ$',ls='-')
plt.title(r'Ausgang für R = 5k')
plt.xlabel("Zeit [ms]")
plt.ylabel("Spannung [V]")
plt.ylim(0,4.55)
plt.legend(loc='lower left')
plt.grid(True, which='both', ls='--', lw=0.5)

plt.tight_layout()
plt.show()





