# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 08:39:14 2025

@author: nilsr
"""
#%% Initialisierung


from ltspice import Ltspice  # <-- das ist die richtige Klasse
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import redpitaya_scpi as scpi
import scipy.signal as sig

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

#%%

filepath = r'C:\Users\nilsr\OneDrive\Desktop\Nils\001_Studium\006_Semester6\001_Analoge_Schaltungen\Messung'

# Check if files exist
if os.path.exists(os.path.join(filepath, 'mag_dB.npy')) and os.path.exists(os.path.join(filepath, 'PHASE_xcorr.npy')):
    MAG_dB = np.load(os.path.join(filepath, 'mag_dB.npy'))
    PHASE_xcorr = np.load(os.path.join(filepath, 'PHASE_xcorr.npy'))
else:
    print("Files not found. Please check file names and directory.")

red_data = np.loadtxt(os.path.join(filepath,'red_data.csv'), delimiter=',',skiprows=1)

red_freq = red_data[:,0]
red_amp = red_data[:,1]
red_phase = red_data[:,2]

#%% Plot

#plt.close('all')

plt.figure(1)
plt.subplot(2, 1, 1)
plt.semilogx(sim_freq, sim_ampl, label ='Simulation')
plt.semilogx(np.linspace(50, 1000, 100), MAG_dB, label = 'python')
plt.semilogx(red_freq, red_amp, label ='Redpitaya')
plt.title('Bode Plot: Magnitude')
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude in dB")
plt.legend()
plt.grid()

plt.subplots_adjust(hspace=0.6)


plt.subplot(2, 1, 2)
plt.semilogx(sim_freq, sim_phase, label='Simulation')
plt.semilogx(np.linspace(50, 1000, 100), PHASE_xcorr, label='python')
plt.semilogx(red_freq, red_phase, label='Redpitaya')
plt.title('Bode Plot: Phase')
plt.xlabel('f in Hz')
plt.ylabel('Phase in deg')
plt.legend()
plt.grid()


