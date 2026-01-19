import math
from machine import Pin, SPI


import network
import socket
import time


###   Initialisierung


# Sollwerte
freq0 = 160  # Bauteilbedingte Grenzfrequenz in Hz
Q_val = 1
H0_val = 1

# Digitalpoti-Parameter
max_step = 255
r_ges = 9.65e3
wiper_r = 2  # wiper_r von ca 70 Ohm


# Werte berechnen
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

def update_filter(freq0, Q_val, H0_val):
    freq_wiper = freq_2_bit(freq0)
    Q_wiper    = Q_2_bit(Q_val)
    H0_wiper   = H0_2_bit(H0_val)

    set_wiper0(cs1, freq_wiper)
    set_wiper1(cs1, freq_wiper)
    set_wiper0(cs2, Q_wiper)
    set_wiper1(cs2, H0_wiper)

    print("Filter aktualisiert:")
    print(" freq =", freq0, "->", freq_wiper, "(", bit_2_res(freq_wiper), "Ohm )")
    print(" Q    =", Q_val, "->", Q_wiper,    "(", bit_2_res(Q_wiper),    "Ohm )")
    print(" H0   =", H0_val, "->", H0_wiper,   "(", bit_2_res(H0_wiper),   "Ohm )")


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


def set_wiper0(cs_pin, value):  # Immer Wiper0 des Chips
    cmd = 0x00                 # 0000 00xx = Wiper 0 Adresse + Write
    mcp_write(cs_pin, cmd, value)

def set_wiper1(cs_pin, value):  # Immer Wiper1 des Chips  
    cmd = 0x10                 # 0001 00xx = Wiper 1 Adresse + Write
    mcp_write(cs_pin, cmd, value)
    
        
    
    
# WLAN verbinden
SSID = "Netzkiwi"             #"WLANAZHB"
PASSWORD = "Apfelkuchen123"   #"Elektro232egs232"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Verbinde mit WLAN...")

timeout = 20  # Sekunden
start = time.time()

while not wlan.isconnected():
    if time.time() - start > timeout:
        print("WLAN-Verbindung fehlgeschlagen")
        print("Status:", wlan.status())
        break
    time.sleep(0.5)

if wlan.isconnected():
    ip = wlan.ifconfig()[0]
    print("WLAN verbunden, IP:", ip)
    

#HTTP Server
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # sonst startet der gleiche Server beim reupload nicht
server.bind(addr)
server.listen(1)

print("HTTP Server läuft...")
print("Beispiel:")
print("http://%s/set?freq=200&Q=1.5&H0=0.8" % ip)


update_filter(freq0, Q_val, H0_val)



#Mailoop
while True:
    client, remote_addr = server.accept()
    request = client.recv(1024).decode()

    try:
        if "GET /set?" in request:
            line = request.split("\r\n")[0]
            path = line.split(" ")[1]          # /set?freq=...&Q=...&H0=...
            query = path.split("?")[1]
            params = query.split("&")

            for p in params:
                key, value = p.split("=")

                if key == "freq":
                    freq0 = float(value)
                elif key == "Q":
                    Q_val = float(value)
                elif key == "H0":
                    H0_val = float(value)
            
            
            
            update_filter(freq0, Q_val, H0_val)

            print("\nNeue Parameter empfangen:")
            print(" freq =", freq0)
            print(" Q    =", Q_val)
            print(" H0   =", H0_val)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Filter UI</title>
        </head>
        <body>
            <h1>Filter Parameter</h1>

            <form action="/set" method="get">
                <label>Freq (Hz):</label><br>
                <input type="number" name="freq" step="1" value="{freq0}"><br><br>

                <label>Q:</label><br>
                <input type="number" name="Q" step="0.1" value="{Q_val}"><br><br>

                <label>H0:</label><br>
                <input type="number" name="H0" step="0.1" value="{H0_val}"><br><br>

                <input type="submit" value="Setzen">
            </form>

            <p>
                Aktuell:<br>
                freq = {freq0}<br>
                Q = {Q_val}<br>
                H0 = {H0_val}
            </p>
        </body>
        </html>
        """

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n\r\n"
            + html
        )


    except Exception as e:
        print("Fehler:", e)
        response = "HTTP/1.1 500 ERROR\r\n\r\n"

    client.send(response)
    client.close()    
    
