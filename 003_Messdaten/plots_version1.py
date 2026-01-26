#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 13:56:36 2026

@author: nils
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

#%% HSB Farben

my_blue = (10/255,85/255,140/255)      #x/255 da HTMP bis 255 sene Farbscala hat und Matplotlib bis 1
my_red = (195/255, 5/255, 35/255)
my_green = (0/255, 145/255, 90/255)
my_yellow = (250/255, 190/255, 0/255)
my_orange = (240/255, 120/255, 35/255)
my_purple = (120/255, 100/255, 165/255)
my_green2 = (110/255, 165/255, 60/255)
my_blue2 = (50/255, 180/255, 200/255)

#%% Biquad alt

folder_path = '001_Biquad'

file_BP = os.path.join(folder_path, 'BP_redp_alt.csv')
file_BS = os.path.join(folder_path, 'BS_redp_alt.csv')
file_TP = os.path.join(folder_path, 'TP_redp_alt.csv')
file_HP = os.path.join(folder_path, 'HP_redp_alt.csv')

df_BP = pd.read_csv(file_BP)
df_BS = pd.read_csv(file_BS)
df_TP = pd.read_csv(file_TP)
df_HP = pd.read_csv(file_HP)

# Spaltennamen bereinigen
for df in [df_BP, df_BS, df_TP, df_HP]:
    df.columns = df.columns.str.strip()

# Amplituden- und Phasendaten extrahieren
amplitude_BP = df_BP.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_BP = df_BP.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_BS = df_BS.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_BS = df_BS.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_TP = df_TP.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_TP = df_TP.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_HP = df_HP.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_HP = df_HP.set_index('Frequency [Hz]')['Phase [deg]']

# Plot erstellen
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.semilogx(amplitude_BP.index, amplitude_BP, label='BP_redp_neu')
ax1.semilogx(amplitude_BS.index, amplitude_BS, label='BS_redp_neu')
ax1.semilogx(amplitude_TP.index, amplitude_TP, label='TP_redp_neu')
ax1.semilogx(amplitude_HP.index, amplitude_HP, label='HP_redp_neu')
ax1.set_title('Amplitudengänge')
ax1.set_xlabel('Frequenz [Hz]')
ax1.set_ylabel('Amplitude [dB]')
ax1.legend(loc='lower left')
ax1.grid(True)

ax2.semilogx(phase_BP.index, phase_BP, label='BP_redp_neu')
ax2.semilogx(phase_BS.index, phase_BS, label='BS_redp_neu')
ax2.semilogx(phase_TP.index, phase_TP, label='TP_redp_neu')
ax2.semilogx(phase_HP.index, phase_HP, label='HP_redp_neu')
ax2.set_title('Phasengänge')
ax2.set_xlabel('Frequenz [Hz]')
ax2.set_ylabel('Phase [°]')
ax2.legend(loc='lower left')
ax2.grid(True)

plt.tight_layout()
plt.show()



#%% Biquad neu

folder_path = '001_Biquad'

file_BP = os.path.join(folder_path, 'BP_redp_neu.csv')
file_BS = os.path.join(folder_path, 'BS_redp_neu.csv')
file_TP = os.path.join(folder_path, 'TP_redp_neu.csv')
file_HP = os.path.join(folder_path, 'HP_redp_neu.csv')

df_BP = pd.read_csv(file_BP)
df_BS = pd.read_csv(file_BS)
df_TP = pd.read_csv(file_TP)
df_HP = pd.read_csv(file_HP)

# Spaltennamen bereinigen
for df in [df_BP, df_BS, df_TP, df_HP]:
    df.columns = df.columns.str.strip()

# Amplituden- und Phasendaten extrahieren
amplitude_BP = df_BP.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_BP = df_BP.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_BS = df_BS.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_BS = df_BS.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_TP = df_TP.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_TP = df_TP.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_HP = df_HP.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_HP = df_HP.set_index('Frequency [Hz]')['Phase [deg]']

# Plot erstellen
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.semilogx(amplitude_BP.index, amplitude_BP, label='BP_redp_neu')
ax1.semilogx(amplitude_BS.index, amplitude_BS, label='BS_redp_neu')
ax1.semilogx(amplitude_TP.index, amplitude_TP, label='TP_redp_neu')
ax1.semilogx(amplitude_HP.index, amplitude_HP, label='HP_redp_neu')
ax1.set_title('Amplitudengänge')
ax1.set_xlabel('Frequenz [Hz]')
ax1.set_ylabel('Amplitude [dB]')
ax1.legend(loc='lower left')
ax1.grid(True)

