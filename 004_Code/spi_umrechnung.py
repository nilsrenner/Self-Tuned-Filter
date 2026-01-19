import math
from machine import Pin, SPI
import time

### Sollwerte
freq0 = 160  # Bauteilbedingte Grenzfrequenz in Hz
Q_val = 1
H0_val = 1

### Digitalpoti-Parameter
max_step = 255
r_ges = 9.65e3
wiper_r = 2  # wiper_r von ca 70 Ohm


### Werte berechnen
def clamp_and_round(x):
    return int(round(max(0, min(255, x))))

def freq_2_bit(freq0):
    freq_c = 1e-6   #1uF
    #vielleicht einzelne rges für jeden wiper?
    wfreq0 = freq0 * 2 * math.pi
    freq_r = 1/(wfreq0 * freq_c)
    freq_wiper = max_step * (1 - freq_r/r_ges) + wiper_r    # mein R in der Gleichung
    return clamp_and_round(freq_wiper)                                       

def Q_2_bit(Q_val):
    r_opv = 1000
    Q_r = Q_val * r_opv
    Q_wiper = max_step * (1 - Q_r/r_ges) + wiper_r
    return clamp_and_round(Q_wiper)

def H0_2_bit(H0_val):
    r_opv = 1000
    H0_r = r_opv/H0_val
    H0_wiper = max_step * (1 - H0_r/r_ges) + wiper_r
    H0_wiper = int(round(H0_wiper))
    return clamp_and_round(H0_wiper)

def bit_2_res(bit):
    res = r_ges * (1 - (bit-wiper_r)/max_step)      #vorher bit-wiper_r
    return res


freq_wiper = freq_2_bit(freq0)
Q_wiper    = Q_2_bit(Q_val)
H0_wiper   = H0_2_bit(H0_val)



### SPI und Pins Initialisieren
# SPI Channel 0 auf GPIO18/19/16
spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
    sck=Pin(18), mosi=Pin(19), miso=Pin(16))

# Chip-Selects (aktiv low)
cs1 = Pin(17, Pin.OUT, value=1) #Mittenfreqzenzbestimmend
cs2 = Pin(20, Pin.OUT, value=1) #Für Q und H0 wiper0 = Q

# Befehlswort aufbauen
def mcp_write(cs_pin, command, value):
    cs_pin.value(0)           # CS low → Chip wird angesprochen
    spi.write(bytes([command & 0xFF, value & 0xFF]))  # 16 Bit: [Cmd|Data]
    cs_pin.value(1)           # CS high → Chip wird freigegeben


def set_wiper0(cs_pin, value):  # Immer Wiper0 DES JEWEILIGEN Chips
    cmd = 0x00                 # 0000 00xx = Wiper 0 Adresse + Write
    mcp_write(cs_pin, cmd, value)

def set_wiper1(cs_pin, value):  # Immer Wiper1 DES JEWEILIGEN Chips  
    cmd = 0x10                 # 0001 00xx = Wiper 1 Adresse + Write
    mcp_write(cs_pin, cmd, value)
    
    
# Schreiben der berechneten Werte
set_wiper0(cs1, freq_wiper)
set_wiper1(cs1, freq_wiper)
set_wiper0(cs2, Q_wiper)
set_wiper1(cs2, H0_wiper)

    
print("freq_wiper:", freq_wiper)
print("R_freq_real:", bit_2_res(freq_wiper))
print("Q_wiper:", Q_wiper)
print("R_Q_real:", bit_2_res(Q_wiper))
print("H0_wiper:", H0_wiper)
print("R_H0_real:", bit_2_res(H0_wiper))

    
    
    
    
    
