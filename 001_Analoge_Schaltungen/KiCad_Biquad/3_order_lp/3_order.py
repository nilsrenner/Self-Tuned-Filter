# -*- coding: utf-8 -*-
"""
Created on Sun May 18 14:59:25 2025

@author: nilsr
"""

# %% Init
from ltspice import Ltspice  # <-- das ist die richtige Klasse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal as signal




#%% Import auf KiCad
filepath = r"C:\Users\nilsr\OneDrive\Desktop\Nils\001_Studium\006_Semester6\001_Analoge_Schaltungen\3_order_lp\schaltungsentwurf_no1.raw"
l = Ltspice(filepath)  # jetzt funktioniert der Konstruktor
l.parse()
print(l.variables)  # statt get_trace_names()

freq = l.get_frequency()
LPF = l.get_data('v(/lpf)')
LPF3 = l.get_data('v(/lpf3)')
LPF3i = l.get_data('v(/inf_lpf3)')


real_LPF_dB = 20 * np.log10(abs(LPF) + 1e-12)
real_LPF3_dB = 20 * np.log10(abs(LPF3) + 1e-12)
real_LPF3i_dB = 20 * np.log10(abs(LPF3i) + 1e-12)

phase_LPF = np.angle(LPF)
phase_LPF3 = np.angle(LPF3)
phase_LPF3i = np.angle(LPF3i)


#%%



H0 = 1
N3 = 3
N2 = 2
Wn = 1000
f0 = Wn/(2*np.pi)
frequencies = np.logspace(1, 5, 1000)  # von 10^1 bis 10^5 rad/s

b3,a3 = signal.butter(N3,Wn,btype='low', analog=True)
b3 = b3*H0
w3, h3 = signal.freqs(b3, a3, worN=frequencies)
h3_angle = np.angle(h3)

b2,a2 = signal.butter(N2,Wn,btype='low', analog=True)
b2 = b2*H0
w2, h2 = signal.freqs(b2, a2, worN=frequencies)
h2_angle = np.angle(h2)


#Bode-Diagramm

#plt.figure(2)
#plt.semilogx(w3 / (2*np.pi), h3_angle)
# plt.semilogx(w3 / (2*np.pi), 20 * np.log10(abs(h3)))
# plt.axvline(f0, color='green') # cutoff frequency
# plt.title('3nd Order Butterworth Low Pass Filter')
# plt.xlabel('Frequency [Hz]')
# plt.ylabel('Amplitude [dB]')
# plt.grid()
# plt.show()


#%%

plt.figure(1)
plt.subplot(2, 1, 1)
plt.semilogx(freq, real_LPF_dB,label = 'LP Order 2sim')
plt.semilogx(freq, real_LPF3_dB,label = 'LP Order 3sim')
plt.semilogx(freq, real_LPF3i_dB,label = 'LP Order 3sim inv')
plt.semilogx(w2 / (2*np.pi), 20 * np.log10(abs(h2)),label = 'LP Order 2but')
plt.semilogx(w3 / (2*np.pi), 20 * np.log10(abs(h3)), label = 'LP Order 3but')
#plt.axvline(f0, color='green') # cutoff frequency
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude")
plt.title('Bode Plot: Magnitude')
plt.legend()
plt.grid()
plt.show()

plt.subplots_adjust(hspace=0.5)

plt.subplot(2, 1, 2)
plt.semilogx(freq, phase_LPF,label = 'LP Order 2sim')
plt.semilogx(freq, phase_LPF3,label = 'LP Order 3sim')
plt.semilogx(freq, phase_LPF3i,label = 'LP Order 3sim inv')
plt.semilogx(w2 / (2*np.pi), h2_angle,label = 'LP Order 2but')
plt.semilogx(w3 / (2*np.pi), h3_angle, label = 'LP Order 3but')

plt.title('Bode Plot: Phase')
plt.xlabel('f in Hz')
plt.ylabel('Phase in deg')
plt.legend()
plt.grid()
plt.show()


plt.figure(2)
plt.semilogx(freq, real_LPF_dB,label = 'LP Order 2sim')
plt.semilogx(freq, real_LPF3_dB,label = 'LP Order 3sim')
plt.semilogx(freq, real_LPF3i_dB,label = 'LP Order 3sim inv')
plt.semilogx(w2 / (2*np.pi), 20 * np.log10(abs(h2)),label = 'LP Order 2but')
plt.semilogx(w3 / (2*np.pi), 20 * np.log10(abs(h3)), label = 'LP Order 3but')
#plt.axvline(f0, color='green') # cutoff frequency
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude")
plt.title('Bode Plot: Magnitude')
plt.legend()
plt.grid()
plt.show()



