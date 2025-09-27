# ⚡ Growatt MIN Modbus Reader

[![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Modbus](https://img.shields.io/badge/Protocol-Modbus%20RTU%2FTCP-orange?style=for-the-badge)](https://modbus.org)
[![Growatt](https://img.shields.io/badge/Compatible-MIN%20Series-red?style=for-the-badge)](https://www.growatt.com)

> 🔌 **Direct local access to your Growatt MIN-series solar inverter data via Modbus - no cloud required!**

Transform your solar monitoring game by talking directly to your Growatt inverter through RS485 Modbus. Perfect for Home Assistant integrations, local dashboards, or any scenario where you want **real-time data without the cloud middleman**.

---

## 🚀 Features

- ⚡ **Real-time data polling** - Get fresh inverter readings every second
- 🌐 **TCP & Serial support** - Works with RS485-to-TCP converters or USB adapters
- 📊 **Smart meter integration** - Grid import/export tracking when meter connected
- 🏠 **Home Assistant ready** - JSON output perfect for HA sensors
- 🔄 **Version agnostic** - Handles both old and new pymodbus versions automatically
- 📈 **Energy flow calculations** - See exactly where your solar power is going
- 🎯 **Zero configuration** - Just set your IP and go!

---

## 📋 What You Get

### 🌞 Solar Production Data
- **PV String voltages & currents** (per string + total)
- **Real-time power generation** 
- **Daily and lifetime energy totals**

### ⚡ AC Output Monitoring  
- **Grid voltage, current, frequency**
- **Instantaneous power output**
- **Inverter temperature & status**

### 🏡 Grid & Load Analysis *(with smart meter)*
- **Grid export/import power** (live readings)
- **House consumption tracking**
- **Energy flow visualization**
- **Perfect grid balance detection**

---

## 🛠️ Hardware Setup

### Option 1: RS485-to-TCP Converter (Recommended)
```
Growatt MIN-10000 ──RS485──> EW11 Converter ──Ethernet──> Your Network
    (SYS COM Port)              (192.168.1.80)              (Python Script)
```

### Option 2: Direct USB Connection
```
Growatt MIN-10000 ──RS485──> USB-RS485 ──USB──> Computer
    (SYS COM Port)           Converter         (Python Script)
```

### 🔌 Physical Connections
- **Inverter side:** Connect to SYS COM port underneath unit
- **Wiring:** Use pins 3 & 4 (Modbus A & B) 
- **Settings:** 9600 baud, 8N1, no flow control
- **Modbus ID:** Usually 1 (configurable in inverter menu)

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv growatt_env
growatt_env\Scripts\activate  # Windows
source growatt_env/bin/activate  # Linux/Mac

# Install required packages
pip install pymodbus pyserial
```

### 2️⃣ Run the Script
```bash
# Use your converter's IP address
python growatt.py 192.168.1.80 502

# Or use defaults (192.168.1.100:502)
python growatt.py

# Serial connection
python growatt.py /dev/ttyUSB0 9600 1
```

### 3️⃣ Watch the Magic ✨

---

## 📊 Example Output

### 🌞 Sunny Day Production
```
==================================================
GROWATT MIN-10000 STATUS
==================================================
Status: Normal
Serial: MIN001234567890
Firmware: 1.24
Temperature: 42.3°C

SOLAR INPUT:
  PV1: 387.2V, 12.4A, 4800W
  PV2: 389.1V, 11.8A, 4590W
  Total: 9390W

AC OUTPUT:
  Voltage: 240.1V
  Current: 38.2A
  Power: 9170W
  Frequency: 50.02Hz

GRID (Smart Meter):
  Power: +6850W (EXPORTING)
  Voltage: 240.3V
  Current: 28.5A
  Frequency: 50.01Hz

LOAD:
  House Consumption: 2320W

ENERGY FLOW:
  Solar Production: 9390W
  House Consumption: 2320W
  Grid Export: 6850W
  Self Consumption: 2320W

ENERGY:
  Today: 45.7 kWh
  Total: 12847.3 kWh
```

### 🌙 Evening Import Mode
```
GRID (Smart Meter):
  Power: -1200W (IMPORTING)
  Voltage: 239.8V

ENERGY FLOW:
  Solar Production: 450W
  House Consumption: 1650W
  Grid Import: 1200W
  Self Consumption: 450W
```

---

## 🏠 Home Assistant Integration

The script outputs perfect JSON for Home Assistant sensors:

```json
{
  "solar": {
    "pv1_voltage": 387.2,
    "pv1_power": 4800,
    "total_power": 9390
  },
  "grid": {
    "power": 6850,
    "export_power": 6850,
    "import_power": 0
  },
  "load": {
    "power": 2320
  },
  "energy": {
    "today_kwh": 45.7,
    "total_kwh": 12847.3
  }
}
```

### 🔗 Integration Ideas
- **RESTful sensors** - Serve JSON via Flask
- **MQTT publishing** - Send data to Home Assistant via MQTT
- **Custom component** - Build a full HA integration
- **Energy dashboard** - Perfect for HA's energy features

---

## ⚙️ Configuration

### 🔧 Built-in Options
```python
CONFIG = {
    'connection_type': 'tcp',        # or 'serial'
    'host': '192.168.1.80',         # Your converter IP
    'port': 502,                    # Modbus TCP port
    'device': '/dev/ttyUSB0',       # For serial connections
    'baudrate': 9600,               # Serial baud rate
    'slave_id': 1                   # Inverter Modbus ID
}
```

### 🎛️ Command Line Options
```bash
python growatt.py [host] [port] [slave_id]

# Examples:
python growatt.py 192.168.1.80          # Just change IP
python growatt.py 192.168.1.80 502      # IP + port  
python growatt.py 192.168.1.80 502 2    # IP + port + slave ID
```

---

## 🔌 Smart Meter Support

### 🌟 Enhanced Features with Smart Meter
When you connect a compatible smart meter (Growatt Smart Meter or Eastron SDM230), you unlock:

- ✅ **Real grid export/import readings** (not calculated)
- ✅ **Actual house consumption tracking**  
- ✅ **Perfect energy balance monitoring**
- ✅ **Zero-export functionality** (if configured)

### 📐 Smart Meter Wiring
- **Meter location:** In-line with main electrical feed (electrician required)
- **Communication:** Connect to inverter pins 7 & 8 (CT/Meter port)
- **Configuration:** Change power harvester setting from 'CT Clamp' to 'Meter'

---

## 🔧 Troubleshooting

### 🚨 Common Issues

**"ImportError: pymodbus not available"**
```bash
pip install pymodbus pyserial
```

**"Connection failed"**
- ✅ Check IP address and port
- ✅ Verify RS485 wiring (pins 3 & 4)
- ✅ Confirm converter is powered and networked
- ✅ Test with Modbus testing tools first

**"No data returned"**
- ✅ Check Modbus slave ID (try 1, 2, or 3)
- ✅ Verify 1-second minimum polling interval
- ✅ Ensure no other Modbus masters on same line

**"Smart meter data missing"**
- ✅ Confirm meter is properly wired to inverter
- ✅ Check power harvester setting in Growatt config
- ✅ Verify meter Modbus address (usually 2 for Eastron)

---

## 🛡️ Compatibility

### ✅ Tested Inverters
- **Growatt MIN 3000-10000 TL-X series**
- **Growatt MIC series** (similar register layout)

### ✅ Compatible Hardware  
- **RS485-to-TCP:** EW11, USR-TCP232-410s, similar
- **RS485-to-USB:** Most generic converters
- **Smart Meters:** Growatt Smart Meter, Eastron SDM230

### ✅ Python Versions
- **Python 3.7+** (tested on 3.8, 3.9, 3.10, 3.11)
- **PyModbus 2.x & 3.x** (auto-detection)

---

## 🤝 Contributing

Found a bug? Have a feature request? Contributions welcome!

1. 🍴 Fork the repo
2. 🌿 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎯 Open a Pull Request

### 🎯 Ideas for Contributions
- Additional inverter model support
- Async/await implementation  
- MQTT integration examples
- Home Assistant custom component
- Grafana dashboard templates
- Battery storage register mapping (SPH series)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⭐ Show Your Support

If this project helped you monitor your solar system, give it a star! ⭐

---

## 🔗 Related Projects

- [OpenInverterGateway](https://github.com/OpenInverterGateway/OpenInverterGateway) - Custom firmware for WiFi dongles
- [Grott](https://github.com/johanmeijer/grott) - Growatt data interception proxy
- [Home Assistant Growatt Integration](https://github.com/indykoning/Growatt_ShineWiFi-S) - Official HA component

---

<div align="center">

**Made with ☀️ by the solar monitoring community**

*Harness the sun, monitor the flow, own your data* 🌞⚡📊

</div>