ax2.semilogx(phase_BP.index, phase_BP, label='BP_redp_neu')
ax2.semilogx(phase_BS.index, phase_BS, label='BS_redp_neu')
ax2.semilogx(phase_TP.index, phase_TP, label='TP_redp_neu')
ax2.semilogx(phase_HP.index, phase_HP, label='HP_redp_neu')
ax2.set_title('Phasengänge')
ax2.set_xlabel('Frequenz [Hz]')
ax2.set_ylabel('Phase [°]')
ax2.legend(loc='lower left')
ax2.grid(True)

plt.tight_layout()
plt.show()

#%% VCF ohne PD

folder_path = '003_VCF_ohne_PD'

file_BP = os.path.join(folder_path, 'BP_redp_23.01.csv')
file_BS = os.path.join(folder_path, 'BS_redp_23.01.csv')
file_TP = os.path.join(folder_path, 'TP_redp_23.01.csv')
file_HP = os.path.join(folder_path, 'HP_redp_23.01.csv')

df_BP = pd.read_csv(file_BP)
df_BS = pd.read_csv(file_BS)
df_TP = pd.read_csv(file_TP)
df_HP = pd.read_csv(file_HP)

# Spaltennamen bereinigen
for df in [df_BP, df_BS, df_TP, df_HP]:
    df.columns = df.columns.str.strip()

# Amplituden- und Phasendaten extrahieren
amplitude_BP = df_BP.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_BP = df_BP.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_BS = df_BS.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_BS = df_BS.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_TP = df_TP.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_TP = df_TP.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_HP = df_HP.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_HP = df_HP.set_index('Frequency [Hz]')['Phase [deg]']

# Plot erstellen
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.semilogx(amplitude_BP.index, amplitude_BP, label='BP_redp_neu')
ax1.semilogx(amplitude_BS.index, amplitude_BS, label='BS_redp_neu')
ax1.semilogx(amplitude_TP.index, amplitude_TP, label='TP_redp_neu')
ax1.semilogx(amplitude_HP.index, amplitude_HP, label='HP_redp_neu')
ax1.set_title('Amplitudengänge')
ax1.set_xlabel('Frequenz [Hz]')
ax1.set_ylabel('Amplitude [dB]')
ax1.legend(loc='lower left')
ax1.grid(True)

ax2.semilogx(phase_BP.index, phase_BP, label='BP_redp_neu')
ax2.semilogx(phase_BS.index, phase_BS, label='BS_redp_neu')
ax2.semilogx(phase_TP.index, phase_TP, label='TP_redp_neu')
ax2.semilogx(phase_HP.index, phase_HP, label='HP_redp_neu')
ax2.set_title('Phasengänge')
ax2.set_xlabel('Frequenz [Hz]')
ax2.set_ylabel('Phase [°]')
ax2.legend(loc='lower left')
ax2.grid(True)

plt.tight_layout()
plt.show()

#%% Grenzfrequenzbestimmung des VCF ohne PD



folder_path = '003_VCF_ohne_PD'
file_R159 = os.path.join(folder_path, 'BS_R159.csv')
file_R212 = os.path.join(folder_path, 'BS_R212.csv')
file_R318 = os.path.join(folder_path, 'BS_R318.csv')
file_R531 = os.path.join(folder_path, 'BS_R531.csv')
file_R796 = os.path.join(folder_path, 'BS_R795.csv')
file_R994 = os.path.join(folder_path, 'BS_R994.csv')
file_R1591 = os.path.join(folder_path, 'BS_R1591.csv')


df_R159 = pd.read_csv(file_R159)
df_R212 = pd.read_csv(file_R212)
df_R318 = pd.read_csv(file_R318)
df_R531 = pd.read_csv(file_R531)
df_R796 = pd.read_csv(file_R796)
df_R994 = pd.read_csv(file_R994)
df_R1591 = pd.read_csv(file_R1591)

# Spaltennamen bereinigen
for df in [df_R159, df_R212, df_R318, df_R531, df_R796, df_R994, df_R1591]:
    df.columns = df.columns.str.strip()
    

# Amplituden- und Phasendaten extrahieren
amplitude_R159 = df_R159.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R159 = df_R159.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R212 = df_R212.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R212 = df_R212.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R318 = df_R318.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R318 = df_R318.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R531 = df_R531.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R531 = df_R531.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R796 = df_R796.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R796 = df_R796.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R994 = df_R994.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R994 = df_R994.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R1591 = df_R1591.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R1591 = df_R1591.set_index('Frequency [Hz]')['Phase [deg]']

