# -*- coding: utf-8 -*-
"""
Created on Tue May 13 10:14:06 2025

@author: nilsr
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, freqz

# Butterworth-Filter 4. Ordnung, 0.4 * Nyquist-Frequenz
b, a = butter(4, 0.4)

# Frequenzgang plotten
w, h = freqz(b, a)
plt.plot(w / np.pi, 20 * np.log10(abs(h)))
plt.title('Frequenzgang des Butterworth-Filters')
plt.xlabel('Frequenz (relativ zur Nyquist-Frequenz)')
plt.ylabel('Amplitude [dB]')
plt.grid(True)
plt.show()
