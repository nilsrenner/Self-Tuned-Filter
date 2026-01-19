import network
import socket
import time

# Startwerte
freq0 = 160.0
Q_val = 1.0
H0_val = 1.0


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
server.bind(addr)
server.listen(1)

print("HTTP Server läuft...")
print("Beispiel:")
print("http://%s/set?freq=200&Q=1.5&H0=0.8" % ip)


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