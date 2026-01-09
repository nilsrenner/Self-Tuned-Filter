from machine import Pin, SPI
import time


### SPI und Pins Initialisieren
# SPI Channel 0 auf GPIO18/19/16
spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
    sck=Pin(18), mosi=Pin(19), miso=Pin(16))

# Chip-Selects (aktiv low)
cs1 = Pin(17, Pin.OUT, value=1) #Mittenfreqzenzbestimmend
cs2 = Pin(20, Pin.OUT, value=1) #Für Q und H0 wiper0 = Q


### Befehlswort aufbauen
def mcp_write(cs_pin, command, value):
    cs_pin.value(0)             # CS dieses Chips low → Chip wird angesprochen
    spi.write(bytes([command & 0xFF, value & 0xFF]))  # 16 Bit: [Cmd|Data]
    cs_pin.value(1)             # CS high → Chip wird freigegeben

def set_wiper0_nv(cs_pin, value):  # Immer Wiper0 DES JEWEILIGEN Chips
    cmd = 0x20                  # 0010 00xx = Wiper 0 Adresse + Write
    mcp_write(cs_pin, cmd, value)

def set_wiper1_nv(cs_pin, value):  # Immer Wiper1 DES JEWEILIGEN Chips  
    cmd = 0x30                  # 0011 00xx = Wiper 1 Adresse + Write
    mcp_write(cs_pin, cmd, value)



### Dieser Code sollte nicht mehr verwendet werden müssen, nur für neuen Poti.
### Dann dies (einzeln) Unkommentieren und vielleicht nach einander ausführen

#set_wiper0_nv(cs1, 232)    # Chip1 Wiper0
#set_wiper1_nv(cs1, 232)   # Chip1 Wiper1  
#set_wiper0_nv(cs2, 232)   # Chip2 Wiper0 
#set_wiper1_nv(cs2, 232)    # Chip2 Wiper1 



def read_wiper0_nv(cs_pin):
    tx = bytearray([0x2C, 0x00])  # 0010 1100 = NV Wiper0 Read ✓
    rx = bytearray(2)
    cs_pin.value(0)
    spi.write_readinto(tx, rx)
    cs_pin.value(1)
    return rx[1]

def read_wiper1_nv(cs_pin):
    tx = bytearray([0x3C, 0x00])  # 0011 1100 = NV Wiper1 Read ✓
    rx = bytearray(2)
    cs_pin.value(0)
    spi.write_readinto(tx, rx)
    cs_pin.value(1)
    return rx[1]

# Nach NV Write: Verify!
print("=== NV VERIFY ===")
print("CS1 W0 NV:", read_wiper0_nv(cs1))   # Sollte 232 sein
print("CS1 W1 NV:", read_wiper1_nv(cs1))   # Sollte 232 sein!? ← PROBLEM
print("CS2 W0 NV:", read_wiper0_nv(cs2))
print("CS2 W1 NV:", read_wiper1_nv(cs2))