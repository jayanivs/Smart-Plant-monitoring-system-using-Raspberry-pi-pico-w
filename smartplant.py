# ==== Import Required Libraries ====
import network        # For Wi-Fi connectivity
import socket         # For creating a simple web server
from machine import Pin, ADC  # Pin control and analog-to-digital conversion
import time           # For delays
import dht            # For DHT temperature/humidity sensor

# ==== Wi-Fi Setup ====
ssid = 'your SSID'         # Wi-Fi network name
password = 'your PASSWORD' # Wi-Fi password

# Initialize the WLAN interface in station mode (client mode)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)     # Activate Wi-Fi interface
wlan.connect(ssid, password)  # Connect to Wi-Fi

# Wait until connected
print("Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep(1)  # Wait for 1 second before checking again

# Once connected, print the IP address assigned by the router
print("Connected! IP:", wlan.ifconfig()[0])

# ==== Sensor Pins Configuration ====
DHT_PIN = 16       # GPIO for DHT11 temperature/humidity sensor
SOIL_PIN = 26      # GPIO for soil moisture sensor (analog)
LDR_PIN = 27       # GPIO for light sensor (analog)
BUZZER_PIN = 17    # GPIO for buzzer
WATER_PIN = 15     # GPIO for water level sensor (digital)

# ==== Initialize Sensors ====
dht_sensor = dht.DHT11(Pin(DHT_PIN))    # Initialize DHT11
soil_sensor = ADC(Pin(SOIL_PIN))        # Initialize soil moisture sensor
ldr_sensor = ADC(Pin(LDR_PIN))          # Initialize LDR (light sensor)
buzzer = Pin(BUZZER_PIN, Pin.OUT)       # Initialize buzzer as output
water_sensor = Pin(WATER_PIN, Pin.IN, Pin.PULL_UP)  # Initialize water sensor as input with pull-up resistor

# ==== Web Server Setup ====
# Close the previous socket if it exists
try:
    s.close()
except:
    pass

# Get server address (listen on all interfaces at port 80)
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

# Create a TCP socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of the socket
s.bind(addr)  # Bind the socket to the IP and port
s.listen(1)   # Listen for 1 connection at a time
print("Web server started at http://{}".format(wlan.ifconfig()[0]))

# ==== Main Loop ====
while True:
    # Wait for a client to connect (e.g., a browser)
    cl, addr = s.accept()
    print("Client connected from", addr)

    # Get a file-like object from the client socket
    cl_file = cl.makefile('rwb', 0)

    # Read HTTP request headers (we ignore the content)
    while True:
        line = cl_file.readline()
        if not line or line == b"\r\n":  # End of headers
            break

    # ==== Read Sensors ====
    try:
        dht_sensor.measure()          # Trigger DHT sensor reading
        temperature = dht_sensor.temperature()  # Get temperature in °C
        humidity = dht_sensor.humidity()        # Get humidity in %
    except:
        temperature = "Error"
        humidity = "Error"

    soil_value = soil_sensor.read_u16()  # Read soil moisture (0-65535)
    ldr_value = ldr_sensor.read_u16()    # Read LDR light value (0-65535)
    water_level = water_sensor.value()   # Read water sensor (0 or 1)
    
    # Determine water status message
    water_status = "Water Detected!" if water_level else "No Water"

    # Activate buzzer if no water detected
    if not water_level:
        buzzer.value(1)  # Turn buzzer ON
    else:
        buzzer.value(0)  # Turn buzzer OFF

    # ==== Create HTML Page ====
    html = """<!DOCTYPE html>
<html>
  <head>
    <title>Pico W Sensor Dashboard</title>
    <meta http-equiv="refresh" content="2"> <!-- Auto-refresh every 2 seconds -->
    <style>
      body {{ font-family: Arial; text-align: center; margin-top: 40px; }}
      .status {{ font-size: 20px; }}
    </style>
  </head>
  <body>
    <h2>Raspberry Pi Pico W Sensor Readings</h2>
    <p class="status">Temperature: {} °C</p>
    <p class="status">Humidity: {} %</p>
    <p class="status">Soil Moisture: {}</p>
    <p class="status">Light Level (LDR): {}</p>
    <p class="status">Water Level: <b style="color:{}">{}</b></p>
  </body>
</html>""".format(
        temperature,
        humidity,
        soil_value,
        ldr_value,
        "green" if water_level else "red",  # Green if water present, red if not
        water_status
    )

    # ==== Send HTML Response to Client ====
    cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    cl.sendall(html)  # Send the HTML content
    cl.close()        # Close the client connection

    # Wait 1 second before next loop iteration
    time.sleep(1)
