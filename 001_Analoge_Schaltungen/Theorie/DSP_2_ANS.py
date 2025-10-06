# -*- coding: utf-8 -*-
"""
Created on Sun May 18 10:46:10 2025

@author: nilsr
"""

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# Filterparameter
N = 2
R = 1000
C = 1e-06
H0 = 1                      #Verstärkungsf.
Q = 0.707
Q_butter = 0.707
Rq = Q * R
Rho = R/H0


w0 = 1 / (R * C)
f0 = w0 / (2 * np.pi)       # Cutoff frequency in Hz 
fs = 10000                  # Sampling frequency in Hz (nur relevant für digital)

# Butterworth Biquad (analog)
b, a = signal.butter(N, Wn=2*np.pi*f0, btype='low', analog=True)
b = b * H0

# Übertragungsfunktion anzeigen
print("Zählerkoeffizienten (b):", b)
print("Nennerkoeffizienten (a):", a)

# Bode-Diagramm
w, h = signal.freqs(b, a)
plt.figure(1)
plt.semilogx(w / (2*np.pi), 20 * np.log10(abs(h)))
plt.axvline(f0, color='green') # cutoff frequency
plt.title('2nd Order Butterworth Low Pass Filter')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.grid()
plt.show()

# Anzeige
print("w0 = {:.2f} rad/s, f0 = {:.2f} Hz, Q (Butterworth) = {:.3f}".format(w0, f0, 1/np.sqrt(2)))
#%%

#Aufgabe 4.4.1


H0 = 10

N = 3
Wn = 1000
f0 = 10000


b,a = signal.butter(N,Wn,btype='low', analog=True)
b = b*H0


# Bode-Diagramm
w, h = signal.freqs(b, a)
plt.figure(2)
plt.semilogx(w / (2*np.pi), 20 * np.log10(abs(h)))
plt.axvline(f0, color='green') # cutoff frequency
plt.title('3nd Order Butterworth Low Pass Filter')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.grid()
plt.show()

#%%

# Aufgabe 4.4.2

f0 = 50
N = 3
H0 = 10
bw = 10

f1 = f0-bw
f2 = f0+bw
Wn = [2*np.pi*f1,2*np.pi*f2]

b,a = signal.butter(N, Wn, btype='bandstop', analog=True)
b = b * H0


# Bode-Diagramm
w, h = signal.freqs(b, a)
plt.figure(3)
plt.semilogx(w / (2*np.pi), 20 * np.log10(abs(h)))
plt.axvline(f1, color='green') # cutoff frequency
plt.axvline(f2, color='green') # cutoff frequency
plt.title('3nd Order Butterworth Bandstop Filter')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.grid()
plt.show()