# Plot erstellen
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.semilogx(amplitude_R159.index, amplitude_R159, label='BS_R159')
ax1.semilogx(amplitude_R212.index, amplitude_R212, label='BS_R212')
ax1.semilogx(amplitude_R318.index, amplitude_R318, label='BS_R318')
ax1.semilogx(amplitude_R531.index, amplitude_R531, label='BS_R531')
ax1.semilogx(amplitude_R796.index, amplitude_R796, label='BS_R796')
ax1.semilogx(amplitude_R994.index, amplitude_R994, label='BS_R994')
ax1.semilogx(amplitude_R1591.index, amplitude_R1591, label='BS_R1591')
ax1.set_title('Amplitudengänge')
ax1.set_xlabel('Frequenz [Hz]')
ax1.set_ylabel('Amplitude [dB]')
ax1.legend(loc='lower left')  # Legende unten links
ax1.grid(True)

ax2.semilogx(phase_R159.index, phase_R159, label='BS_R159')
ax2.semilogx(phase_R212.index, phase_R212, label='BS_R212')
ax2.semilogx(phase_R318.index, phase_R318, label='BS_R318')
ax2.semilogx(phase_R531.index, phase_R531, label='BS_R531')
ax2.semilogx(phase_R796.index, phase_R796, label='BS_R796')
ax2.semilogx(phase_R994.index, phase_R994, label='BS_R994')
ax2.semilogx(phase_R1591.index, phase_R1591, label='BS_R1591')
ax2.set_title('Phasengänge')
ax2.set_xlabel('Frequenz [Hz]')
ax2.set_ylabel('Phase [°]')
ax2.legend(loc='lower left')  # Legende unten links
ax2.grid(True)

plt.tight_layout()
plt.show()


   


#eigene berechung von w0 
    
def find_center_frequency_by_phase(df):
    phase = df['Phase [deg]'].values
    frequency = df['Frequency [Hz]'].values

    for i in range(len(phase) - 1):
        if phase[i] * phase[i + 1] < 0:  # detektion des vorzeidchenwechsels
            x1, x2 = frequency[i], frequency[i + 1]
            y1, y2 = phase[i], phase[i + 1]
            x = x1 - y1 * (x2 - x1) / (y2 - y1) #interpolierte frequenz
            return x
    return None


center_freq_R159 = find_center_frequency_by_phase(df_R159)
center_freq_R212 = find_center_frequency_by_phase(df_R212)
center_freq_R318 = find_center_frequency_by_phase(df_R318)
center_freq_R531 = find_center_frequency_by_phase(df_R531)
center_freq_R796 = find_center_frequency_by_phase(df_R796)
center_freq_R994 = find_center_frequency_by_phase(df_R994)
center_freq_R1591 = find_center_frequency_by_phase(df_R1591)


def freq_0(Res):
    cap = 1e-6 #* 0.907
    V_r = 9.73  #10.73 funktioniert von der Abweichung her sehr gut, selbiges mit Ref*x
    V_c = 1     # Ergebnis ist \pm7.5 % abweichung
    freq_0 = round(V_r / (2 * np.pi * V_c * cap * Res),2)
    return freq_0

def abweichung(df, Res):
    abw = round((1 - freq_0(Res)/find_center_frequency_by_phase(df)) * 100,2)
    return abw
    


print(f"Mittenfrequenz BS_R1591: {center_freq_R1591:.2f} Hz")
print("Theoriewert:             ", freq_0(1591),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R1591, 1591))

print(f"Mittenfrequenz BS_R994:  {center_freq_R994:.2f} Hz")
print("Theoriewert:            ", freq_0(994),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R994, 994))

print(f"Mittenfrequenz BS_R796:  {center_freq_R796:.2f} Hz")
print("Theoriewert:            ", freq_0(796),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R796, 796))

print(f"Mittenfrequenz BS_R531:  {center_freq_R531:.2f} Hz")
print("Theoriewert:            ", freq_0(531),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R531, 531))

print(f"Mittenfrequenz BS_R318:  {center_freq_R318:.2f} Hz")
print("Theoriewert:            ", freq_0(318),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R318, 318))

print(f"Mittenfrequenz BS_R212:  {center_freq_R212:.2f} Hz")
print("Theoriewert:            ", freq_0(212),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R212, 212))

