# -*- coding: utf-8 -*-
"""
Created on Tue May  6 09:53:31 2025

@author: nilsr
"""

#%% Initialisierung


from ltspice import Ltspice  # <-- das ist die richtige Klasse
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import redpitaya_scpi as scpi
import scipy.signal as sig

import datetime
import time
import sys
import os

#%% Import von KiCad

filepath = r'C:\Users\nilsr\OneDrive\Desktop\Nils\001_Studium\006_Semester6\001_Analoge_Schaltungen\schaltungsentwurf_no1\schaltungsentwurf_no1.raw'
l = Ltspice(filepath)  # jetzt funktioniert der Konstruktor
l.parse()
#print(l.variables)  # statt get_trace_names()

sim_freq = l.get_frequency()
LPF = l.get_data('v(/lpf)')
HPF = l.get_data('v(/hpf)')
BPF = l.get_data('v(/bpf)')
BSF = l.get_data('v(/bsf)')


# Magnitude
real_LPF_dB = 20 * np.log10(abs(LPF) + 1e-12)
real_HPF_dB = 20 * np.log10(abs(HPF) + 1e-12)
real_BPF_dB = 20 * np.log10(abs(BPF) + 1e-12)
real_BSF_dB = 20 * np.log10(abs(BSF) + 1e-12)

# Phase
phase_lp = np.degrees(np.unwrap(np.angle(LPF)))
phase_hp = np.degrees(np.unwrap(np.angle(HPF)))
phase_bp = np.degrees(np.unwrap(np.angle(BPF)))
phase_bs = np.degrees(np.unwrap(np.angle(BSF)))


ftype = input('Art des Filtertyps (HP,LP,BP,BS):')

if ftype == 'HP':
    sim_ampl = real_HPF_dB
    sim_phase = phase_hp
elif ftype == 'LP':
    sim_ampl = real_LPF_dB
    sim_phase = phase_lp
elif ftype == 'BP':
    sim_ampl = real_BPF_dB
    sim_phase = phase_bp
elif ftype == 'BS':
    sim_ampl = real_BSF_dB
    sim_phase = phase_bs
else:
    print('This Filtertyp does not exist')
    
#%% Import vom redpitaya

print("Um den Redpitaya verwenden zu können muss die VPN verwendet werden")
workplace = input("Arbeitsplatz:")

if workplace == "1":
    IP = "192.168.111.181"
elif workplace == "2":
    IP = "192.168.111.182"
elif workplace == "3":
    IP = "192.168.111.183"
elif workplace == "6":
    IP = "192.168.111.186"
else:
    print("This workplace does not excist")

print("Connecting to",IP)
red_ip = scpi.scpi(IP)

DF_IN1 = pd.DataFrame()
DF_IN2 = pd.DataFrame()

# Parameters
func = 'SQUARE'
ampl = 0.2
offset = 0.0
freqs = np.linspace(50, 1000, 100)
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
    
    min_periods = 5
    wait_time = max(0.1, min_periods/freq)
    #time.sleep(wait_time)

    # Input IN1
    time.sleep(wait_time)  # in seconds
    red_ip.tx_txt('ACQ:SOUR1:DATA?')  # Readout buffer IN1
    IN1str = red_ip.rx_txt()
    IN1str = IN1str.strip('{}\n\r').replace("  ", "").split(',')
    IN1 = np.array(list(map(float, IN1str)))
    DF_IN1[str(freq)] = IN1

    # Input IN2
    time.sleep(wait_time)  # in seconds
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

PHASE_xcorr = np.empty((len(freqs)),dtype=float)

for i, freq in enumerate(freqs):
    corr = sig.correlate(DF_IN1[str(freq)].values, DF_IN2[str(freq)],method='fft')
    lags = sig.correlation_lags(len(DF_IN1[str(freq)]), len(DF_IN2[str(freq)]))
    phase_rad_xcorr = 2 * np.pi * freq * lags[np.argmax(corr)] * ts
    PHASE_xcorr[i] = phase_rad_xcorr
PHASE_deg = np.rad2deg(np.unwrap(PHASE_xcorr))
 

#%% Datenspeicherung

date_str = datetime.datetime.now().strftime("%Y-%m-%d")
Q = 1
H0 = 1
#funk = 'sqare'

filename_mag = fr'C:\Users\nilsr\OneDrive\Desktop\Nils\001_Studium\006_Semester6\001_Analoge_Schaltungen\Messwerte\{date_str}_Mag_dB_{ftype}_Q{Q}_H0{H0}.csv'
filename_phase = fr'C:\Users\nilsr\OneDrive\Desktop\Nils\001_Studium\006_Semester6\001_Analoge_Schaltungen\Messwerte\{date_str}_PHASE_{ftype}_Q{Q}_H0{H0}.csv'


np.savetxt(filename_mag, MAG_dB)
np.savetxt(filename_phase,PHASE_xcorr)


#%% Plot

plt.close('all')

plt.figure(1,figsize = (12,9))
plt.semilogx(sim_freq, real_LPF_dB,label = 'Lowpass')
plt.semilogx(sim_freq, real_HPF_dB,label = 'Highpass')
plt.semilogx(sim_freq, real_BPF_dB,label = 'Bandpass')
plt.semilogx(sim_freq, real_BSF_dB,label = 'Bandstop')
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude")
plt.title('Filtertypen Simulation')
plt.legend()
plt.grid()
plt.show()



plt.figure(2)
plt.subplot(2, 1, 1)
plt.semilogx(freqs, MAG_dB, label = 'Messung')
plt.semilogx(sim_freq, sim_ampl, label ='Simulation')
plt.title('Bode Plot: Magnitude')
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude in dB")
plt.legend()
plt.grid()

plt.subplots_adjust(hspace=0.6)


plt.subplot(2, 1, 2)
plt.semilogx(freqs, PHASE_deg, label='Messung')
plt.semilogx(sim_freq, sim_phase, label='Simulation')
plt.title('Bode Plot: Phase')
plt.xlabel('f in Hz')
plt.ylabel('Phase in deg')
plt.legend()
plt.grid()

