#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  6 08:41:03 2025

@author: daniel
"""

# %% Init
import time
import sys
import os

sys.path.append(os.path.dirname(__file__)+'\\redpitaya_scpi')

import redpitaya_scpi as scpi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

# %% 
print("Um den Redpitaya verwenden zu können muss die VPN verwendet werden")
workplace = input("Arbeitsplatz:")

if workplace == "1":
    IP = "192.168.111.181"
elif workplace == "2":
    IP = "192.168.111.182"
elif workplace == "3":
    IP = "192.168.111.183"
elif workplace == "4":
    IP = "192.168.111.183"
else:
    print("This workplace does not excist")

print("Connecting to",IP)
red_ip = scpi.scpi(IP)

DF_IN1 = pd.DataFrame()
DF_IN2 = pd.DataFrame()

# Parameters
func = 'SINE'
ampl = 0.2
offset = 0.0
freqs = np.arange(10, 1000, 10)
print("Parameters:\n","Waveform:",func,"\n","Amplitude:",ampl,"[v]\n","Offset:",offset,"[V]\n","Frequency range:",min(freqs),"to",max(freqs))

for freq in freqs:

    red_ip.tx_txt('GEN:RST')  # Signal Generator reset
    red_ip.tx_txt('SOUR1:FUNC ' + str(func).upper())  # Wave form
    red_ip.tx_txt('SOUR1:VOLT ' + str(ampl))  # Magnitude
    red_ip.tx_txt('SOUR1:VOLT:OFFS ' + str(offset))  # Offset
    red_ip.tx_txt('SOUR1:FREQ:FIX ' + str(freq))  # Frequency
    red_ip.tx_txt('OUTPUT1:STATE ON')  # Output
    red_ip.tx_txt('SOUR1:TRig:INT')
    time.sleep(1)

    # Trigger
    red_ip.tx_txt('ACQ:RST')  # Input reset
    red_ip.tx_txt('ACQ:DEC 64')  # Decimation
    red_ip.tx_txt('ACQ:TRIG:LEV 0.5')  # Trigger level
    red_ip.tx_txt('ACQ:TRIG:DLY 8192')  # Delay
    red_ip.tx_txt('ACQ:START')  # Start measurement
    red_ip.tx_txt('ACQ:TRIG NOW')

    # Input IN1
    time.sleep(0.1)  # in seconds
    red_ip.tx_txt('ACQ:SOUR1:DATA?')  # Readout buffer IN1
    IN1str = red_ip.rx_txt()
    IN1str = IN1str.strip('{}\n\r').replace("  ", "").split(',')
    IN1 = np.array(list(map(float, IN1str)))
    DF_IN1[str(freq)] = IN1

    # Input IN2
    time.sleep(0.1)  # in seconds
    red_ip.tx_txt('ACQ:SOUR2:DATA?')  # Readout buffer IN2
    IN2str = red_ip.rx_txt()
    IN2str = IN2str.strip('{}\n\r').replace("  ", "").split(',')
    IN2 = np.array(list(map(float, IN2str)))
    DF_IN2[str(freq)] = IN2

    red_ip.tx_txt('OUTPUT2:STATE OFF')



Data_IN1 = 'daten/IN1_INT_IN'  # + str(datetime.now().strftime('%Y-%m-%d_%H_%M'))
Data_IN2 = 'daten/IN2_INT_OUT'  #+ str(datetime.now().strftime('%Y-%m-%d_%H_%M'))

DF_IN1.to_csv(Data_IN1 + '.csv', index=False)
DF_IN2.to_csv(Data_IN2 + '.csv', index=False)

DF_IN1.to_parquet(Data_IN1 + ".parquet", index=False)
DF_IN2.to_parquet(Data_IN2 + ".parquet", index=False)
print("Messwerte sind im Ordner Daten als .csv zu finden")

#Datenauswertung

w = 2 * np.pi * freqs
N = 16384  # length of data array, STEMlab buffer size
t = np.linspace(0, 8.389e-3, N)
ts = 8.389e-3 / N  # sampling time

MAG_dB = 20 * np.log10(np.abs(DF_IN2.std() / DF_IN1.std()))
PHASE_xcorr = pd.Series()

for freq in freqs:
    corr = sig.correlate(DF_IN1[str(freq)].values, DF_IN2[str(freq)])
    lags = sig.correlation_lags(len(DF_IN1[str(freq)]), len(DF_IN2[str(freq)]))
    phase_rad_xcorr = 2 * np.pi * freq * lags[np.argmax(corr)] * ts
    PHASE_xcorr[str(freq)] = np.rad2deg(phase_rad_xcorr)
    
#Plot
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