print(f"Mittenfrequenz BS_R159:  {center_freq_R159:.2f} Hz")
print("Theoriewert:            ", freq_0(159),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R159, 159))


#%%#%% Grenzfrequenzbestimmung des VCF ohne PD mit neuen Cs



folder_path = '003_VCF_ohne_PD'
file_R159 = os.path.join(folder_path, 'BS_R159_cneu.csv')
file_R212 = os.path.join(folder_path, 'BS_R212_cneu.csv')
file_R318 = os.path.join(folder_path, 'BS_R318_cneu.csv')
file_R531 = os.path.join(folder_path, 'BS_R531_cneu.csv')
file_R796 = os.path.join(folder_path, 'BS_R795_cneu.csv')
file_R994 = os.path.join(folder_path, 'BS_R994_cneu.csv')
file_R1591 = os.path.join(folder_path, 'BS_R1591_cneu.csv')


df_R159 = pd.read_csv(file_R159)
df_R212 = pd.read_csv(file_R212)
df_R318 = pd.read_csv(file_R318)
df_R531 = pd.read_csv(file_R531)
df_R796 = pd.read_csv(file_R796)
df_R994 = pd.read_csv(file_R994)
df_R1591 = pd.read_csv(file_R1591)

# Spaltennamen bereinigen
for df in [df_R159, df_R212, df_R318, df_R531, df_R796, df_R994, df_R1591]:
    df.columns = df.columns.str.strip()
    

# Amplituden- und Phasendaten extrahieren
amplitude_R159 = df_R159.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R159 = df_R159.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R212 = df_R212.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R212 = df_R212.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R318 = df_R318.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R318 = df_R318.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R531 = df_R531.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R531 = df_R531.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R796 = df_R796.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R796 = df_R796.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R994 = df_R994.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R994 = df_R994.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R1591 = df_R1591.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R1591 = df_R1591.set_index('Frequency [Hz]')['Phase [deg]']

# Plot erstellen
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.semilogx(amplitude_R159.index, amplitude_R159, label='BS_R159')
ax1.semilogx(amplitude_R212.index, amplitude_R212, label='BS_R212')
ax1.semilogx(amplitude_R318.index, amplitude_R318, label='BS_R318')
ax1.semilogx(amplitude_R531.index, amplitude_R531, label='BS_R531')
ax1.semilogx(amplitude_R796.index, amplitude_R796, label='BS_R796')
ax1.semilogx(amplitude_R994.index, amplitude_R994, label='BS_R994')
ax1.semilogx(amplitude_R1591.index, amplitude_R1591, label='BS_R1591')
ax1.set_title('Amplitudengänge')
ax1.set_xlabel('Frequenz [Hz]')
ax1.set_ylabel('Amplitude [dB]')
ax1.legend(loc='lower left')  # Legende unten links
ax1.grid(True)

ax2.semilogx(phase_R159.index, phase_R159, label='BS_R159')
ax2.semilogx(phase_R212.index, phase_R212, label='BS_R212')
ax2.semilogx(phase_R318.index, phase_R318, label='BS_R318')
ax2.semilogx(phase_R531.index, phase_R531, label='BS_R531')
ax2.semilogx(phase_R796.index, phase_R796, label='BS_R796')
ax2.semilogx(phase_R994.index, phase_R994, label='BS_R994')
ax2.semilogx(phase_R1591.index, phase_R1591, label='BS_R1591')
ax2.set_title('Phasengänge')
ax2.set_xlabel('Frequenz [Hz]')
ax2.set_ylabel('Phase [°]')
ax2.legend(loc='lower left')  # Legende unten links
ax2.grid(True)

plt.tight_layout()
plt.show()


   


#eigene berechung von w0 
    
def find_center_frequency_by_phase(df):
    phase = df['Phase [deg]'].values
    frequency = df['Frequency [Hz]'].values

    for i in range(len(phase) - 1):
        if phase[i] * phase[i + 1] < 0:  # detektion des vorzeidchenwechsels
            x1, x2 = frequency[i], frequency[i + 1]
            y1, y2 = phase[i], phase[i + 1]
            x = x1 - y1 * (x2 - x1) / (y2 - y1) #interpolierte frequenz
            return x
    return None


center_freq_R159 = find_center_frequency_by_phase(df_R159)
center_freq_R212 = find_center_frequency_by_phase(df_R212)
center_freq_R318 = find_center_frequency_by_phase(df_R318)
center_freq_R531 = find_center_frequency_by_phase(df_R531)
center_freq_R796 = find_center_frequency_by_phase(df_R796)
center_freq_R994 = find_center_frequency_by_phase(df_R994)
center_freq_R1591 = find_center_frequency_by_phase(df_R1591)


