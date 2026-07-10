# Embedded Attendance System

A comprehensive, IoT-based attendance system using a fingerprint scanner (via ESP32) and a Flask backend server. This project allows institutions to track attendance with biometric security in real-time.

## Features
- **Hardware Integration**: Uses an R503 (or similar) fingerprint scanner via ESP32.
- **Real-Time Logging**: Sends fingerprint data to the centralized server.
- **Admin Dashboard**: View total students, attendance logs, and registered devices through the web interface.
- **Device Management**: Register and manage authorized scanner locations.
- **RESTful API**: Allows modular expansion and secure communication.

## Repository Structure
- `backend/`: The Flask web application, database models, and utility scripts.
- `hardware/`: The C++ source code for the ESP32 microcontroller and wiring diagrams.

## Prerequisites
- Python 3.8+
- Arduino IDE (with ESP32 board support)
- Wi-Fi connection for the ESP32 to communicate with the server

## Setup Instructions

### 1. Backend Setup
Navigate into the backend directory and set up a virtual environment:
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

Initialize the SQLite database and add a test device:
```bash
python reset.py
python sql.py
python add_stud.py
```

Run the server:
```bash
python app.py
```
*Note: Make sure your machine's IP is accessible by the ESP32 module over the network.*

### 2. Hardware Setup
- Open `hardware/esp_code.ino` in your Arduino IDE.
- Make sure you install the `Adafruit Fingerprint Sensor Library` from the Library Manager.
- Ensure the hardware wiring matches `hardware/esp_pinout.txt`.
- Update the HTTP request URL in the `.ino` file to point to your Flask server's IP address (e.g. `http://192.168.x.x:5000/api/attendance`).
- Flash to your ESP32.

## Simulation
If you do not have the physical hardware, you can run the hardware simulator to test the attendance endpoint:
```bash
cd backend
python hardware_simulator.py
```

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
