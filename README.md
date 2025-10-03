🌱 Smart Plant Monitoring System – Raspberry Pi Pico W

A smart IoT-based plant monitoring system using Raspberry Pi Pico W. The project measures **temperature, humidity, soil moisture, light intensity, and water level** in real time and hosts a simple web dashboard accessible via Wi-Fi. It also triggers a **buzzer alert when low water is detected**.

🔑 Features

- 🌡️ Temperature & humidity monitoring with DHT11  
- 🌱 Soil moisture detection via analog sensor  
- 💡 Light intensity measurement using LDR  
- 💧 Water level detection with buzzer alerts  
- 📡 Wi-Fi enabled real-time monitoring (Pico W)  
- 🌍 Web server with auto-refresh dashboard  


🛠️ Hardware Required

- Raspberry Pi Pico W  
- DHT11 Temperature & Humidity Sensor  
- Soil Moisture Sensor  
- LDR (Light Dependent Resistor)  
- Water Level Sensor  
- Buzzer  
- Breadboard, Jumper Wires, Power Supply  

⚙️ Software & Setup

1. Install **MicroPython** on your Raspberry Pi Pico W.  
2. Upload the project files (e.g., `main.py`).  
3. Edit Wi-Fi credentials inside the code:

```python
ssid = 'Your_SSID'
password = 'Your_PASSWORD'

4.Run the script and connect Pico W to Wi-Fi.

5.Open a browser and go to http://<Pico_W_IP> to view the dashboard.

🖥️ Web Dashboard Preview

The Pico W hosts a simple webpage that auto-refreshes every 2 seconds, displaying:
🌡️ Temperature (°C)
💧 Humidity (%)
🌱 Soil Moisture (raw value)
💡 Light Intensity (LDR raw value)
🚨 Water level status (green/red with buzzer alert)

📂 Project Structure
├── main.py            # Core code (sensors + web server)
├── README.md          # Project documentation

🚀 Future Improvements

-Add automatic irrigation using a water pump.
-Store sensor data in a cloud database (Firebase / MQTT).
-Add mobile-friendly UI for the dashboard.
-Deploy with IoT platforms like Blynk / ThingsBoard.
