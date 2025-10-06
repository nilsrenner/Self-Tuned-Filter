# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 13:09:59 2025

@author: nilsr
"""

import numpy as np
import matplotlib.pyplot as plt


C = 0.0002 #22*10^(-6)
L = 0.056 #56 *10^(-3)
R = 100
Schaltung = input('welcher Schaltungstyp:')


f1 = 0      # 10^1 = 10 Hz
f2 = 5      # 10^5 = 100 kHz umschreiben dass der das selber erkennt
N = 500      #Anzahl werte
#f = np.arange(f1,f2,N)
f = np.logspace(f1,f2,N)
w = 2 * np.pi * f


# Impedanzen (komplex!)
Zc = 1 / (1j * w * C)
Zl = 1j * w * L
Zr = R * np.ones_like(w)

if Schaltung == "RCLP":
    print("Schaltung ist RCLP")
    U_in = (Zr + Zc)
    U_out = Zc
elif Schaltung == 'CRHP':
    print("Schaltung ist CRHP")
    U_in = (Zc + Zr)
    U_out = (Zr)
elif Schaltung == 'RLHP':
    print("Schaltung ist RLHP")
    U_in = (Zr + Zl)
    U_out = Zl
elif Schaltung == 'LRLP':
    print("Schaltung ist LRLP")
    U_in = (Zl + Zr)
    U_out = Zr
elif Schaltung == 'LCBP':
    print("Schaltung ist LCBP")
    U_in = (Zl + Zc)
    U_out = Zc
elif Schaltung == 'CLBP':
    print("Schaltung ist CLBP")
    U_in = (Zc + Zl)
    U_out = Zl
    
else:
    print("keine Schaltung erkannt")





H = U_out/U_in

U = H * 1


plt.figure(1)
plt.semilogx(f, np.abs(U), label='|H(f)|')
plt.title('Übertragungsfunktion H(f)')
plt.xlabel('Frequenz [Hz]')
plt.ylabel('Betrag $|U_H|$ [V]')
plt.grid()
plt.legend()


