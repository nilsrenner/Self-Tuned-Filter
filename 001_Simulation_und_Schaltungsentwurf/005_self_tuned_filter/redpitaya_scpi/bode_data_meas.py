#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Measurements for Bode plots
Input signal: DF_IN1
Output signal: DF_IN2

@author: Mirco Meiners (HSB)
"""

# %% Init
import time
from datetime import datetime
import redpitaya_scpi as scpi
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

# %% Connection params
LABDESK = {
    "ELIE1": "192.168.111.181",
    "ELIE2": "192.168.111.182",
    "ELIE3": "192.168.111.183",
    "ELIE4": "192.168.111.184",
    "ELIE5": "192.168.111.185",
    "ELIE6": "192.168.111.186"
}

IP = LABDESK["ELIE4"]  # IP des Laborplatzes
rp = scpi.scpi(IP)

DATA_SIZE = 1024 * 16       # ((1024 * 1024 * 128) / 2) ## for 128 MB ##
READ_DATA_SIZE = 1024 * 16  # (1024 * 256)              ## for 128 MB ##

dec = 64
trig_lvl = 0.5

# %% Measurement / Data Accquisition
TSTAMP = datetime.datetime.now()

DF_IN1 = pd.DataFrame()
DF_IN2 = pd.DataFrame()

# Parameters
func = 'SINE'
ampl = 0.5
offset = 0.0
freqs = np.arange(800, 1200, 5)

for freq in freqs:

    rp.tx_txt('ANALOG:RST ')  # Set analog outputs to 0V
    rp.tx_txt('GEN:RST')  # Signal Generator reset
    rp.tx_txt('PHAS:ALIGN')  # Synchronize
    rp.tx_txt('SOUR1:TRig:INT')
    rp.tx_txt('SOUR1:FUNC ' + str(func))  # Wellenform
    rp.tx_txt('SOUR1:VOLT ' + str(ampl))  # Amplitude
    rp.tx_txt('SOUR1:VOLT:OFFS ' + str(offset))  # Offset
    rp.tx_txt('SOUR1:PHAS ' + str(offset))  # Offset
    rp.tx_txt('SOUR1:FREQ:FIX:Direct ' + str(freq))  # Frequenz
    # rp.tx_txt('SOUR1:FREQ:FIX ' + str(freq))  # Frequenz

    # Enable output
    rp.tx_txt('OUTPUT1:STATE ON')
    rp.tx_txt('SOUR1:TRig:INT')

    time.sleep(1)  # in Sekunden

    # print("Start program")

    # ACQUISITION
    rp.tx_txt('ACQ:RST')  # Input reset

    # Get memory region (DMM)
    start_address = int(rp.txrx_txt('ACQ:AXI:START?'))
    size = int(rp.txrx_txt('ACQ:AXI:SIZE?'))
    start_address2 = round(start_address + size/2)

    rp.tx_txt(f"ACQ:AXI:DEC {dec}")  # Decimation
    # rp.tx_txt(f"ACQ:DEC {dec}")  # Decimation (1, 8, 16, 64, 1024, 8192)

    rp.tx_txt('ACQ:AXI:DATA:Units VOLTS')  # Set units
    # rp.tx_txt('ACQ:DATA:Units VOLTS')

    rp.tx_txt(f"ACQ:AXI:SOUR1:Trig:Dly {DATA_SIZE}")  # Trigger delay ch1
    rp.tx_txt(f"ACQ:AXI:SOUR2:Trig:Dly {DATA_SIZE}")  # Trigger delay ch2
    # rp.tx_txt(f"ACQ:TRig:DLY {DATA_SIZE}")  # Delay

    # Set-up channel 1 and 2 buffers to each work with half of available memory space.
    rp.tx_txt(f"ACQ:AXI:SOUR1:SET:Buffer {start_address},{size/2}")
    rp.tx_txt(f"ACQ:AXI:SOUR2:SET:Buffer {start_address2},{size/2}")

    rp.tx_txt('ACQ:AXI:SOUR1:ENable ON')  # Enable DMM ch1
    rp.tx_txt('ACQ:AXI:SOUR2:ENable ON')  # Enable DMM ch2

    rp.tx_txt(f"ACQ:TRig:LEV {trig_lvl}")  # Trigger level

    rp.tx_txt('ACQ:START')  # Start aquisition
    # rp.tx_txt('ACQ:TRig NOW')  # Trigger manually

    # print("Waiting for trigger\n")
    # This loop is not needed, if triggered manually
    while 1:
        rp.tx_txt('ACQ:TRig:STAT?')
        if rp.rx_txt() == 'TD':
            break

    # while 1:
    #    rp.tx_txt('ACQ:TRig:FILL?')
    #    if rp.rx_txt() == '1':
    #        break

    # wait for fill adc buffer DMM
    while 1:
        rp.tx_txt('ACQ:AXI:SOUR1:TRig:FILL?')
        if rp.rx_txt() == '1':
            print('DMA buffer full\n')
            break

    # Data Acquisition

    # Input IN1
    # rp.tx_txt('ACQ:SOUR1:DATA?')  # Readout buffer IN1
    posIN1 = int(rp.txrx_txt('ACQ:AXI:SOUR1:Trig:Pos?'))
    rp.tx_txt(f"ACQ:AXI:SOUR1:DATA:Start:N? {posIN1},{READ_DATA_SIZE}")
    IN1str = rp.rx_txt()
    IN1str = IN1str.strip('{}\n\r').replace("  ", "").split(',')
    DF_IN1[str(freq)] = np.array(list(map(float, IN1str)))

    # Input IN2
    # rp.tx_txt('ACQ:SOUR2:DATA?')  # Readout buffer IN2
    posIN2 = int(rp.txrx_txt('ACQ:AXI:SOUR2:Trig:Pos?'))
    rp.tx_txt(f"ACQ:AXI:SOUR2:DATA:Start:N? {posIN2},{READ_DATA_SIZE}")
    IN2str = rp.rx_txt()
    IN2str = IN2str.strip('{}\n\r').replace("  ", "").split(',')
    DF_IN2[str(freq)] = np.array(list(map(float, IN2str)))


# Stop Acquisition
rp.tx_txt('ACQ:STOP')

# Stopp des Generators
rp.tx_txt('OUTPUT1:STATE OFF')

# %% Data storage
# + str(datetime.now().strftime('%Y-%m-%d_%H_%M'))
Data_IN1 = 'data/IN1_UB_VBS'
# + str(datetime.now().strftime('%Y-%m-%d_%H_%M'))
Data_IN2 = 'data/IN2_UB_VBP'
# Data_IN = 'data/IN_UB_VBS_VBP'  #+ str(datetime.now().strftime('%Y-%m-%d_%H_%M'))

# %% Store data on disk as comma-seperated-values
DF_IN1.to_csv(Data_IN1 + '.csv', index=False)
DF_IN2.to_csv(Data_IN2 + '.csv', index=False)

# %% Store data on disk as excel sheet
# with pd.ExcelWriter(Data_IN + '.xlsx') as writer:
#     DF_IN1.to_excel(writer, sheet_name='IN1', index=False)
#     DF_IN2.to_excel(writer, sheet_name='IN2', index=False)

# DF_IN1.to_excel(Data_IN1 + '.xlsx', index=False)
# DF_IN2.to_excel(Data_IN2 + '.xlsx', index=False)

# %% Store data on disk as HDF5
# DF_IN1.to_hdf(Data_IN1 + ".h5", "table", append=True)
# DF_IN2.to_hdf(Data_IN2 + ".h5", "table", append=True)

# %% Store data on disk as apache parquet
# DF_IN1.to_parquet(Data_IN1 + ".parquet", index=False)
# DF_IN2.to_parquet(Data_IN2 + ".parquet", index=False)

# %% Store data on disk as apache feather
# DF_IN1.to_feather(Data_IN1 + ".feather")
# DF_IN2.to_feather(Data_IN2 + ".feather")

# %% Plot
# plt.plot(DF_IN1['1000'], label='IN1')
# plt.plot(DF_IN2['1000'], label='IN2')
# plt.legend()
# plt.show()