def freq_0(Res):
    cap = 1e-6
    V_r = 9.73  #10.73 funktioniert von der Abweichung her sehr gut, selbiges mit Ref*x
    V_c = 1     # Ergebnis ist \pm7.5 % abweichung
    freq_0 = round(V_r / (2 * np.pi * V_c * cap * Res),2)
    return freq_0

def abweichung(df, Res):
    abw = round((1 - freq_0(Res)/find_center_frequency_by_phase(df)) * 100,2)
    return abw
    


print(f"Mittenfrequenz BS_R1591: {center_freq_R1591:.2f} Hz")
print("Theoriewert:             ", freq_0(1591),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R1591, 1591))

print(f"Mittenfrequenz BS_R994:  {center_freq_R994:.2f} Hz")
print("Theoriewert:            ", freq_0(994),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R994, 994))

print(f"Mittenfrequenz BS_R796:  {center_freq_R796:.2f} Hz")
print("Theoriewert:            ", freq_0(796),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R796, 796))

print(f"Mittenfrequenz BS_R531:  {center_freq_R531:.2f} Hz")
print("Theoriewert:            ", freq_0(531),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R531, 531))

print(f"Mittenfrequenz BS_R318:  {center_freq_R318:.2f} Hz")
print("Theoriewert:            ", freq_0(318),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R318, 318))

print(f"Mittenfrequenz BS_R212:  {center_freq_R212:.2f} Hz")
print("Theoriewert:            ", freq_0(212),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R212, 212))

print(f"Mittenfrequenz BS_R159:  {center_freq_R159:.2f} Hz")
print("Theoriewert:            ", freq_0(159),"Hz")
print("Abwichung in Prozent:   ", abweichung(df_R159, 159))


#%%


folder_path = '003_VCF_ohne_PD'
file_R994 = os.path.join(folder_path, 'BS_R994.csv')
file_R994_cneu = os.path.join(folder_path, 'BS_R994_cneu.csv')
file_R994_cneu_Vc2 = os.path.join(folder_path, 'BS_R994_cneu_Vc2.csv')




# Daten laden
df_R994 = pd.read_csv(file_R994)
df_R994_cneu = pd.read_csv(file_R994_cneu)
df_R994_cneu_Vc2 = pd.read_csv(file_R994_cneu_Vc2)

# Spaltennamen bereinigen
for df in [df_R994, df_R994_cneu, df_R994_cneu_Vc2]:
    df.columns = df.columns.str.strip()

# Amplituden- und Phasendaten extrahieren
amplitude_R994 = df_R994.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R994 = df_R994.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R994_cneu = df_R994_cneu.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R994_cneu = df_R994_cneu.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_R994_cneu_Vc2 = df_R994_cneu_Vc2.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_R994_cneu_Vc2 = df_R994_cneu_Vc2.set_index('Frequency [Hz]')['Phase [deg]']

# Plot erstellen
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.semilogx(amplitude_R994.index, amplitude_R994, label='BS_R994')
ax1.semilogx(amplitude_R994_cneu.index, amplitude_R994_cneu, label='BS_R994_cneu')
ax1.semilogx(amplitude_R994_cneu_Vc2.index, amplitude_R994_cneu_Vc2, label='BS_R994_cneu_Vc2')
ax1.set_title('Amplitudengänge')
ax1.set_xlabel('Frequenz [Hz]')
ax1.set_ylabel('Amplitude [dB]')
ax1.legend(loc='lower left')
ax1.grid(True)

ax2.semilogx(phase_R994.index, phase_R994, label='BS_R994')
ax2.semilogx(phase_R994_cneu.index, phase_R994_cneu, label='BS_R994_cneu')
ax2.semilogx(phase_R994_cneu_Vc2.index, phase_R994_cneu_Vc2, label='BS_R994_cneu_Vc2')
ax2.set_title('Phasengänge')
ax2.set_xlabel('Frequenz [Hz]')
ax2.set_ylabel('Phase [°]')
ax2.legend(loc='lower left')
ax2.grid(True)

plt.tight_layout()
plt.savefig('amplitude_phase_plots.png')
plt.show()




