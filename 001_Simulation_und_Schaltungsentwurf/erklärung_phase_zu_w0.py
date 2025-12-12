#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 14:30:58 2025

@author: nils
"""


my_blue = (10/255,85/255,140/255)      #x/255 da HTMP bis 255 sene Farbscala hat und Matplotlib bis 1
my_red = (195/255, 5/255, 35/255)
my_green = (0/255, 145/255, 90/255)
my_orange = (240/255, 120/255, 35/255)
my_blue2 = (50/255, 180/255, 200/255)

#%%
import numpy as np
import matplotlib.pyplot as plt

# Grundparameter
f1 = 1000       # Hz, erste Frequenz
f2 = 1100       # Hz, zweite Frequenz
fs = 200000     # Samplingfrequenz
T = 2e-3        # Gesamtdauer in Sekunden

t = np.linspace(0, T, int(fs*T), endpoint=False)

# Zwei Frequenzen, die alle halbe Periode wechseln
signal = np.zeros_like(t)
period = 1/f1    # Periode der Grundfrequenz

for i, ti in enumerate(t):
    if (ti % (period/2)) < (period/4):
        f = f1
    else:
        f = f2
    signal[i] = np.sin(2*np.pi*f*ti)

plt.plot(t*1000, signal)
plt.xlabel("t / ms")
plt.ylabel("Amplitude")
plt.title("Sinussignal mit leicht variierender Frequenz")
plt.grid(True)
plt.tight_layout()
plt.show()

#%%

import numpy as np
import matplotlib.pyplot as plt




def find_zeros(x, y):
    """
    Findet Nullstellen eines diskreten Signals y(x) mittels
    Vorzeichenwechsel + linearer Interpolation.
    
    Parameter:
        x : array_like
            Zeit- bzw. Werte-Achse
        y : array_like
            Signalwerte
    
    Rückgabe:
        zeros : ndarray
            Exakt interpolierte Nullstellenpositionen
    """
    x = np.asarray(x)
    y = np.asarray(y)

    # Indexstellen der Vorzeichenwechsel finden
    idx = np.where(np.diff(np.sign(y)))[0]

    # lineare Interpolation der Nullstelle zwischen idx und idx+1
    zeros = x[idx] - y[idx] * (x[idx+1] - x[idx]) / (y[idx+1] - y[idx])

    return zeros

f_e = 875
f_d = 900
f_c = 925
f_b = 950
f_a = 975

f0 = 1000  # Hz, erste Frequenz

fa = 1025
fb = 1050
fc = 1075

fd = 1100  # Hz, zweite Frequenz
      
fe = 1125
ff = 1150
fg = 1175
fh = 1200

#fs = 200000     # Samplingfrequenz
T = 10e-3        # Gesamtdauer in Sekunden
t = np.linspace(0, T, 200000)

ref_sig = np.sin(f0 * 2*np.pi * t)

# #ns:
# zerof1 = find_zeros(t, sig1)
# zero1 = zerof1[1]
# print(zero1)

# idx_zero = np.searchsorted(t, zero1)
# t_cut = t[:idx_zero]
# sig1_cut = sig1[:idx_zero]

phi0 = np.pi / 4  # 45°

T1 = ((1/fb)/2)*3/4
t1 = np.linspace(0, T1,2000)
sig1 = np.sin(fb * 2*np.pi * t1 + phi0)


zero1 = t1[-1]
T2 = (1/fc)/2
t2 = np.linspace(zero1, zero1 + T2, 2000)
sig2 = -np.sin(2 * np.pi * fc * (t2 - zero1))

zero2 = t2[-1]
T3 = (1/fd)/2
t3 = np.linspace(zero2, zero2 + T3, 2000)
sig3 = np.sin(2 * np.pi * fd * (t3 - zero2))

zero3 = t3[-1]
T4 = (1/fe)/2
t4 = np.linspace(zero3, zero3 + T4, 2000)
sig4 = -np.sin(2 * np.pi * fe * (t4 - zero3))

zero4 = t4[-1]      
T5 = (1/fd)/2
t5 = np.linspace(zero4, zero4 + T5, 2000)
sig5 = np.sin(2 * np.pi * fd * (t5 - zero4))

zero5 = t5[-1]
T6 = (1/fc)/2
t6 = np.linspace(zero5, zero5 + T6, 2000)
sig6 = -np.sin(2 * np.pi * fc * (t6 - zero5))

zero6 = t6[-1]
T7 = (1/fb)/2
t7 = np.linspace(zero6, zero6 + T7, 2000)
sig7 = np.sin(2 * np.pi * fb * (t7 - zero6))

zero7 = t7[-1]
T8 = (1/fa)/2
t8 = np.linspace(zero7, zero7 + T8, 2000)
sig8 = -np.sin(2 * np.pi * fa * (t8 - zero7))

zero8 = t8[-1]
T9 = (1/f0)/2
t9 = np.linspace(zero8, zero8 + T9, 2000)
sig9 = np.sin(2 * np.pi * f0 * (t9 - zero8))

zero9 = t9[-1]
T10 = (1/f_a)/2
t10 = np.linspace(zero9, zero9 + T10, 2000)
sig10 = -np.sin(2 * np.pi * f_a * (t10 - zero9))

zero10 = t10[-1]
T11 = (1/f_b)/2
t11 = np.linspace(zero10, zero10 + T11, 2000)
sig11 = np.sin(2 * np.pi * f_b * (t11- zero10))

zero11 = t11[-1]
T12 = (1/f_c)/2
t12 = np.linspace(zero11, zero11 + T12, 2000)
sig12 = -np.sin(2 * np.pi * f_c * (t12- zero11))

zero12 = t12[-1]
T13 = (1/f_d)/2
t13 = np.linspace(zero12, zero12 + T13, 2000)
sig13 = np.sin(2 * np.pi * f_d * (t13- zero12))

zero13 = t13[-1]
T14 = (1/f_e)/2
t14 = np.linspace(zero13, zero13 + T14, 2000)
sig14 = -np.sin(2 * np.pi * f_e * (t14- zero13))

zero14 = t14[-1]
T15 = (1/f_d)/2
t15 = np.linspace(zero14, zero14 + T15, 2000)
sig15 = np.sin(2 * np.pi * f_d * (t15- zero14))

zero15 = t15[-1]
T16 = (1/f_c)/2
t16 = np.linspace(zero15, zero15 + T16, 2000)
sig16 = -np.sin(2 * np.pi * f_c * (t16- zero15))

zero16 = t16[-1]
T17 = (1/f_b)/2
t17 = np.linspace(zero16, zero16 + T17, 2000)
sig17 = np.sin(2 * np.pi * f_b * (t17- zero16))

zero17 = t17[-1]
T18 = (1/f_a)/2
t18 = np.linspace(zero17, zero17 + T18, 2000)
sig18 = -np.sin(2 * np.pi * f_a * (t18- zero17))




plt.plot(t * 1000,ref_sig)
plt.plot(t1 * 1000, sig1)
plt.plot(t2 * 1000, sig2)
plt.plot(t3 * 1000, sig3)
plt.plot(t4 * 1000, sig4)
plt.plot(t5 * 1000, sig5)
plt.plot(t6 * 1000, sig6)
plt.plot(t7 * 1000, sig7)
plt.plot(t8 * 1000, sig8)
plt.plot(t9 * 1000, sig9)
plt.plot(t10 * 1000, sig10)
plt.plot(t11 * 1000, sig11)
plt.plot(t12 * 1000, sig12)
plt.plot(t13 * 1000, sig13)
plt.plot(t14 * 1000, sig14)
plt.plot(t15 * 1000, sig15)
plt.plot(t16 * 1000, sig16)
plt.plot(t17 * 1000, sig17)
plt.plot(t18 * 1000, sig18)



plt.grid(True)
plt.tight_layout()
plt.show()

#%%

import numpy as np
import matplotlib.pyplot as plt

f_e = 875
f_d = 900
f_c = 925
f_b = 950
f_a = 975

f0 = 1000  # Hz, erste Frequenz

fa = 1025
fb = 1050
fc = 1075

fd = 1100  # Hz, zweite Frequenz
      
fe = 1125
ff = 1150
fg = 1175
fh = 1200

#fs = 200000     # Samplingfrequenz
T = 7e-3        # Gesamtdauer in Sekunden
t = np.linspace(0, T, 200000)

ref_sig = np.sin(f0 * 2*np.pi * t)



T1 = ((1/fb)/2)/2
t1 = np.linspace(0, T1,2000)
sig1 = np.cos(fb * 2*np.pi * t1)


zero1 = t1[-1]
T2 = (1/fa)/2
t2 = np.linspace(zero1, zero1 + T2, 2000)
sig2 = -np.sin(2 * np.pi * fa * (t2 - zero1))

zero2 = t2[-1]
T3 = (1/f0)/2
t3 = np.linspace(zero2, zero2 + T3, 2000)
sig3 = np.sin(2 * np.pi * f0 * (t3 - zero2))

zero3 = t3[-1]
T4 = (1/f_a)/2
t4 = np.linspace(zero3, zero3 + T4, 2000)
sig4 = -np.sin(2 * np.pi * f_a * (t4 - zero3))

zero4 = t4[-1]      
T5 = (1/f_b)/2
t5 = np.linspace(zero4, zero4 + T5, 2000)
sig5 = np.sin(2 * np.pi * f_b * (t5 - zero4))

zero5 = t5[-1]
T6 = (1/f_a)/2
t6 = np.linspace(zero5, zero5 + T6, 2000)
sig6 = -np.sin(2 * np.pi * f_a * (t6 - zero5))

zero6 = t6[-1]
T7 = (1/f0)/2
t7 = np.linspace(zero6, zero6 + T7, 2000)
sig7 = np.sin(2 * np.pi * f0 * (t7 - zero6))

zero7 = t7[-1]
T8 = (1/fa)/2
t8 = np.linspace(zero7, zero7 + T8, 2000)
sig8 = -np.sin(2 * np.pi * fa * (t8 - zero7))

zero8 = t8[-1]
T9 = (1/fb)/2
t9 = np.linspace(zero8, zero8 + T9, 2000)
sig9 = np.sin(2 * np.pi * fb * (t9 - zero8))

zero9 = t9[-1]
T10 = (1/fa)/2
t10 = np.linspace(zero9, zero9 + T10, 2000)
sig10 = -np.sin(2 * np.pi * fa * (t10 - zero9))

zero10 = t10[-1]
T11 = (1/f0)/2
t11 = np.linspace(zero10, zero10 + T11, 2000)
sig11 = np.sin(2 * np.pi * f0 * (t11- zero10))

zero11 = t11[-1]
T12 = (1/f_a)/2
t12 = np.linspace(zero11, zero11 + T12, 2000)
sig12 = -np.sin(2 * np.pi * f_a * (t12- zero11))

zero12 = t12[-1]
T13 = (1/f_b)/2
t13 = np.linspace(zero12, zero12 + T13, 2000)
sig13 = np.sin(2 * np.pi * f_b * (t13- zero12))

zero13 = t13[-1]
T14 = (1/f_a)/2
t14 = np.linspace(zero13, zero13 + T14, 2000)
sig14 = -np.sin(2 * np.pi * f_a * (t14- zero13))

zero14 = t14[-1]
T15 = (1/f_d)/2
t15 = np.linspace(zero14, zero14 + T15, 2000)
sig15 = np.sin(2 * np.pi * f_d * (t15- zero14))

zero15 = t15[-1]
T16 = (1/f_c)/2
t16 = np.linspace(zero15, zero15 + T16, 2000)
sig16 = -np.sin(2 * np.pi * f_c * (t16- zero15))

zero16 = t16[-1]
T17 = (1/f_b)/2
t17 = np.linspace(zero16, zero16 + T17, 2000)
sig17 = np.sin(2 * np.pi * f_b * (t17- zero16))

zero17 = t17[-1]
T18 = (1/f_a)/2
t18 = np.linspace(zero17, zero17 + T18, 2000)
sig18 = -np.sin(2 * np.pi * f_a * (t18- zero17))



plt.figure(figsize=(10,4), dpi = 100)
plt.plot(t * 1000,ref_sig, color = my_blue)
plt.plot(t1 * 1000, sig1, color = my_orange)
plt.plot(t2 * 1000, sig2, color = my_red, label='Freq. decreases')
plt.plot(t3 * 1000, sig3, color = my_blue2, label = 'f = 1000 Hz')
plt.plot(t4 * 1000, sig4, color = my_red)
plt.plot(t5 * 1000, sig5, color = my_red)
plt.plot(t6 * 1000, sig6, color = my_green, label='Freq. increases')
plt.plot(t7 * 1000, sig7, color = my_blue2)
plt.plot(t8 * 1000, sig8, color = my_green)
plt.plot(t9 * 1000, sig9, color = my_green)
plt.plot(t10 * 1000, sig10, color = my_red)
plt.plot(t11 * 1000, sig11, color = my_blue2)
plt.plot(t12 * 1000, sig12, color = my_red)
plt.plot(t13 * 1000, sig13, color = my_red)
plt.plot(t14 * 1000, sig14, color = my_green)
# plt.plot(t15 * 1000, sig15)
# plt.plot(t16 * 1000, sig16)
# plt.plot(t17 * 1000, sig17)
# plt.plot(t18 * 1000, sig18)


plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


#%%








