import math
from machine import Pin, SPI
#import machine

import network
import socket
import time


led = Pin("LED", Pin.OUT)

# 1. Start-Check: LED blinkt 5 mal schnell
# Wenn du das siehst, weißt du: Der Pico hat Strom und der Code läuft!
for _ in range(5):
    led.value(1)
    time.sleep(0.1)
    led.value(0)
    time.sleep(0.1)

led.value(1) # LED bleibt an: WLAN wird jetzt gestartet


###   Initialisierung


# Sollwerte
freq0 = 160  # Bauteilbedingte Grenzfrequenz in Hz
Q_val = 1
H0_val = 1

# Digitalpoti-Parameter
max_step = 255
r_ges = 9.65e3
wiper_r = 2  # wiper_r von ca 70 Ohm


freq_wiper = 0
freq_r     = 0

Q_wiper = 0
Q_r     = 0

H0_wiper = 0
H0_r     = 0


# Werte berechnen
def clamp_and_round(x):
    return int(round(max(0, min(255, x))))

def freq_2_bit(freq0):
    freq_c = 1e-6   #1uF
    #vielleicht einzelne rges für jeden wiper?
    wfreq0 = freq0 * 2 * math.pi
    freq_r = 1/(wfreq0 * freq_c)
    freq_wiper = max_step * (1 - freq_r/r_ges) + wiper_r    # mein R in der Gleichung
    return clamp_and_round(freq_wiper), freq_r                                      

def Q_2_bit(Q_val):
    r_opv = 1000
    Q_r = Q_val * r_opv
    Q_wiper = max_step * (1 - Q_r/r_ges) + wiper_r
    return clamp_and_round(Q_wiper), Q_r

def H0_2_bit(H0_val):
    r_opv = 1000
    H0_r = r_opv/H0_val
    H0_wiper = max_step * (1 - H0_r/r_ges) + wiper_r
    #H0_wiper = int(round(H0_wiper))
    return clamp_and_round(H0_wiper), H0_r

def bit_2_res(bit):
    res = r_ges * (1 - (bit-wiper_r)/max_step)      #vorher bit-wiper_r
    return res

def update_filter(freq0, Q_val, H0_val):
    global freq_wiper, freq_r, Q_wiper, Q_r, H0_wiper, H0_r
    freq_wiper, freq_r = freq_2_bit(freq0)
    Q_wiper,    Q_r    = Q_2_bit(Q_val)
    H0_wiper,   H0_r   = H0_2_bit(H0_val)

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
    
        
    
    
# eigenes WLAN aufbauen statt WLAN verbinden

ap = network.WLAN(network.AP_IF)
ap.active(True)

ap.config(
    essid="Pico-Filter",
    password="filter123"
)


# Feste IP setzen
ap.ifconfig(("192.168.4.1", "255.255.255.0", "192.168.4.1", "8.8.8.8"))

print("Access Point aktiv")
print("SSID: Pico-Filter")
print("IP:", ap.ifconfig()[0])
time.sleep(1)



#HTTP Server
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # sonst startet der gleiche Server beim reupload nicht
server.bind(addr)
server.listen(1)

print("HTTP Server läuft...")
AP_IP = ap.ifconfig()[0]
print("http://%s/filter" % AP_IP)



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

            <h2>Aktueller Zustand</h2>

            <table border="1" cellpadding="6" cellspacing="0">
                <tr>
                    <th>Parameter</th>
                    <th>Wert</th>
                    <th>Ist-R (aus Bit)</th>
                    <th>Soll-R (Theorie)</th>
                </tr>

                <tr>
                    <td>Freq</td>
                    <td>{freq0} Hz</td>
                    <td>{bit_2_res(freq_wiper):.1f} Ω</td>
                    <td>{freq_r:.1f} Ω</td>
                </tr>

                <tr>
                    <td>Q</td>
                    <td>{Q_val}</td>
                    <td>{bit_2_res(Q_wiper):.1f} Ω</td>
                    <td>{Q_r:.1f} Ω</td>
                </tr>

                <tr>
                    <td>H0</td>
                    <td>{H0_val}</td>
                    <td>{bit_2_res(H0_wiper):.1f} Ω</td>
                    <td>{H0_r:.1f} Ω</td>
                </tr>
            </table>

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
    