# Mittenfrequenz berechnen
def find_center_frequency_by_phase(df):
    phase = df['Phase [deg]'].values
    frequency = df['Frequency [Hz]'].values

    for i in range(len(phase) - 1):
        if phase[i] * phase[i + 1] < 0:  # Detektion des Vorzeichenwechsels
            x1, x2 = frequency[i], frequency[i + 1]
            y1, y2 = phase[i], phase[i + 1]
            x = x1 - y1 * (x2 - x1) / (y2 - y1)  # Interpolierte Frequenz
            return x
    return None

center_freq_R994 = find_center_frequency_by_phase(df_R994)
center_freq_R994_cneu = find_center_frequency_by_phase(df_R994_cneu)
center_freq_R994_cneu_Vc2 = find_center_frequency_by_phase(df_R994_cneu_Vc2)

def freq_0(Res):
    cap = 1e-6
    V_r = 9.73
    V_c = 1
    freq_0 = round(V_r / (2 * np.pi * V_c * cap * Res), 2)
    return freq_0

def freq_0_Vc2(Res):
    cap = 1e-6
    V_r = 9.73
    V_c = 2
    freq_0 = round(V_r / (2 * np.pi * V_c * cap * Res), 2)
    return freq_0

def abweichung(df, Res):
    abw = round((1 - freq_0(Res) / find_center_frequency_by_phase(df)) * 100, 2)
    return abw

# Ergebnisse ausgeben
print(f"Mittenfrequenz BS_R994: {center_freq_R994:.2f} Hz")
print("Theoriewert:             ", freq_0(994), "Hz")
print("Abweichung in Prozent:   ", abweichung(df_R994, 994))

print(f"Mittenfrequenz BS_R994_cneu: {center_freq_R994_cneu:.2f} Hz")
print("Theoriewert:             ", freq_0(994), "Hz")
print("Abweichung in Prozent:   ", abweichung(df_R994_cneu, 994))

print(f"Mittenfrequenz BS_R994_cneu_Vc2: {center_freq_R994_cneu_Vc2:.2f} Hz")
print("Theoriewert:             ", freq_0_Vc2(994), "Hz")
print("Abweichung in Prozent:   ", 5.51)



#%% Gesamtsystem

folder_path = '002_self_tuned_filter'
file_BP = os.path.join(folder_path, 'BP_redp_19.01.csv')
file_BS = os.path.join(folder_path, 'BS_redp_19.01.csv')
file_TP = os.path.join(folder_path, 'TP_redp_19.01.csv')
file_HP = os.path.join(folder_path, 'HP_redp_19.01.csv')

df_BP = pd.read_csv(file_BP)
df_BS = pd.read_csv(file_BS)
df_TP = pd.read_csv(file_TP)
df_HP = pd.read_csv(file_HP)

# Spaltennamen bereinigen
for df in [df_BP, df_BS, df_TP, df_HP]:
    df.columns = df.columns.str.strip()

# Amplituden- und Phasendaten extrahieren
amplitude_BP = df_BP.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_BP = df_BP.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_BS = df_BS.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_BS = df_BS.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_TP = df_TP.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_TP = df_TP.set_index('Frequency [Hz]')['Phase [deg]']

amplitude_HP = df_HP.set_index('Frequency [Hz]')['Amplitude [dB]']
phase_HP = df_HP.set_index('Frequency [Hz]')['Phase [deg]']

# Plot erstellen
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.semilogx(amplitude_BP.index, amplitude_BP, label='BP_redp_neu')
ax1.semilogx(amplitude_BS.index, amplitude_BS, label='BS_redp_neu')
ax1.semilogx(amplitude_TP.index, amplitude_TP, label='TP_redp_neu')
ax1.semilogx(amplitude_HP.index, amplitude_HP, label='HP_redp_neu')
ax1.set_title('Amplitudengänge')
ax1.set_xlabel('Frequenz [Hz]')
ax1.set_ylabel('Amplitude [dB]')
ax1.legend(loc='lower left')
ax1.grid(True)

ax2.semilogx(phase_BP.index, phase_BP, label='BP_redp_neu')
ax2.semilogx(phase_BS.index, phase_BS, label='BS_redp_neu')
ax2.semilogx(phase_TP.index, phase_TP, label='TP_redp_neu')
ax2.semilogx(phase_HP.index, phase_HP, label='HP_redp_neu')
ax2.set_title('Phasengänge')
ax2.set_xlabel('Frequenz [Hz]')
ax2.set_ylabel('Phase [°]')
ax2.legend(loc='lower left')
ax2.grid(True)

plt.tight_layout()
plt.show()
