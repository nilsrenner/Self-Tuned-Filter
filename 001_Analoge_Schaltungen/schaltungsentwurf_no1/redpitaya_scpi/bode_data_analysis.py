#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data analysis for Bode plots
Input signal: DF_IN1
Output signal: DF_IN2

@author: Mirco Meiners (HSB)
"""

import numpy as np
import scipy.signal as sig
import pandas as pd
import matplotlib.pyplot as plt

# %% Array of tones (GEN):
# Parameters
func = 'SINE'
ampl = 0.2
offset = 0.0
freqs = np.arange(10, 1000, 10)

w = 2 * np.pi * freqs
N = 16384  # length of data array, STEMlab buffer size
t = np.linspace(0, 8.389e-3, N)
ts = 8.389e-3 / N  # sampling time

# %% Data storage and read
Data_IN1 = 'data/IN1_INT_IN'  # + str(datetime.now().strftime('%Y-%m-%d_%H_%M'))
Data_IN2 = 'data/IN2_INT_OUT'  # + str(datetime.now().strftime('%Y-%m-%d_%H_%M'))
# Data_IN = 'data/IN_UB_VBS_VBP'  # + str(datetime.now().strftime('%Y-%m-%d_%H_%M'))

# DF_IN1 = pd.read_csv(Data_IN1 + '.csv')
# DF_IN2 = pd.read_csv(Data_IN2 + '.csv')

DF_IN1 = pd.read_parquet(Data_IN1 + '.parquet')
DF_IN2 = pd.read_parquet(Data_IN2 + '.parquet')

# %% Fitting and extraction of sine params
# SigParam_IN1 = pd.DataFrame()
# SigParam_IN2 = pd.DataFrame()

# for freq in freqs:
#     SigParam_IN1[str(freq)] = fit_sin(t, DF_IN1[str(freq)].values)
#     SigParam_IN2[str(freq)] = fit_sin(t, DF_IN2[str(freq)].values)

# %% Test fitting for f = 800 Hz
# plt.plot(t, ampl * np.sin(2 * np.pi * 800 * t) + offset, label='OUT1')
# plt.plot(t,
#          SigParam_IN1.iloc[0, 0] *
#          np.sin(SigParam_IN1.iloc[3, 0] * t + SigParam_IN1.iloc[1, 0]),
#          label='IN1')
# plt.plot(t,
#          SigParam_IN2.iloc[0, 0] *
#          np.sin(SigParam_IN2.iloc[3, 0] * t + SigParam_IN2.iloc[1, 0]),
#          label='IN2')
# plt.legend()

# %% Magnitude in dB
# MAG_dB_IN1_fit = 20 * np.log10(np.abs(SigParam_IN2.iloc[0] / ampl))
# MAG_dB_IN2_fit = 20 * np.log10(np.abs(SigParam_IN2.iloc[0] / ampl))
# MAG_dB_fit = 20 * np.log10(np.abs(SigParam_IN2.iloc[0] / SigParam_IN1.iloc[0]))

# %% Magnitudes (rms) via std on DataFrame
# MAG_dB_IN1 = 20 * np.log10(np.abs(DF_IN1.std() / ampl))
# MAG_dB_IN2 = 20 * np.log10(np.abs(DF_IN2.std() / ampl))
MAG_dB = 20 * np.log10(np.abs(DF_IN2.std() / DF_IN1.std()))

# %% Phase difference
# Ref.:
# https://stackoverflow.com/questions/27545171/identifying-phase-shift-between-signals
# y1 = ampl * np.sin(w[0] * t)
# dt = 0.2e-3
# y2 = ampl * np.sin(w[0] * t - w[0] * dt)

# %% Cross-correlation
# corr = sig.correlate(y1, y2)
# lags = sig.correlation_lags(len(y1), len(y2))
# phase_rad_xcorr = lags[np.argmax(corr)] * ts * w[0]
# phase_deg_xcorr = np.rad2deg(phase_rad_xcorr)

# %% Cross-correlation with dataframes and synthesized input signal
# phase_IN1 = np.ndarray(len(freqs))
# phase_IN2 = np.ndarray(len(freqs))

# for n in range(0, len(freqs)):
#     vin = ampl * np.sin(2 * np.pi * freqs[n] * t)
#     corr1 = sig.correlate(vin, DF_IN1[str(freqs[n])].values)
#     corr2 = sig.correlate(vin, DF_IN2[str(freqs[n])].values)
#     lags1 = sig.correlation_lags(len(vin), len(DF_IN1[str(freqs[n])]))
#     lags2 = sig.correlation_lags(len(vin), len(DF_IN2[str(freqs[n])]))
#     phase_rad_xcorr1 = 2 * np.pi * freqs[n] * lags1[np.argmax(corr1)] * ts
#     phase_rad_xcorr2 = 2 * np.pi * freqs[n] * lags2[np.argmax(corr2)] * ts
#     phase_IN1[n] = np.rad2deg(phase_rad_xcorr1)
#     phase_IN2[n] = np.rad2deg(phase_rad_xcorr2)

# %% Cross-correlation with dataframes and measured input signal as DF_IN1
PHASE_xcorr = pd.Series()

for freq in freqs:
    corr = sig.correlate(DF_IN1[str(freq)].values, DF_IN2[str(freq)])
    lags = sig.correlation_lags(len(DF_IN1[str(freq)]), len(DF_IN2[str(freq)]))
    phase_rad_xcorr = 2 * np.pi * freq * lags[np.argmax(corr)] * ts
    PHASE_xcorr[str(freq)] = np.rad2deg(phase_rad_xcorr)

# %% Frequency domain
# y1_fft = np.fft.fft(y1)
# y2_fft = np.fft.fft(y2)

# y1_fft_2 = y1_fft[0:N // 2]
# y2_fft_2 = y2_fft[0:N // 2]

# phase_rad_fft = np.angle(y1_fft[0:N // 2] / y2_fft[0:N // 2])
# c = np.inner(y2_fft_2, np.conj(y1_fft_2)) / np.sqrt(
#    np.inner(y1_fft_2, np.conj(y1_fft_2)) *
#    np.inner(y2_fft_2, np.conj(y2_fft_2)))

# phase_rad_fft = np.max(np.angle(c))
# phase_deg_fft = np.max(np.angle(c, deg=True))

# %% Hilbert transform
# y1_h = sig.hilbert(y1)
# y2_h = sig.hilbert(y2)

# phase_rad_h = np.angle(y2_h/y1_h)
# phase_rad_h = np.angle(np.linalg.lstsq(y2_h.T, y1_h.T))[0]
# phase_rad_h = np.angle(np.dot(y1_h, np.linalg.pinv(y2_h)))
# c = np.inner(y2_h, np.conj(y1_h)) / np.sqrt(
#     np.inner(y1_h, np.conj(y1_h)) * np.inner(y2_h, np.conj(y2_h)))
# phase_rad_h = np.angle(c)
# phase_deg_h = np.angle(c, deg=True)

# %% Plots
plt.figure()
plt.subplot(2, 1, 1)
plt.title('Bode Plot')
plt.semilogx(freqs, MAG_dB)
plt.grid()
plt.ylabel('Magnitude in dB')
#
plt.subplot(2, 1, 2)
plt.semilogx(freqs, PHASE_xcorr)
plt.grid()
plt.xlabel('f in Hz')
plt.ylabel('Phase in deg')
