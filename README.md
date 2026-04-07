# 📡 ESP32 Ultrasonic Radar Mapper

A real-time, sweeping radar visualization system built with an **ESP32**, an **HC-SR04 Ultrasonic Sensor**, a standard **180° Servo Motor**, and a **Proximity Buzzer**. 

This project bridges embedded hardware and PC software. The ESP32 acts as the hardware backend—sweeping the environment, calculating distances, and triggering physical alarms—while a Python/Pygame script running on the PC parses the serial data stream to render a classic, fading green radar UI.

## ✨ Features
* **Real-Time Data Streaming:** 50Hz serial communication between the microcontroller and the PC.
* **Proximity Alarm:** Integrated hardware buzzer that acts as a physical security alarm if an object breaches a customizable critical range (e.g., 20cm).
* **Hardware-Level Echo Interference Prevention:** Custom timing logic ensures clean sonic pulses by preventing echo-overlap.
* **Dynamic Pygame UI:** Features a custom graphics engine rendering a sweeping beam, accurate distance tracking, and a dynamic fading trail effect (simulating phosphor persistence).
* **Signal Blocking Visuals:** The radar beam dynamically turns red behind detected objects to simulate acoustic shadows.

## 🧰 Hardware Requirements
* ESP32 Development Board
* HC-SR04 Ultrasonic Sensor
* 180° Micro Servo Motor (e.g., SG90)
* Active Buzzer (or Passive Buzzer with PWM)
* Jumper Wires & Breadboard

## 🔌 Wiring Diagram
*Note: This project strictly avoids ESP32 strapping pins to guarantee safe boot sequences.*

| Component | Pin | ESP32 Connection |
| :--- | :--- | :--- |
| **Ultrasonic Sensor** | VCC | 5V / VIN |
| | GND | GND |
| | Trig | **GPIO 13** |
| | Echo | **GPIO 14** |
| **Servo Motor** | Power (Red) | 5V / VIN |
| | Ground (Brown) | GND |
| | Signal (Yellow) | **GPIO 27** |
| **Buzzer** | Power (+) | **GPIO 26** |
| | Ground (-) | GND |

## 💻 Software Setup

### 1. The Hardware Backend (ESP32)
1. Flash the ESP32 with the MicroPython firmware.
2. Upload the `main.py` script to the root directory of the ESP32.
3. The board will automatically execute the sweep, manage the alarm logic, and begin broadcasting serial data. 

### 2. The Visual Frontend (PC)
The PC interface requires Python 3.x. 

1. Clone this repository:
```bash
git clone [https://github.com/Aman22112005/ESP32-Ultrasonic-Radar.git](https://github.com/Aman22112005/ESP32-Ultrasonic-Radar.git)
cd ESP32-Ultrasonic-Radar
```

2. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```
Configure the COM Port: Open real_radar.py and update the arduino_port variable to match the COM port assigned to your ESP32 (e.g., COM3 on Windows or /dev/ttyUSB0 on Linux).

3.Run the visualization:
```bash
python real_radar.py
```

## 🛠️ Troubleshooting
* **ModuleNotFoundError:** Ensure you installed the dependencies via the requirements file, or manually via pip install pyserial pygame.
* **Access Denied / Port Busy:** Ensure IDEs like Thonny or Arduino are completely closed before running the Pygame script. Only one application can access the serial port at a time.
* **False Alarms / Ghost Objects:** If the buzzer sounds randomly, ensure your ESP32 has a stable power supply. Servo motors drawing high current can cause sensor brown-outs.