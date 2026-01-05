from machine import Pin, SPI
import time


### SPI und Pins Initialisieren
# SPI Channel 0 auf GPIO18/19/16
spi = SPI(
    0,
    baudrate=1_000_000,
    polarity=0,
    phase=0,
    bits=8,
    firstbit=SPI.MSB,
    sck=Pin(18),
    mosi=Pin(19),
    miso=Pin(16),
)

# Chip-Selects (aktiv low)
cs1 = Pin(17, Pin.OUT, value=1) #Mittenfreqzenzbestimmend
cs2 = Pin(20, Pin.OUT, value=1) #Für Q und H0 wiper0 = Q


### Befehlswort aufbauen
def mcp_write(cs_pin, command, value):
    cs_pin.value(0)           # CS dieses Chips low → Chip wird angesprochen
    spi.write(bytes([command & 0xFF, value & 0xFF]))  # 16 Bit: [Cmd|Data]
    cs_pin.value(1)           # CS high → Chip wird freigegeben


def set_wiper0(cs_pin, value):  # Immer Wiper0 DES JEWEILIGEN Chips
    cmd = 0x00                 # 0000 00xx = Wiper 0 Adresse + Write
    mcp_write(cs_pin, cmd, value)

def set_wiper1(cs_pin, value):  # Immer Wiper1 DES JEWEILIGEN Chips  
    cmd = 0x10                 # 0001 00xx = Wiper 1 Adresse + Write
    mcp_write(cs_pin, cmd, value)


set_wiper0(cs1, 26)    # Chip1 Wiper0 = ca 10% = 1k
set_wiper1(cs1, 26)   # Chip1 Wiper1 = ca 10%  
set_wiper0(cs2, 128)   # Chip2 Wiper0 = 50%     wiper0 = Q
set_wiper1(cs2, 32)    # Chip2 Wiper1 = 12,5%

