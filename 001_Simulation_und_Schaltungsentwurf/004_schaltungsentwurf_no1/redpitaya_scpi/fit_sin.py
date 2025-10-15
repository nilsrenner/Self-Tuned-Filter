#!/usr/bin/env python3

"""
https://stackoverflow.com/questions/16716302/how-do-i-fit-a-sine-curve-to-my-data-with-pylab-and-numpy
"""

import numpy as np
import scipy.optimize as opt


# %% Sinosoidal fitting function
def fit_sin(t, y):
    ff = np.fft.fftfreq(len(t), (t[1] - t[0]))  # assume uniform spacing
    Fyy = abs(np.fft.fft(y))
    guess_freq = abs(ff[np.argmax(Fyy[1:]) + 1])  # excluding the zero frequency "peak"
    guess_amp = np.std(y) * 2.**0.5
    guess_offset = np.mean(y)
    guess = np.array([guess_amp, 2. * np.pi * guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):
        return A * np.sin(w * t + p) + c

    popt, pcov = opt.curve_fit(sinfunc, t, y, p0=guess)
    A, w, p, c = popt
    f = w / (2 * np.pi)

    return np.array([A, p, f, w])